from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from pathlib import Path
import os


class CassandraSettings:
    def __init__(self):
        self.host = os.getenv("CASSANDRA_HOST", "cassandra")
        self.port = int(os.getenv("CASSANDRA_PORT", "9042"))
        self.username = os.getenv("CASSANDRA_USERNAME", "cassandra")
        self.password = os.getenv("CASSANDRA_PASSWORD", "cassandra")
        self.keyspace = os.getenv("CASSANDRA_KEYSPACE", "ml_predictions")

    def get_cluster(self) -> Cluster:
        if self.username and self.password:
            auth_provider = PlainTextAuthProvider(
                username=self.username,
                password=self.password,
            )
        else:
            auth_provider = None

        return Cluster(
            [self.host],
            port=self.port,
            auth_provider=auth_provider,
        )


settings = CassandraSettings()
