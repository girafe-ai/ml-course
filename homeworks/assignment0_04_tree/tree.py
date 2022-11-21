import numpy as np
from sklearn.base import BaseEstimator
import time


def entropy(y):  
    """
    Computes entropy of the provided distribution. Use log(value + eps) for numerical stability
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, n_classes)
        One-hot representation of class labels for corresponding subset
    
    Returns
    -------
    float
        Entropy of the provided subset
    """
    EPS = 0.0005

    # YOUR CODE HERE
    p = np.sum(y, axis=0) / len(y) if y.size != 0 else np.array([1])

    return -np.sum(p * np.log(p + EPS)) 
    
def gini(y):
    """
    Computes the Gini impurity of the provided distribution
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, n_classes)
        One-hot representation of class labels for corresponding subset
    
    Returns
    -------
    float
        Gini impurity of the provided subset
    """

    # YOUR CODE HERE
    p = np.sum(y, axis=0) / len(y) if y.size != 0 else np.array([1])
    return 1 - np.sum(p * p)
    
def variance(y):
    """
    Computes the variance the provided target values subset
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, 1)
        Target values vector
    
    Returns
    -------
    float
        Variance of the provided target vector
    """
    
    # YOUR CODE HERE
    
    return 1 / len(y) * np.sum((y - np.mean(y)) ** 2) 

def mad_median(y):
    """
    Computes the mean absolute deviation from the median in the
    provided target values subset
    
    Parameters
    ----------
    y : np.array of type float with shape (n_objects, 1)
        Target values vector
    
    Returns
    -------
    float
        Mean absolute deviation from the median in the provided vector
    """

    # YOUR CODE HERE
    
    return 1 / len(y) * np.sum(np.abs(y - np.mean(y))) 


def one_hot_encode(n_classes, y):
    y_one_hot = np.zeros((len(y), n_classes), dtype=float)
    y_one_hot[np.arange(len(y)), y.astype(int)[:, 0]] = 1.
    return y_one_hot


def one_hot_decode(y_one_hot):
    return y_one_hot.argmax(axis=1)[:, None]


class Node:
    """
    This class is provided "as is" and it is not mandatory to it use in your code.
    """
    def __init__(self, feature_index = None, threshold = None, proba = 0):
        self.feature_index = feature_index
        self.threshold = threshold
        self.value = None
        self.proba = proba
        self.left_child = None
        self.right_child = None
        
        
