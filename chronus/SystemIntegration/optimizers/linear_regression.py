from chronus.domain.Run import Run
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from chronus.domain.interfaces.optimizer_interface import OptimizerInterface


class LinearRegressionOptimizer(OptimizerInterface):
    def make_model(self, runs: list[Run]):
        headers = Run.schema()["properties"].keys()
        df = pd.DataFrame(runs, columns=headers)

        # Convert the columns to appropriate data types
        df = df.apply(pd.to_numeric, errors='ignore')
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])

        # Display the dataframe
        print(df)

        # Preprocess the data
        X, y = preprocess_data(df)

        # Create and train the model
        model = create_model()
        model.fit(X, y)

        # Find the best configuration
        best_config = model.best_estimator_
        print("Best configuration:", best_config)

        # Find the best hyperparameters
        best_hyperparameters = model.best_params_
        print("Best hyperparameters:", best_hyperparameters)


def preprocess_data(df):
    # Extract the features and the target
    X = df[['cores', 'thread_per_core', 'frequency']]
    y = df['gflops_per_watt']

    return X, y


def create_model():
    # Create a pipeline with polynomial features, standard scaler, and linear regression
    pipeline = Pipeline([
        ('poly_features', PolynomialFeatures(include_bias=False)),
        ('std_scaler', StandardScaler()),
        ('lin_reg', LinearRegression())
    ])

    # Hyperparameters to be tuned
    param_grid = {
        'poly_features__degree': [2, 3, 4],
    }

    # Grid search to find the best hyperparameters
    model = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')

    return model



