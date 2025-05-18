import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
from sklearn.metrics import mean_squared_error

# data preparation
df = pd.read_csv('economic_indicators_dataset_2010_2023.csv')

# drop feature
df = df.drop('Date', axis=1)

# one-hot encoding
nominal_column = ['Country']
df = pd.get_dummies(df, columns=nominal_column, drop_first=False)

# X, y split
X = df.drop('Inflation Rate (%)', axis=1)
y = df['Inflation Rate (%)']

# train, test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# AutoML configuration
automl = AutoML(
        mode='Explain',
        algorithms=['Xgboost', 'Random Forest', 'Neural Network'],
        train_ensemble=False,
        stack_models=False,
        eval_metric='rmse',
        explain_level=2
        )

# run AutoML process (test several models & store best model)
automl.fit(X_train, y_train)

# predict with the best model
predictions = automl.predict(X_test)
print('RMSE of best model:', np.sqrt(mean_squared_error(y_test, predictions)))

# result of all model
automl.report()
leaderboard = automl.get_leaderboard()
print(leaderboard[['model_type', 'metric_value', 'train_time']])

# partition
print("--------------------------------------------------------")

# AutoML2 configuration
automl2 = AutoML(
        mode='Perform',
        features_selection=False,
        algorithms=['Xgboost', 'Random Forest', 'Neural Network'],
        train_ensemble=False,
        stack_models=False,
        eval_metric='rmse',
        explain_level=2
        )

# run AutoML process (test several models & store best model)
automl2.fit(X_train, y_train)

# predict with the best model
predictions = automl2.predict(X_test)
print('RMSE of best model:', np.sqrt(mean_squared_error(y_test, predictions)))

# result of all model
automl2.report()
leaderboard = automl2.get_leaderboard()
print(leaderboard[['model_type', 'metric_value', 'train_time']])

# partition
print("--------------------------------------------------------")

# AutoML3 configuration
automl3 = AutoML(
        mode='Perform',
        features_selection=False,
        algorithms=['Xgboost', 'Random Forest', 'Neural Network'],
        train_ensemble=False,
        stack_models=False,
        eval_metric='rmse',
        validation_strategy={
            'validation_type': 'kfold',
            'k_folds': 7,
            'shuffle': False,
            'stratify': False
            },
        explain_level=2
        )

# run AutoML process (test several models & store best model)
automl3.fit(X_train, y_train)

# predict with the best model
predictions = automl3.predict(X_test)
print('RMSE of best model:', np.sqrt(mean_squared_error(y_test, predictions)))

# result of all model
automl3.report()
leaderboard = automl3.get_leaderboard()
print(leaderboard[['model_type', 'metric_value', 'train_time']])
