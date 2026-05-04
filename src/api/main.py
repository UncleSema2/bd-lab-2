import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from cassandra.cluster import Cluster

from src.api.routes import router
from src.api.repositories.prediction_repository import PredictionRepository
from src.api.services.prediction_service import PredictionService


def read_setting(name: str) -> str:
    file_path = os.getenv(f"{name}_FILE")
    if not file_path:
        raise RuntimeError(f"Missing required setting file pointer: {name}_FILE")

    value = Path(file_path).read_text(encoding="utf-8").strip()
    if not value:
        raise RuntimeError(f"Empty setting in file for: {name}")

    return value


@asynccontextmanager
async def lifespan(app: FastAPI):
    cassandra_host = read_setting("CASSANDRA_HOST")
    cassandra_port = int(read_setting("CASSANDRA_PORT"))
    cassandra_username = read_setting("CASSANDRA_USERNAME")
    cassandra_password = read_setting("CASSANDRA_PASSWORD")
    cassandra_keyspace = read_setting("CASSANDRA_KEYSPACE")

    model_version = os.getenv("MODEL_VERSION", "1.0.0")

    auth_provider = None
    if cassandra_username and cassandra_password:
        from cassandra.auth import PlainTextAuthProvider
        auth_provider = PlainTextAuthProvider(
            username=cassandra_username,
            password=cassandra_password,
        )

    cluster = Cluster(
        [cassandra_host],
        port=cassandra_port,
        auth_provider=auth_provider,
    )

    try:
        cluster.connect()
    except Exception as e:
        if auth_provider:
            cluster = Cluster([cassandra_host], port=cassandra_port)
            cluster.connect()

    repository = PredictionRepository(cluster, cassandra_keyspace)

    prediction_service = PredictionService(
        config_path="config.ini",
        model_version=model_version,
        prediction_repository=repository,
    )

    app.state.cluster = cluster
    app.state.prediction_service = prediction_service

    try:
        yield
    finally:
        cluster.shutdown()


app = FastAPI(
    title="Breast Cancer Classifier",
    lifespan=lifespan,
)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
