import numpy as np

class LaplaceDistribution:    
    @staticmethod
    def mean_abs_deviation_from_median(x: np.ndarray):
        '''
        Args:
        - x: A numpy array of shape (n_objects, n_features) containing the data
          consisting of num_train samples each of dimension D.
        '''
        ####
        # Do not change the class outside of this block
        # Your code here
        median = np.median(x, axis=0)  # Находим медиану для каждой фичи
        deviation = np.abs(x - median)  # Находим абсолютное отклонение от медианы
        mean_deviation = np.mean(deviation, axis=0)  # Находим среднее абсолютное отклонение
        return mean_deviation
        ####

    def __init__(self, features):
        '''
        Args:
            feature: A numpy array of shape (n_objects, n_features). Every column represents all available values for the selected feature.
        '''
        ####
        # Do not change the class outside of this block
        self.loc = loc # YOUR CODE HERE
        self.scale = scale # YOUR CODE HERE
        ####


    def logpdf(self, values):
        '''
        Returns logarithm of probability density at every input value.
        Args:
            values: A numpy array of shape (n_objects, n_features). Every column represents all available values for the selected feature.
        '''
        ####
        # Do not change the class outside of this block
        exponent = -np.abs(values - self.loc) / self.scale
        log_density = -np.log(2 * self.scale) + exponent
        return log_density

        ####
        
    
    def pdf(self, values):
        '''
        Returns probability density at every input value.
        Args:
            values: A numpy array of shape (n_objects, n_features). Every column represents all available values for the selected feature.
        '''
        return np.exp(self.logpdf(value))
