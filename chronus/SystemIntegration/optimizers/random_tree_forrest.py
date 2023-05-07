from sklearn.model_selection import GridSearchCV

from chronus.domain.interfaces.optimizer_interface import OptimizerInterface
from chronus.domain.Run import Run


class RandomTreeOptimizer(OptimizerInterface):
    @staticmethod
    def name() -> str:
        return "random-tree"

    def make_model(self, runs: list[Run]):
        print("RandomTreeOptimizer.make_model")
        import numpy as np
        from sklearn.model_selection import train_test_split

        X = []
        y = []

        for run in runs:
            X.append([run.cores, run.threads_per_core, run.frequency])
            y.append(run.gflops_per_watt)

        X = np.array(X)
        y = np.array(y)

        param_grid = {
            "n_estimators": [10, 50, 100, 200],
            "max_depth": [None, 10, 20, 30],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "max_features": ["auto", "sqrt"],
            "bootstrap": [True, False],
        }
        from sklearn.ensemble import RandomForestRegressor

        rf = RandomForestRegressor(random_state=42)
        grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

        grid_search.fit(X, y)
        best_params = grid_search.best_params_

        print("Best hyperparameters:")
        print(best_params)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # random forrest regressor with these paremters {'bootstrap': False, 'max_depth': None, 'max_features': 'auto', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 10}
        model = RandomForestRegressor(**best_params, random_state=42)
        model.fit(X, y)

        from sklearn.metrics import mean_squared_error, r2_score

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

        configurations_np = np.array([list(config.values()) for config in configurations])
        predicted_efficiencies = model.predict(configurations_np)
        best_config_index = np.argmax(predicted_efficiencies)

        best_config = configurations[best_config_index]
        best_efficiency_pred = predicted_efficiencies[best_config_index]

        print("Best predicted configuration:")
        print(f"Cores: {best_config['cores']}")
        print(f"Threads per core: {best_config['threads_per_core']}")
        print(f"Frequency: {best_config['frequency']} Hz")
        print(f"Predicted energy efficiency: {best_efficiency_pred} GFLOPS/Watt")
