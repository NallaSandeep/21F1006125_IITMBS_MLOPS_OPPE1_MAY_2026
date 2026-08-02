from pathlib import Path

import joblib
import mlflow
import pandas as pd
from mlflow.models import infer_signature
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier


TARGET_COLUMN = "target"
FEATURE_COLUMNS = [
    "open",
    "high",
    "low",
    "close",
    "volume",
    "rolling_avg_10",
    "volume_sum_10",
]


def load_data(path):
    """Load the processed stock-price training data."""
    data = pd.read_csv(path)
    required_columns = set(FEATURE_COLUMNS + [TARGET_COLUMN])
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(
            "The training data is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    return data.dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN]).copy()


def split_data(data):
    """Create a stratified train/validation split for the binary price-direction target."""
    X = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN].astype(int)

    return train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42,
    )


def train_model_log_mlflow(X_train, y_train, X_test, y_test):
    mlflow.set_tracking_uri("http://136.64.73.131:8100")
    mlflow.set_experiment("stock_price_direction_experiment")

    with mlflow.start_run():
        params = {"max_depth": 4, "random_state": 1, "min_samples_split": 3}
        model = DecisionTreeClassifier(**params)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, zero_division=0),
            "recall": recall_score(y_test, predictions, zero_division=0),
            "f1_score": f1_score(y_test, predictions, zero_division=0),
        }

        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(
            sk_model=model,
            name="decision_tree_model",
            registered_model_name="StockDirectionDecisionTree",
            input_example=X_test.head(),
            signature=infer_signature(X_test, predictions),
        )

        print(f"Accuracy={metrics['accuracy']:.4f}")
        return model, predictions, metrics["accuracy"]


def main():
    data = load_data("data/train.csv")
    X_train, X_test, y_train, y_test = split_data(data)
    model, predictions, _ = train_model_log_mlflow(X_train, y_train, X_test, y_test)

    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    joblib.dump(model, artifacts_dir / "model.joblib")
    pd.DataFrame({"actual": y_test.to_numpy(), "prediction": predictions}).to_csv(
        artifacts_dir / "predictions.csv", index=False
    )


if __name__ == "__main__":
    main()
