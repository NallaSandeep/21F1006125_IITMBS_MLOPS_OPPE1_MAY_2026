"""Build a point-in-time correct training set from the Feast feature store."""

from pathlib import Path

import pandas as pd
from feast import FeatureStore


REPOSITORY_PATH = Path(__file__).parent
TRAINING_DATA_PATH = REPOSITORY_PATH.parent / "data" / "train.csv"


def get_training_data():
    raw_data = pd.read_csv(TRAINING_DATA_PATH)
    raw_data["timestamp"] = pd.to_datetime(raw_data["timestamp"], utc=True)

    # Each row asks Feast for values belonging to that stock as of its timestamp.
    # This prevents later values from being joined into historical training rows.
    entity_dataframe = raw_data[["stock_name", "timestamp", "target"]]
    store = FeatureStore(repo_path=str(REPOSITORY_PATH))
    return store.get_historical_features(
        entity_df=entity_dataframe,
        features=[
            "stock_rolling_features:rolling_avg_10",
            "stock_rolling_features:volume_sum_10",
        ],
    ).to_df()


if __name__ == "__main__":
    output_path = REPOSITORY_PATH / "training_dataset.csv"
    get_training_data().to_csv(output_path, index=False)
    print(f"Wrote point-in-time correct training data to {output_path}")
