from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
import pickle

class DecisionTreeModel:
    def __init__(self, max_depth=None, min_samples_split=2, random_state=42):
        """
        Initialize the Decision Tree Model with hyperparameters.
        :param max_depth: The maximum depth of the tree (None means nodes are expanded until all leaves are pure).
        :param min_samples_split: The minimum number of samples required to split an internal node.
        :param random_state: The seed for the random number generator for reproducibility.
        """
        self.model = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=random_state
        )

    def train(self, X_train, y_train):
        """
        Train the Decision Tree model on the provided data.
        :param X_train: Features for training
        :param y_train: Labels for training
        """
        self.model.fit(X_train, y_train)

    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on the test set.
        :param X_test: Features for testing
        :param y_test: True labels for testing
        :return: Accuracy score and classification report
        """
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        
        return accuracy, report

    def predict(self, X):
        """
        Make predictions with the trained model.
        :param X: Features for making predictions
        :return: Predicted labels
        """
        return self.model.predict(X)

    def save_model(self, file_path):
        """
        Save the trained model to a file.
        :param file_path: Path to the file where the model should be saved
        """
        with open(file_path, 'wb') as model_file:
            pickle.dump(self.model, model_file)

    def load_model(self, file_path):
        """
        Load a trained model from a file.
        :param file_path: Path to the file where the model is saved
        """
        with open(file_path, 'rb') as model_file:
            self.model = pickle.load(model_file)
