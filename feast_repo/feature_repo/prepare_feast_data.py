from pathlib import Path
import pandas as pd

repo_path = Path(__file__).parent
source_path = repo_path.parent.parent / "data" / "train.csv"
output_path = repo_path / "data" / "stock_features.parquet"

data = pd.read_csv(source_path)
data["timestamp"] = pd.to_datetime(data["timestamp"], utc=True)

output_path.parent.mkdir(exist_ok=True)
data.to_parquet(output_path, index=False)

print(f"Created: {output_path}")