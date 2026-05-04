# Breast Cancer Classifier (ML Pipeline)

Классификатор злокачественных опухолей груди на основе логистической регрессии.

В проекте есть полный цикл:
- предобработка данных
- обучение модели
- FastAPI для инференса
- DVC для версионирования артефактов
- pytest для тестирования

---

# Dataset

Используется датасет Breast Cancer Wisconsin из scikit-learn.

Характеристики:
- 569 образцов
- 30 признаков (радиус, текстура, периметр, площадь и т.д.)
- 2 класса: злокачественная (1) и доброкачественная (0) опухоль
- данные предобработаны и сохранены в `data/raw/`

---

# Модель

Логистическая регрессия:
- максимальное количество итераций: 10000
- стандартизация признаков: StandardScaler

---

# Pipeline

DVC pipeline состоит из двух этапов:

1. preprocess - разбиение данных на train/test
   - вход: `data/raw/X.csv`, `data/raw/y.csv`
   - выход: `data/processed/X_train.csv`, `data/processed/y_train.csv`, `data/processed/X_test.csv`, `data/processed/y_test.csv`

2. train - обучение классификатора
   - вход: `data/processed/*.csv`
   - выход: `experiments/log_reg.sav`, `experiments/scaler.pkl`

Запуск pipeline:
```bash
dvc repro
```

---

# API

Простой FastAPI сервис с одним эндпоинтом для предсказания.

## Эндпоинты

- `/health` -- проверка состояния сервиса
- `/predict` -- предсказание класса опухоли

## /predict

POST запрос с параметрами: [tests/test_0.json](tests/test_0.json)

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d @tests/test_0.json
```

Ответ:
```json
{
  "prediction": 0,
  "model": "LOG_REG"
}
```

---

# Установка и запуск

## Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск DVC pipeline

```bash
dvc repro
```

## Запуск API

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI: http://localhost:8000/docs

## Запуск через Docker

```bash
docker-compose up --build
```

## Тестирование

```bash
pytest tests/
```
