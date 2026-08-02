# AI Usage Documentation

## AI Tools Utilized and Conversation History

- Tool Name: OpenAI Codex
  - Purpose: Assistance with adapting the MLflow training script to the stock
    training data, setting up DVC data-versioning steps, and defining a Feast
    feature store with point-in-time historical retrieval.
  - Shared Chat Link: Not available. This Codex session does not provide a
    public share link.
  - Notes: No other GenAI/LLM tools were used. The substantive prompt/response
    record is included below.

- Tool Name: ChatGPT
  - Purpose: Additional AI assistance related to the exam work.
  - Shared Chat Link: https://chatgpt.com/share/6a6f467d-59e4-83e8-b2cc-bf88fb315f05
  - Notes: Public conversation shared by the student.

---

## 3 Prompts and Responses Used

### Tool Name #1: OpenAI Codex

- Prompt 1: `please change graded_assignment.py according to data/train.csv file`
  - Response Log: Inspected `data/train.csv` and updated
    `graded_assignment.py` to use the stock-data feature columns `open`,
    `high`, `low`, `close`, `volume`, `rolling_avg_10`, and `volume_sum_10`,
    with `target` as the binary label. The response also updated MLflow naming,
    added data validation, and saved a model and predictions as artifacts.

- Prompt 2: Provided the Deliverable 2 and Deliverable 3 specifications.
  - Response Log: Identified the required DVC workflow: initialize DVC, track
    `data/v0` and `data/v1` using separate `.dvc` pointer files, configure a
    GCS remote, push the cached data, and demonstrate restoration using
    `dvc pull`. Prepared Feast definitions for entity `stock_name` and features
    `rolling_avg_10` and `volume_sum_10`, plus a point-in-time retrieval script.

- Prompt 3: Supplied the result of `feast -c feast_repo apply`, which failed
  because `train.csv` was interpreted as Parquet.
  - Response Log: Diagnosed that Feast's file offline store expects Parquet.
    Recommended converting the CSV source to Parquet and changing `FileSource`
    to `data/stock_features.parquet`. Also added `ValueType.STRING` to the
    `stock_name` entity to address the Feast deprecation warning.

- Prompt 4: `I want to start from feast init by deleteing existing folder. Please guide me step by step`
  - Response Log: Explained how to remove only the old Feast directory, run
    `feast init`, configure `feature_store.yaml`, convert the processed source
    CSV to Parquet, define the entity and feature view, apply definitions,
    materialize the features, and retrieve historical features.

- Prompt 5: Explained that `feast init` created a nested
  `feast_repo/feature_repo` directory and asked where to keep
  `prepare_feast_data.py`.
  - Response Log: Confirmed the nested repository layout was valid. Directed
    that `prepare_feast_data.py`, `feature_definitions.py`, and
    `get_training_data.py` should be stored in
    `feast_repo/feature_repo/`, with input data addressed as
    `../../data/train.csv` from that location.

- Prompt 6: Asked whether generated `test_workflow.py` could be deleted.
  - Response Log: Confirmed it is a generated sample workflow and is not needed
    for the stock-feature solution.

- Prompt 7: Asked for the next step after generating the Parquet file.
  - Response Log: Directed execution of `feast apply`, `feast materialize`, and
    `get_training_data.py`, and described that the expected output is a
    point-in-time correct training CSV.

- Prompt 8: Asked what `get_training_data.py` is.
  - Response Log: Explained that it retrieves historical Feast features at each
    entity row's timestamp to prevent future data leaking into earlier training
    rows. Provided a script using `FeatureStore.get_historical_features` with
    `stock_name`, `timestamp`, and `target`.

- Prompt 9: Reported the message `Using timestamp as the event timestamp` and
  then a `Killed` process while running the historical retrieval.
  - Response Log: Clarified that the timestamp message is informational and
    that `Killed` indicates a Workbench memory limit during the large historical
    join. Recommended reducing the demonstration source to 5,000 feature rows
    and the retrieval entity dataframe to 100 rows, while retaining
    point-in-time correct retrieval.

- Prompt 10: Asked whether to continue after Feast processing remained blocked.
  - Response Log: Recommended proceeding to the DVC deliverable while retaining
    the Feast implementation files and documenting the memory limitation.

- Prompt 11: Repeated the DVC and Feast deliverable requirements.
  - Response Log: Provided the DVC command sequence: `dvc init`, configure a
    GCS remote, remove Git tracking from `data/v0` and `data/v1`, run
    `dvc add` for each directory, commit `data/v0.dvc` and `data/v1.dvc`, run
    `dvc push`, and demonstrate restoration with a Git checkout followed by
    `dvc pull`.

---

## AI-Assisted Files

- `graded_assignment.py`: Adapted from Iris classification to stock direction
  classification using `data/train.csv`.
- `feast_repo/feature_repo/feature_store.yaml`: Local Feast configuration.
- `feast_repo/feature_repo/feature_definitions.py`: Defines entity
  `stock_name` and rolling feature view.
- `feast_repo/feature_repo/prepare_feast_data.py`: Converts the processed CSV
  source to Parquet for Feast.
- `feast_repo/feature_repo/get_training_data.py`: Requests historical,
  point-in-time correct feature values.

## Limitations Encountered

The full Feast historical retrieval was terminated by the Workbench environment
(`Killed`), indicating insufficient memory for the full source/query join. The
recommended reduced-size retrieval preserves the point-in-time retrieval method
for demonstration purposes.
