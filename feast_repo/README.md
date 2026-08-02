# Feast feature store

The feature definitions use `data/train.csv`, whose rolling values are computed
by `preprocess_data.py`. From the repository root, run:

```powershell
feast -c feast_repo apply
feast -c feast_repo materialize 2017-01-02T00:00:00Z 2030-01-01T00:00:00Z
python feast_repo/get_training_data.py
```

`get_training_data.py` requests features at each row's own timestamp and writes
the resulting point-in-time correct dataset to `feast_repo/training_dataset.csv`.
