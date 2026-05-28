WINE_ROWS = [
    {"wine_id": "W001", "alcohol": 13.2, "color_intensity": 5.1, "flavanoids": 3.0, "class_name": "class_0"},
    {"wine_id": "W002", "alcohol": 12.3, "color_intensity": 3.2, "flavanoids": 2.1, "class_name": "class_1"},
    {"wine_id": "W003", "alcohol": 14.1, "color_intensity": 7.2, "flavanoids": 1.3, "class_name": "class_2"},
    {"wine_id": "W004", "alcohol": 13.8, "color_intensity": 6.8, "flavanoids": 1.1, "class_name": "class_2"},
    {"wine_id": "W005", "alcohol": 12.8, "color_intensity": 4.8, "flavanoids": 2.9, "class_name": "class_0"},
]

FEATURE_IMPORTANCE = [
    {"feature": "color_intensity", "importance": 0.45},
    {"feature": "flavanoids", "importance": 0.35},
    {"feature": "alcohol", "importance": 0.20},
]


def summarize_by_class() -> list[dict]:
    classes = sorted({row["class_name"] for row in WINE_ROWS})
    summary = []
    for class_name in classes:
        rows = [row for row in WINE_ROWS if row["class_name"] == class_name]
        summary.append(
            {
                "class_name": class_name,
                "count": len(rows),
                "avg_alcohol": round(sum(row["alcohol"] for row in rows) / len(rows), 2),
                "avg_color_intensity": round(sum(row["color_intensity"] for row in rows) / len(rows), 2),
            }
        )
    return summary


def predict_wine(alcohol: float, color_intensity: float, flavanoids: float) -> dict:
    if alcohol <= 0 or color_intensity <= 0 or flavanoids <= 0:
        raise ValueError("입력값은 모두 0보다 커야 합니다.")
    if color_intensity >= 6.0:
        label = "class_2"
    elif flavanoids >= 2.5:
        label = "class_0"
    else:
        label = "class_1"
    return {"prediction": label, "alcohol": alcohol, "color_intensity": color_intensity, "flavanoids": flavanoids}


def dashboard_payload(alcohol: float, color_intensity: float, flavanoids: float) -> dict:
    return {
        "rows": WINE_ROWS,
        "summary": summarize_by_class(),
        "feature_importance": FEATURE_IMPORTANCE,
        "prediction": predict_wine(alcohol, color_intensity, flavanoids),
    }


if __name__ == "__main__":
    print(dashboard_payload(13.0, 5.0, 3.1))
