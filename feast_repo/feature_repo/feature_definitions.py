from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource, ValueType
from feast.types import Float64

stock_source = FileSource(
    name="stock_training_source",
    path="data/stock_features.parquet",
    timestamp_field="timestamp",
)

stock = Entity(
    name="stock_name",
    join_keys=["stock_name"],
    value_type=ValueType.STRING,
)

stock_rolling_features = FeatureView(
    name="stock_rolling_features",
    entities=[stock],
    ttl=timedelta(days=3650),
    schema=[
        Field(name="rolling_avg_10", dtype=Float64),
        Field(name="volume_sum_10", dtype=Float64),
    ],
    source=stock_source,
)