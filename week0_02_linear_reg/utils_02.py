import numpy as np
from matplotlib import pyplot as plt


# Move to utils.py
def visualise(mu, sigma, points, title=None, greater_than_zero=False, log_scale=False):
    if greater_than_zero:
        mu = np.clip(mu, 0, mu.max())
    
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    plt.plot(points, mu, "r", label="mean value")
    _x = np.concatenate((points, points[::-1]))
    _y = np.concatenate((
        [mu[i] - sigma[i] for i in range(len(points))], 
        [mu[i] + sigma[i] for i in range(len(points)-1, -1, -1)],
    ))
    if greater_than_zero:
        _y = np.clip(_y, 0, _y.max())
    plt.fill(_x, _y, fc='r', alpha=.2, ec=None, label='+- sigma range')
    
    if log_scale:
        ax.set_xscale('log')
        
    if title is not None:
        plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.grid()