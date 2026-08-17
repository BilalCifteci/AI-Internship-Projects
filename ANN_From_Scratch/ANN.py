import numpy as np


class ANN:

    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):

     np.random.seed(1)

     self.input_size = input_size
     self.hidden_size = hidden_size
     self.output_size = output_size
     self.learning_rate = learning_rate

     self.W1 = np.random.randn(hidden_size, input_size) * 0.01
     self.b1 = np.zeros((hidden_size, 1))

     self.W2 = np.random.randn(output_size, hidden_size) * 0.01
     self.b2 = np.zeros((output_size, 1))

    def relu(self, z):
        return np.maximum(0, z)


    def relu_derivative(self, z):
        return (z > 0).astype(float)


    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))


    def forward(self, X):

        self.Z1 = np.dot(self.W1, X) + self.b1
        self.A1 = self.relu(self.Z1)

        self.Z2 = np.dot(self.W2, self.A1) + self.b2
        self.A2 = self.sigmoid(self.Z2)

        return self.A2


    def loss(self, Y, prediction):

        m = Y.shape[1]

        epsilon = 1e-8

        cost = -(1 / m) * np.sum(
            Y * np.log(prediction + epsilon)
            +
            (1 - Y) * np.log(1 - prediction + epsilon)
        )

        return cost


    def backward(self, X, Y):

        m = X.shape[1]

        # Output layer
        dZ2 = self.A2 - Y

        dW2 = (1 / m) * np.dot(dZ2, self.A1.T)

        db2 = (1 / m) * np.sum(
            dZ2,
            axis=1,
            keepdims=True
        )

        # Hidden layer
        dA1 = np.dot(self.W2.T, dZ2)

        dZ1 = dA1 * self.relu_derivative(self.Z1)

        dW1 = (1 / m) * np.dot(dZ1, X.T)

        db1 = (1 / m) * np.sum(
            dZ1,
            axis=1,
            keepdims=True
        )

        # Gradient descent
        self.W1 = self.W1 - self.learning_rate * dW1
        self.b1 = self.b1 - self.learning_rate * db1

        self.W2 = self.W2 - self.learning_rate * dW2
        self.b2 = self.b2 - self.learning_rate * db2
    def train(self, X, Y, epochs=2000):

     for epoch in range(epochs):

        prediction = self.forward(X)

        cost = self.loss(Y, prediction)

        self.backward(X, Y)

        if epoch % 100 == 0:
            print("Epoch:", epoch, "Loss:", cost)
    def predict(self, X):

     probabilities = self.forward(X)

     predictions = (probabilities >= 0.5).astype(int)

     return predictions


X = np.array([
    [0, 0, 1, 1],
    [0, 1, 0, 1]
])

Y = np.array([
    [0, 1, 1, 1]
])

model = ANN(
    input_size=2,
    hidden_size=4,
    output_size=1,
    learning_rate=0.1
)

model.train(X, Y, epochs=2000)

output = model.forward(X)

print("\nFinal probabilities:")
print(output)

predictions = model.predict(X)

print("\nPredictions:")
print(predictions)

print("\nReal values:")
print(Y)