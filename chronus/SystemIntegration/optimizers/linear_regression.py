import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.Run import Run


class LinearRegressionOptimizer(OptimizerInterface):
    def make_model(self, runs: list[Run]):
        df = runs_to_dataframe(runs)

        # Convert the columns to appropriate data types
        df = df.apply(pd.to_numeric, errors="ignore")

        # Display the dataframe
        print(df)

        # Preprocess the data
        X = df.drop(columns=["gflops_per_watt"])  # Input features
        y = df["gflops_per_watt"]  # Target variable

        # Create and train the model
        model = create_model()
        model.fit(X, y)

        # Find the best configuration
        best_config = model.best_estimator_
        print("Best configuration:", best_config)

        # Find the best hyperparameters
        best_hyperparameters = model.best_params_
        print("Best hyperparameters:", best_hyperparameters)

        configurations = generate_configurations()
        best_config, best_efficiency = find_best_configuration(model, configurations)

        print("Best configuration:", best_config)
        print("Best energy efficiency (gflops_per_watt):", best_efficiency)


def runs_to_dataframe(runs: list[Run]) -> pd.DataFrame:
    data = []
    for run in runs:
        data.append(
            {
                "cores": run.cores,
                "threads_per_core": run.threads_per_core,
                "frequency": run.frequency,
                "gflops_per_watt": run.gflops_per_watt,
            }
        )
    return pd.DataFrame(data)


def preprocess_data(df):
    # Extract the features and the target
    X = df[["cores", "thread_per_core", "frequency"]]
    y = df["gflops_per_watt"]

    return X, y


def create_model():
    # Create a pipeline with polynomial features, standard scaler, and linear regression
    pipeline = Pipeline(
        [
            ("poly_features", PolynomialFeatures(include_bias=False)),
            ("std_scaler", StandardScaler()),
            ("lin_reg", LinearRegression()),
        ]
    )

    # Hyperparameters to be tuned
    param_grid = {
        "poly_features__degree": [2, 3, 4],
    }

    # Grid search to find the best hyperparameters
    model = GridSearchCV(pipeline, param_grid, cv=5, scoring="neg_mean_squared_error")

    return model


def generate_configurations():
    # Define the range of cores, threads_per_core, and frequencies you want to test
    cores_range = range(1, 33)
    threads_per_core_range = range(1, 3)
    frequencies_range = [1500000.0, 2200000.0, 2500000.0]

    # Generate all possible combinations of configurations
    configurations = [
        {"cores": cores, "threads_per_core": tpc, "frequency": freq}
        for cores in cores_range
        for tpc in threads_per_core_range
        for freq in frequencies_range
    ]

    return configurations


def find_best_configuration(model, configurations):
    best_config = None
    best_efficiency = -1

    for config in configurations:
        X_test = pd.DataFrame([config])  # Convert the configuration into a DataFrame
        predicted_efficiency = model.predict(X_test)[0]  # Predict the energy efficiency

        if predicted_efficiency > best_efficiency:
            best_config = config
            best_efficiency = predicted_efficiency

    return best_config, best_efficiency
