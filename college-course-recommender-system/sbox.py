import numpy as np

def custom_normalized_sigmoid_function(value, tuning_constant):
    return 1 - np.exp(-tuning_constant * value)

print(str(custom_normalized_sigmoid_function(0.5, 1.0)))