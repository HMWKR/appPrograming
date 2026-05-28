import pickle
from pathlib import Path


MODEL_PATH = Path(__file__).with_name("model.pkl")


def load_model(path: Path = MODEL_PATH) -> dict:
    if not path.exists():
        from train_model import save_model

        save_model(path)
    return pickle.loads(path.read_bytes())


def predict_species(petal_length: float, sepal_length: float) -> dict:
    if petal_length <= 0 or sepal_length <= 0:
        raise ValueError("petal_length와 sepal_length는 0보다 커야 합니다.")

    model = load_model()
    if petal_length <= model["thresholds"]["setosa_max_petal"]:
        label = "setosa"
    elif petal_length <= model["thresholds"]["versicolor_max_petal"]:
        label = "versicolor"
    else:
        label = "virginica"

    return {
        "input": {
            "petal_length": petal_length,
            "sepal_length": sepal_length,
        },
        "prediction": label,
        "model": model["name"],
    }


if __name__ == "__main__":
    print(predict_species(4.8, 6.1))
