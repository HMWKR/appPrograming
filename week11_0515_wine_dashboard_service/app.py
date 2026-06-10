from math import exp
from statistics import mean


CLASS_INFO = {
    "class_0": {
        "name": "Barolo",
        "description": "알코올과 프롤린 수치가 높고 색이 진한 편입니다.",
    },
    "class_1": {
        "name": "Grignolino",
        "description": "중간 정도의 색 강도와 균형 잡힌 페놀 특성을 보입니다.",
    },
    "class_2": {
        "name": "Barbera",
        "description": "색 강도와 산도 관련 특성이 두드러지는 편입니다.",
    },
}

TOP_FEATURES = [
    {"feature": "flavanoids", "importance": 0.202, "cumulative": 0.202},
    {"feature": "color_intensity", "importance": 0.171, "cumulative": 0.373},
    {"feature": "proline", "importance": 0.139, "cumulative": 0.513},
    {"feature": "alcohol", "importance": 0.112, "cumulative": 0.625},
    {"feature": "od280_od315", "importance": 0.112, "cumulative": 0.737},
    {"feature": "hue", "importance": 0.071, "cumulative": 0.807},
]

FALLBACK_ROWS = [
    {
        "sample_id": 1,
        "class_name": "class_0",
        "alcohol": 14.23,
        "flavanoids": 3.06,
        "color_intensity": 5.64,
        "proline": 1065.0,
        "od280_od315": 3.92,
        "hue": 1.04,
    },
    {
        "sample_id": 2,
        "class_name": "class_1",
        "alcohol": 12.37,
        "flavanoids": 2.45,
        "color_intensity": 2.12,
        "proline": 520.0,
        "od280_od315": 2.78,
        "hue": 1.19,
    },
    {
        "sample_id": 3,
        "class_name": "class_2",
        "alcohol": 13.17,
        "flavanoids": 0.63,
        "color_intensity": 7.90,
        "proline": 725.0,
        "od280_od315": 1.48,
        "hue": 0.60,
    },
]


def load_rows() -> list[dict]:
    try:
        from sklearn.datasets import load_wine
    except Exception:
        return FALLBACK_ROWS

    wine = load_wine()
    feature_index = {name: idx for idx, name in enumerate(wine.feature_names)}
    rows = []
    for index, values in enumerate(wine.data, start=1):
        rows.append(
            {
                "sample_id": index,
                "class_name": f"class_{int(wine.target[index - 1])}",
                "alcohol": round(float(values[feature_index["alcohol"]]), 2),
                "flavanoids": round(float(values[feature_index["flavanoids"]]), 2),
                "color_intensity": round(float(values[feature_index["color_intensity"]]), 2),
                "proline": round(float(values[feature_index["proline"]]), 2),
                "od280_od315": round(float(values[feature_index["od280/od315_of_diluted_wines"]]), 2),
                "hue": round(float(values[feature_index["hue"]]), 2),
            }
        )
    return rows


def filter_rows(class_name: str = "all") -> list[dict]:
    rows = load_rows()
    if class_name == "all":
        return rows
    if class_name not in CLASS_INFO:
        raise ValueError("class_name은 all, class_0, class_1, class_2 중 하나여야 합니다.")
    return [row for row in rows if row["class_name"] == class_name]


def summarize_by_class() -> list[dict]:
    rows = load_rows()
    summary = []
    for class_name in CLASS_INFO:
        class_rows = [row for row in rows if row["class_name"] == class_name]
        summary.append(
            {
                "class_name": class_name,
                "name": CLASS_INFO[class_name]["name"],
                "count": len(class_rows),
                "avg_alcohol": round(mean(row["alcohol"] for row in class_rows), 2),
                "avg_color_intensity": round(mean(row["color_intensity"] for row in class_rows), 2),
                "avg_flavanoids": round(mean(row["flavanoids"] for row in class_rows), 2),
            }
        )
    return summary


def _softmax(scores: dict[str, float]) -> dict[str, float]:
    max_score = max(scores.values())
    exps = {label: exp(score - max_score) for label, score in scores.items()}
    total = sum(exps.values())
    return {label: round(value / total, 4) for label, value in exps.items()}


def predict_wine(
    flavanoids: float,
    color_intensity: float,
    proline: float,
    alcohol: float,
    od280_od315: float,
    hue: float,
) -> dict:
    inputs = {
        "flavanoids": flavanoids,
        "color_intensity": color_intensity,
        "proline": proline,
        "alcohol": alcohol,
        "od280_od315": od280_od315,
        "hue": hue,
    }
    invalid = [name for name, value in inputs.items() if value <= 0]
    if invalid:
        raise ValueError(f"0보다 큰 값이 필요합니다: {', '.join(invalid)}")

    scores = {
        "class_0": alcohol * 0.28 + flavanoids * 0.32 + proline / 1000 * 0.28 + od280_od315 * 0.12,
        "class_1": hue * 0.30 + flavanoids * 0.18 + od280_od315 * 0.28 + (1 / color_intensity) * 0.45,
        "class_2": color_intensity * 0.34 + (1 / flavanoids) * 0.25 + alcohol * 0.12 + (1 / hue) * 0.22,
    }
    probabilities = _softmax(scores)
    prediction = max(probabilities, key=probabilities.get)
    return {
        "prediction": prediction,
        "name": CLASS_INFO[prediction]["name"],
        "description": CLASS_INFO[prediction]["description"],
        "probabilities": probabilities,
        "inputs": inputs,
    }


def dashboard_payload(
    flavanoids: float = 2.03,
    color_intensity: float = 5.06,
    proline: float = 747.0,
    alcohol: float = 13.0,
    od280_od315: float = 2.61,
    hue: float = 0.96,
) -> dict:
    return {
        "rows": filter_rows("all")[:10],
        "summary": summarize_by_class(),
        "feature_importance": TOP_FEATURES,
        "prediction": predict_wine(
            flavanoids=flavanoids,
            color_intensity=color_intensity,
            proline=proline,
            alcohol=alcohol,
            od280_od315=od280_od315,
            hue=hue,
        ),
    }


if __name__ == "__main__":
    payload = dashboard_payload()
    print("samples:", len(load_rows()))
    print("summary:", payload["summary"])
    print("prediction:", payload["prediction"])
