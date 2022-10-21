import mlflow
mlflow.set_tracking_uri("http://mlflow.localhost:3001/")
mlflow.set_experiment("0")
mlflow.log_metric(key="test", value=2)
mlflow.log_artifact("./metaflow.py")