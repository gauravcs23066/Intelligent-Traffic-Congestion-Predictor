import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Sample Data
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
Y = np.array([2, 4, 5, 4, 5])

print("Original Dataset:")
print(f"X: {X.flatten()}")
print(f"Y: {Y}\n")

# Create Model
model = LinearRegression()

# Train Model
model.fit(X, Y)

# Predict on training data
Y_pred_train = model.predict(X)

# Plot original regression
plt.figure(figsize=(10, 6))
plt.scatter(X, Y, color='blue', label='Actual Data')
plt.plot(X, Y_pred_train, color='red', label='Regression Line')
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Linear Regression (Original Data)")
plt.legend()
plt.grid(True)
plt.show()

# Calculate Error Metrics for original model
mse_original = mean_squared_error(Y, Y_pred_train)
mae_original = mean_absolute_error(Y, Y_pred_train)

print(f"\nError Metrics for Original Model:")
print(f"Mean Squared Error (MSE): {mse_original:.2f}")
print(f"Mean Absolute Error (MAE): {mae_original:.2f}")

# Predict new values
X_new = np.array([0, 6, 7]).reshape(-1, 1)
Y_pred_new = model.predict(X_new)

print(f"\nPredictions for new values (X = {X_new.flatten()}):")
for i in range(len(X_new)):
    print(f"X = {X_new[i][0]}, Predicted Y = {Y_pred_new[i]:.2f}")