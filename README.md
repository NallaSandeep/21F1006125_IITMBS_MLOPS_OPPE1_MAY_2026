# OPPE1

## Overview

Build a stock movement predictor with end-to-end MLOps tooling (DVC, Feast, MLflow, and CI with CML) on Google Cloud Platform.

## Problem Description
Being an MLOps engineer in an investment firm, my task is to build a predictor for stock movements in the next 5 minutes.

Using minute-level and historical data, predict at every minute whether a particular stock will trade up or down 5 minutes later.

### Target and Training Details
* Predict 1 if the stock will close 5 minutes later at a price higher than the current price, and 0 otherwise.
* Use the past 10 minutes of data to predict the outcome 5 minutes into the future.
* Create the prediction/target column for the entire dataset based on actual stock price values. Use this as the ground truth for training and testing.
* Train the predictor in two iterations:
  * Iteration 1: Use v0 data only.
  * Iteration 2: Use the merged data of v0 and v1.
* If data is missing, process the last 10 available data points.

## Objectives

* Data Versioning with DVC
* Feast Feature Store Integration
* Training & Evaluation
* Hyperparameter Tuning & Experiment Tracking with MLflow
* CI on Main Branch with CML Report Generation

## Included Files
* graded_assignment.py - Load data, splits the data to train and test, builds the model using train data, upload the model to mlflow model registry, validates the model using test data
* data folder - Contains different sets of iris data
* Unit test files
  * test_data_validation.py - Validates the sanity of input data file
  * test_graded_assignment.py - Validates the functionality of functions present in graded_assigment.py
  * test_model_evaluation.py - Validates the mlflow best/latest model accuracy, precision, recall and f1 score
* .github/workflows/ci.yaml - Contains the set of Github actions configuration
* Configure GCP Cloud Storage as remote DVC dvc remote add -d storage gs://mlops-course-project-eada5958-ab21-4f76-b53-graded-assignments Use 'dvc remote list' for existing remote configuration
* Create DVC pipeline dvc stage add -n train -d graded_assignment.py -d data/iris.csv -o artifacts/model.joblib -o artifacts/predictions.csv python graded_assignment.py
* dvc.lock - Data model versioning result (of dvc repro command)
* dvc.yaml - DVC configuration that includes training of the model, adding input dependencies
  * Removed model dependency from dvc

## Steps to launch Vertex AI Workbench
* Open Google Cloud Console
* Search and open 'Vertex AI (Agentic Platform)' page
* Select 'Notebooks' section
* Select 'Workbench' section
* Create a workbench instance if not created; Start the existing workbench instance if it already exists

## Steps to start MLFlow instance
* Open the workbench instance in SSH mode
* Install mlflow library (pip install mlflow)
* Create a new screen (screen -S mlflow_experiment)
* Start mlflow server
  ```
  mlflow server \
    --host 0.0.0.0 \
    --port 8100 \
    --allowed-hosts "*" \
    --cors-allowed-origins "*"
  ```
* Press keys Ctrl + A and Ctrl + D to detach from screen
* To list the existing screens, use 'screen -list'
* To reattach to previous screen, use 'screen -R mlflow_experiment)
* Create a firewall rule to allow mlflow instance (External IP address of VPC instance, port: 8100)
* Get the external IP address of the VM instance and access the IP (Say 34.66.27.54:8100) -> MLFlow UI page displays

# Setup
## Git
* Run 'git clone https://github.com/21f1006125-ds/21f1006125_MLOPS_WEEKLY_ASSIGNMENT.git'
* Enter credentials (Username and Password)
* Run 'cd 21f1006125_MLOPS_WEEKLY_ASSIGNMENT/'
* Run 'git commit -m 'test commit'' 
* Run 'git push'
* Run 'git config --global credential.helper store'
* Run 'git tag -a version -m "data with n records"
* git config --global user.email "21f1006125@ds.study.iitm.ac.in"
* git config --global user.name "21f1006125"

## Storage Bucket
* Create a new bucket
```gcloud storage buckets create gs://mlops_course_oppe1```

## GCP
* From Google console, configure workload identify federal pool (ie., github pool)
* Create a github provider (https://iam.googleapis.com/projects/434534994925/locations/global/workloadIdentityPools/github-pool/providers/github)
* Include repository matching condition
```
assertion.repository in [
  '21f1006125-ds/21f1006125_MLOPS_WEEKLY_ASSIGNMENT',
  '21f1006125-ds/21F1006125_IITMBS_MLOPS_OPPE1_MAY_2026_MOCK',
 '21f1006125-ds/21F1006125_IITMBS_MLOPS_OPPE1_MAY_2026'
]
```
* Go to Service Accounts screen -> Select the intended service account
* Assign Workload Identify User role to principalSet://iam.googleapis.com/projects/434534994925/locations/global/workloadIdentityPools/github-pool/attribute.repository/21f1006125-ds/21f1006125_MLOPS_WEEKLY_ASSIGNMENT

## Python
* Run 'python3 -m venv .env'
* Run 'source .env/bin/activate'
* Run 'pip install -r requirements.txt'

## DVC
* Run 'dvc init'
* Run 'dvc remote list'
* Run 'dvc remote add -d storage gs://mlops_course_oppe1'
* Create DVC pipeline dvc stage add -n train -d graded_assignment.py -d data/iris.csv -o artifacts/model.joblib -o artifacts/predictions.csv python graded_assignment.py
* Run 'dvc config core.autostage true'
* Run 'dvc pull' to pull corresponding versioned data
* Run 'dvc repro' to train model and build dvc data and model versions
* Run 'dvc push' to push data and model version objects to Google cloud storage

## Feast
* Create feast store
```feast init feast_repo```
* Generate a feature file
* Modify feast_repo/feature_repo configuration files
```
feature_definitions.py
feature_store.yaml
```
* Run 
```
cd ./data/feast_repo/feature_repo
feast apply
```
* Train model on historical feast feature store data

## Commands
* Activate Google Cloud Shell
* Run 'cd mlops/week5/' (create a directory if it doesn't exist)
* Run 'git clone https://github.com/21f1006125-ds/21f1006125_MLOPS_WEEKLY_ASSIGNMENT.git'
* Enter credentials (Username and Password)
* Run 'cd 21f1006125_MLOPS_WEEKLY_ASSIGNMENT/'
* Run 'python3 -m venv .env'
* Run 'source .env/bin/activate'
* Run 'pip install -r requirements.txt'
* Run 'dvc init'
* Run 'dvc remote add -d storage gs://mlops-course-project-eada5958-ab21-4f76-b53-graded-assignments'
* Run 'dvc remote list' for existing remote configuration
* Run 'dvc pull' to pull corresponding versioned data
* Run 'dvc repro' to train model and build dvc data and model versions
* Run 'dvc push' to push data and model version objects to Google cloud storage


## Hyper Parameter Tuning Results
### version 1
* max_depth = 4; min_samples_split = 3
* Test accuracy score - 0.95
### version 2
* max_depth = 3; min_samples_split = 2
* Test accuracy score - 0.983
