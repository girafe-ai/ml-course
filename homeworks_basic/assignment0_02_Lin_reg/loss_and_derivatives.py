import numpy as np


class LossAndDerivatives:
    @staticmethod
    def mse(X, Y, w):
        """
        X : numpy array of shape (`n_observations`, `n_features`)
        Y : numpy array of shape (`n_observations`, `target_dimentionality`)
        w : numpy array of shape (`n_features`, `target_dimentionality`)

        Return : float
            single number with MSE value of linear model (X.dot(w)) with no bias term
            on the selected dataset.
        
        Comment: If Y is two-dimentional, average the error over both dimentions.
        """

        return np.mean((X.dot(w) - Y)**2)

    @staticmethod
    def mae(X, Y, w):
        """
        X : numpy array of shape (`n_observations`, `n_features`)
        Y : numpy array of shape (`n_observations`, `target_dimentionality`)
        w : numpy array of shape (`n_features`, `target_dimentionality`)
                
        Return: float
            single number with MAE value of linear model (X.dot(w)) with no bias term
            on the selected dataset.

        Comment: If Y is two-dimentional, average the error over both dimentions.
        """

        # YOUR CODE HERE    
        return 

    @staticmethod
    def l2_reg(w):
        """
        w : numpy array of shape (`n_features`, `target_dimentionality`)

        Return: float
            single number with L2 norm of the weight matrix

        Computes the L2 regularization term for the weight matrix w.
        """
        
        # YOUR CODE HERE
        return 

    @staticmethod
    def l1_reg(w):
        """
        w : numpy array of shape (`n_features`, `target_dimentionality`)

        Return : float
            single number with L1 norm of the weight matrix
        
        Computes the L1 regularization term for the weight matrix w.
        """

        # YOUR CODE HERE
        return 

    @staticmethod
    def no_reg(w):
        """
        Simply ignores the regularization
        """
        return np.zeros_like(w)
    
    @staticmethod
    def mse_derivative(X, Y, w):
        """
        X : numpy array of shape (`n_observations`, `n_features`)
        Y : numpy array of shape (`n_observations`, `target_dimentionality`)
        w : numpy array of shape (`n_features`, `target_dimentionality`)
        
        Return : numpy array of shape (`n_features`, `target_dimentionality`)

        Computes the MSE derivative for linear regression (X.dot(w)) with no bias term
        w.r.t. w weight matrix.
        """

        # YOUR CODE HERE
        return 

    @staticmethod
    def mae_derivative(X, Y, w):
        """
        X : numpy array of shape (`n_observations`, `n_features`)
        Y : numpy array of shape (`n_observations`, `target_dimentionality`)
        w : numpy array of shape (`n_features`, `target_dimentionality`)
        
        Return : numpy array of shape (`n_features`, `target_dimentionality`)

        Computes the MAE derivative for linear regression (X.dot(w)) with no bias term
        w.r.t. w weight matrix.
        """

        # YOUR CODE HERE
        return 

    @staticmethod
    def l2_reg_derivative(w):
        """
        w : numpy array of shape (`n_features`, `target_dimentionality`)

        Return : numpy array of shape (`n_features`, `target_dimentionality`)

        Computes the L2 regularization term derivative w.r.t. the weight matrix w.
        """

        # YOUR CODE HERE
        return 

    @staticmethod
    def l1_reg_derivative(w):
        """
        w : numpy array of shape (`n_features`, `target_dimentionality`)

        Return : numpy array of shape (`n_features`, `target_dimentionality`)

        Computes the L1 regularization term derivative w.r.t. the weight matrix w.
        """

        # YOUR CODE HERE
        return 

    @staticmethod
    def no_reg_derivative(w):
        """
        Simply ignores the derivative
        """
        return np.zeros_like(w)