class DecisionTree(BaseEstimator):
    all_criterions = {
        'gini': (gini, True), # (criterion, classification flag)
        'entropy': (entropy, True),
        'variance': (variance, False),
        'mad_median': (mad_median, False)
    }

    def __init__(self, n_classes=None, max_depth=np.inf, min_samples_split=2, 
                 criterion_name='gini', debug=False):

        assert criterion_name in self.all_criterions.keys(), 'Criterion name must be on of the following: {}'.format(self.all_criterions.keys())
        
        self.n_classes = n_classes
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.criterion_name = criterion_name

        self.depth = 0
        self.root = None # Use the Node class to initialize it later
        self.debug = debug

        
        
    def make_split(self, feature_index, threshold, X_subset, y_subset):
        """
        Makes split of the provided data subset and target values using provided feature and threshold
        
        Parameters
        ----------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels for corresponding subset
        
        Returns
        -------
        (X_left, y_left) : tuple of np.arrays of same type as input X_subset and y_subset
            Part of the providev subset where selected feature x^j < threshold
        (X_right, y_right) : tuple of np.arrays of same type as input X_subset and y_subset
            Part of the providev subset where selected feature x^j >= threshold
        """

        # YOUR CODE HERE
        left_idx = np.where(X_subset[:, feature_index] < threshold)
        right_idx = np.where(X_subset[:, feature_index] >= threshold)

        X_left = X_subset[left_idx]
        y_left = y_subset[left_idx]

        X_right = X_subset[right_idx]
        y_right = y_subset[right_idx]
        
        return (X_left, y_left), (X_right, y_right)
    
    def make_split_only_y(self, feature_index, threshold, X_subset, y_subset):
        """
        Split only target values into two subsets with specified feature and threshold
        
        Parameters
        ----------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels for corresponding subset
        
        Returns
        -------
        y_left : np.array of type float with shape (n_objects_left, n_classes) in classification 
                   (n_objects, 1) in regression 
            Part of the provided subset where selected feature x^j < threshold

        y_right : np.array of type float with shape (n_objects_right, n_classes) in classification 
                   (n_objects, 1) in regression 
            Part of the provided subset where selected feature x^j >= threshold
        """

        # YOUR CODE HERE
        left_idx = np.where(X_subset[:, feature_index] < threshold)
        right_idx = np.where(X_subset[:, feature_index] >= threshold)

        y_left = y_subset[left_idx]
        y_right = y_subset[right_idx]
        
        return y_left, y_right

    def choose_best_split(self, X_subset, y_subset):
        """
        Greedily select the best feature and best threshold w.r.t. selected criterion
        
        Parameters
        ----------
        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels or target values for corresponding subset
        
        Returns
        -------
        feature_index : int
            Index of feature to make split with

        threshold : float
            Threshold value to perform split

        """
        # YOUR CODE HERE

        best_treshold, best_feature_index, best_score = None, None, -1
        n_objects, n_features = X_subset.shape
        H = self.criterion


        for feature_index in range(n_features):
            tresholds = np.unique(X_subset[:, feature_index])
            for treshold in tresholds:
                y_left, y_right = self.make_split_only_y(feature_index, treshold, X_subset, y_subset)
                L, R, Q = len(y_left), len(y_right), len(y_subset)
                score = H(y_subset) - L / Q * H(y_left) - R / Q * H(y_right) if L * R != 0 else 0
                if score > best_score:
                    best_score = score
                    best_treshold, best_feature_index = treshold, feature_index

        return best_feature_index, best_treshold
    
    def make_tree(self, X_subset, y_subset, depth=0):
        """
        Recursively builds the tree
        
        Parameters
        ----------
        X_subset : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the selected subset

        y_subset : np.array of type float with shape (n_objects, n_classes) in classification 
                   (n_objects, 1) in regression 
            One-hot representation of class labels or target values for corresponding subset
        
        Returns
        -------
        root_node : Node class instance
            Node of the root of the fitted tree
        """

        # YOUR CODE HERE

        node = Node()
        
        if depth < self.max_depth and len(y_subset) >= self.min_samples_split and len(np.unique(one_hot_decode(y_subset) if self.classification else y_subset )) != 1:
            node.feature_index, node.threshold = self.choose_best_split(X_subset, y_subset)
            (X_left, y_left), (X_right, y_right) = self.make_split(node.feature_index, node.threshold, X_subset, y_subset)
            node.left_child = self.make_tree(X_left, y_left, depth + 1)
            node.right_child = self.make_tree(X_right, y_right, depth + 1)
        else:
            if self.classification:
                node.value = np.argmax(np.bincount(one_hot_decode(y_subset).flatten()))
                node.proba = np.mean(y_subset, axis=0) 
            else:
                node.value = np.mean(y_subset)


        return node

        
    def fit(self, X, y):
        """
        Fit the model from scratch using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data to train on

        y : np.array of type int with shape (n_objects, 1) in classification 
                   of type float with shape (n_objects, 1) in regression 
            Column vector of class labels in classification or target values in regression
        
        """
        assert len(y.shape) == 2 and len(y) == len(X), 'Wrong y shape'
        self.criterion, self.classification = self.all_criterions[self.criterion_name]
        if self.classification:
            if self.n_classes is None:
                self.n_classes = len(np.unique(y))
            y = one_hot_encode(self.n_classes, y)

        self.root = self.make_tree(X, y)
    
    def _predict(self, x, node = Node()):
        """Predict class for a single sample."""
        if self.classification:
            if isinstance(node.value, np.int64):
                return node.value
        else:
            if isinstance(node.value, np.float64):
                return node.value

        if x[node.feature_index] < node.threshold:
            return self._predict(x, node.left_child)
        return self._predict(x, node.right_child)
        
    def predict(self, X):
        """
        Predict the target value or class label  the model from scratch using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data the predictions should be provided for

        Returns
        -------
        y_predicted : np.array of type int with shape (n_objects, 1) in classification 
                   (n_objects, 1) in regression 
            Column vector of class labels in classification or target values in regression
        
        """
        return np.array([self._predict(x, node=self.root) for x in X])


    def _predict_proba(self, x, node = Node()):
        """Predict probabilities of classes for a single sample."""
        if isinstance(node.value, np.int64):
            return node.proba
        
        
        if x[node.feature_index] < node.threshold:
            return self._predict_proba(x, node.left_child)
        return self._predict_proba(x, node.right_child)

    def predict_proba(self, X):
        """
        Only for classification
        Predict the class probabilities using the provided data
        
        Parameters
        ----------
        X : np.array of type float with shape (n_objects, n_features)
            Feature matrix representing the data the predictions should be provided for

        Returns
        -------
        y_predicted_probs : np.array of type float with shape (n_objects, n_classes)
            Probabilities of each class for the provided objects
        
        """
        assert self.classification, 'Available only for classification problem'

        # YOUR CODE HERE
        
        
        return np.array([self._predict_proba(x, node=self.root) for x in X])
