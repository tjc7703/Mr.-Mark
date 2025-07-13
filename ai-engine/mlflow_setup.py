import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("mrmark-ai-experiment")

    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)

    with mlflow.start_run():
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")
        print(f"Logged run with accuracy: {acc}") 