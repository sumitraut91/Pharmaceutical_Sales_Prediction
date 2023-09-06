from pathlib import Path

class Config:
    RANDOM_SEED = 42
    ASSETS_PATH = Path("../")
    REPO = r"C:\Users\Sumit\Desktop\Sumit\Internship\Project 2"
    MODELS_PATH = ASSETS_PATH / "models"
    DATASET_FILE_PATH = "data/store.csv"
    DATASET_PATH = ASSETS_PATH / "data"
    FEATURES_PATH = ASSETS_PATH / "features"
    MODELS_PATH = ASSETS_PATH / "models"
    METRICS_FILE_PATH = ASSETS_PATH / "metrics"