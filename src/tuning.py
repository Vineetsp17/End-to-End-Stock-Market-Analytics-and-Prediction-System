from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

def tune_random_forest(X_train, y_train):

    param_dist = {
        "n_estimators": [50, 100, 200, 300],
        "max_depth": [None, 5, 10, 20, 30],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "max_features": ["sqrt", "log2"]
    }

    model = RandomForestRegressor(random_state=42)

    random_search = RandomizedSearchCV(
        model,
        param_distributions=param_dist,
        n_iter=15,
        cv=3,
        scoring="neg_mean_squared_error",
        random_state=42,
        n_jobs=-1
    )

    random_search.fit(X_train, y_train)

    print("Best Parameters:", random_search.best_params_)

    return random_search.best_estimator_