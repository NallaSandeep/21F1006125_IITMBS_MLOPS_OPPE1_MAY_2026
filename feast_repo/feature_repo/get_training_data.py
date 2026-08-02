from pathlib import Path

import pandas as pd
from feast import FeatureStore

repo_path = Path(__file__).parent
raw_data = pd.read_csv(repo_path.parent.parent / "data" / "train.csv")
raw_data["timestamp"] = pd.to_datetime(raw_data["timestamp"], utc=True)

entity_df = raw_data[["stock_name", "timestamp", "target"]]

store = FeatureStore(repo_path=str(repo_path))
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "stock_rolling_features:rolling_avg_10",
        "stock_rolling_features:volume_sum_10",
    ],
).to_df()

output_path = repo_path / "training_dataset.csv"
training_df.to_csv(output_path, index=False)

print(f"Created: {output_path}")
print(training_df.head())