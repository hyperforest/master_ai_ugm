from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
# from urllib.parse import urlparse
import pandas as pd

import mlflow
import mlflow.sklearn

iris = load_iris()
X = iris.data
y = iris.target
k = 3
p = 1
random_state = 21

mlflow.set_experiment('test_mlflow')

# for k in range(3, 11):
#     for p in range(1, 4):

with mlflow.start_run() as run:
    # mlflow.log_param('k', k)
    # mlflow.log_param('p', p)
    # mlflow.log_param('random_state', random_state)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.33, random_state=random_state)
    knn = KNeighborsClassifier(n_neighbors=k, p=p)

    mm = MinMaxScaler()
    X_train = mm.fit_transform(X_train)
    X_test = mm.transform(X_test)

    knn.fit(X_train, y_train)
    mlflow.sklearn.log_model(knn, "knn")

    y_pred = knn.predict(X_test)
    # y_pred_s = pd.Series(y_pred, name='prediction')
    # y_pred_s.to_csv('knn/pred.csv', index=False)

    res = classification_report(y_test, y_pred, output_dict=True)

    mlflow.log_metric('accuracy', res['accuracy'])
    # mlflow.log_metric('f1-score', res['macro avg']['f1-score'])
    # mlflow.log_metric('precision', res['macro avg']['precision'])
    # mlflow.log_metric('recall', res['macro avg']['recall'])

    # mlflow.log_artifact('knn')