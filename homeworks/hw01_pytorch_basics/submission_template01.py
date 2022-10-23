import numpy as np
import torch
from torch import nn

def create_model():
    simple_nn = nn.ReLU(784, 256, 16, 10, bias=False)
    medium_model = nn.Sequential(*[nn.Linear(784, 32, bias=False), nn.ReLU(), nn.Linear(32, 10, bias=False)])
    return simple_nn 
def count_parameters(model):
    param = model.parameters()
    return param
    
    return None
    
