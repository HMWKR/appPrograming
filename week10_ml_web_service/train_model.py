import pickle
from pathlib import Path


MODEL_PATH = Path(__file__).with_name("model.pkl")


def build_model() -> dict:
    return {
        "name": "iris_rule_model",
        "thresholds": {
            "setosa_max_petal": 2.0,
            "versicolor_max_petal": 5.2,
        },
        "labels": ["setosa", "versicolor", "virginica"],
    }


def save_model(path: Path = MODEL_PATH) -> Path:
    model = build_model()
    path.write_bytes(pickle.dumps(model))
    return path


if __name__ == "__main__":
    saved_path = save_model()
    print(f"saved: {saved_path.name}")
