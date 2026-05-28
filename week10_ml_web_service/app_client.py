from service_api import predict_species


def format_prediction(petal_length: float, sepal_length: float) -> str:
    result = predict_species(petal_length, sepal_length)
    return (
        f"예측 품종: {result['prediction']} "
        f"(petal={petal_length}, sepal={sepal_length})"
    )


if __name__ == "__main__":
    print(format_prediction(1.5, 5.1))
    print(format_prediction(4.8, 6.1))
