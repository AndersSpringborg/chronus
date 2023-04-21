from typing import List

import json
import os
from pprint import pprint

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVR

from chronus.domain.Run import Run

param_grid = {
    "C": [0.1, 1, 10],
    "kernel": ["linear", "poly", "rbf", "sigmoid"],
    "gamma": ["scale", "auto"],
}


def fit_model(x_train: any, y_train: any):
    file_path = "../out/best_params.json"
    if os.path.isfile(file_path):
        print("Loading best parameters from file...")
        with open(file_path) as f:
            best_params = json.load(f)
        return SVR(**best_params), best_params

    # Create an SVM model with support vector regression
    svm = SVR()

    # Create a grid search object with cross-validation
    grid_search = GridSearchCV(
        estimator=svm,
        param_grid=param_grid,
        cv=5,
        scoring="neg_mean_squared_error",
        verbose=1,
        n_jobs=-1,
    )

    # Fit the grid search object to the training data
    pprint("Finding best hyperparameters for SVM model...")
    grid_search.fit(x_train, y_train)

    # Print the best hyperparameters found
    print("Best hyperparameters:", grid_search.best_params_)
    print("Saving best parameters to file...")
    with open("../out/best_params.json", "w") as f:
        json.dump(grid_search.best_params_, f)

    # Return the best model found
    return grid_search.best_estimator_, grid_search.best_params_


def config_model(data: list[Run]):
    # Split the data into training and testing sets
    X = [[run.cpu_cores, run.cpu_clock] for run in data]
    y = [run.gflops for run in data]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Fit the SVM model and perform grid search
    svm, best_params = fit_model(X_train, y_train)
    print("Best model:", svm)

    # Evaluate the performance of the best model on the test data
    y_pred = svm.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print("MSE:", mse)
    return best_params
