import joblib
from sklearn.linear_model import LogisticRegression

# Example training data
# [repeated_401, total_requests, unknown_paths]

X = [
    [0, 10, 0],   # normal traffic
    [5, 20, 6],   # suspicious traffic
]

y = [0, 1]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "app/ml/model.pkl")

print("Model trained and saved.")