import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from features import build_features

def train():
    df = build_features()

    feature_cols = ['fg_pct_home', 'fg_pct_away',
                 'ft_pct_home', 'ft_pct_away', 'fg3_pct_home', 'fg3_pct_away',
                 'ast_home', 'ast_away', 'reb_home', 'reb_away', 'tov_home', 'tov_away']

    X = df[feature_cols]
    y = df['home_win']

    # TODO: split X and y into training and testing sets
    # hint: train_test_split(X, y, test_size=0.2)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # TODO: create a LogisticRegression model and fit it on the training data
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # TODO: use the trained model to predict on the test data
    predictions = model.predict(X_test)

    # TODO: compare predictions to actual y_test values using accuracy_score
    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy}")
    return(accuracy)

if __name__ == "__main__":
    train()