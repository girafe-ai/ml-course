import numpy as np
from sklearn.base import BaseEstimator

def entropy(y):
    # Ваш код здесь
    pass

def gini(y):
    # Ваш код здесь
    pass

def variance(y):
    # Ваш код здесь
    pass

def mad_median(y):
    # Ваш код здесь
    pass


class DecisionTree(BaseEstimator):
    
    def __init__(self, max_depth=np.inf, min_samples_split=2, 
                 criterion='gini', debug=False):
        # Ваш код здесь
        pass
    
    def fit(self, X, y):
        # Ваш код здесь
        pass
        
    def predict(self, X):
        # Ваш код здесь
        pass
        
    def predict_proba(self, X):
        # Ваш код здесь
        pass
    