import os
import pandas as pd
import numpy as np
from qplot import qp, qplot
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS

os.environ['NIXTLA_ID_AS_COL'] = 'True'

# -------------------------------------------------------------------------------------------

def gaussian_noise (y, block_size=50):
    noise = np.zeros_like(y)  # Initialize a noise array of zeros
    num_blocks = len(y) // block_size  # Calculate the number of complete blocks

    for i in range(num_blocks + 1):  # Include a partial block if any
        start_idx = i * block_size
        end_idx = start_idx + block_size
        if i % 2 == 0:  # Apply noise to even indexed blocks
            noise[start_idx:end_idx] = np.random.normal(
                0, 12, min(block_size, len(y) - start_idx)
            )

    return y + noise

# -------------------------------------------------------------------------------------------

def generate_function(x, a=0.1, b=10, c=2 * np.pi / 10, frequency_trend=None):
    """
    Generates values for a function that includes a linear trend and a cosine wave.
    The frequency of the cosine wave can increase or decrease linearly with x.

    Parameters:
        x (array-like): Array of x values.
        a (float): Coefficient for the linear trend.
        b (float): Amplitude of the cosine wave.
        c (float): Base frequency of the cosine wave.
        frequency_trend (str or None): 
            If 'increase', the frequency of the cosine wave increases linearly with x.
            If 'decrease', the frequency of the cosine wave decreases linearly with x.
            If None, the frequency remains constant.

    Returns:
        np.array: Array of y values corresponding to each x.
    """
    k = 0.003  # Adjust the constant k as needed to control the rate of frequency change

    if frequency_trend == 'increase':
        c_scaled = c * (1 + k * x)
    elif frequency_trend == 'decrease':
        c_scaled = c / (1 + k * x)
    else:
        c_scaled = c

    y = a * x + b * np.cos(c_scaled * x)
    
    return y

# -------------------------------------------------------------------------------------------

# Returns mean squared error
def calculate_error (original_data, prediction):
    return (np.round (np.mean ((original_data - prediction) ** 2), 3))

# -------------------------------------------------------------------------------------------

x_values = np.linspace(0, 1000, 3000)

# Level 1
level1 = generate_function (x_values)

# Level 2
level2 = generate_function (x_values, frequency_trend = "decrease")

# Level 3
level3 = gaussian_noise (level1)

# Level4
level4 = gaussian_noise (level2)

qp(level1[0:600], level2[0:600], level3[0:600], level4[0:600], colors=["r", "g", "b"])

# Level 1: Data to pandas
train = level1[:-300]
test = level1[-300:]
df = pd.DataFrame ({
    'unique_id': 'series_1',
    'ds': pd.date_range (start='2023-01-01', periods = len (train), freq='D'),
    'y': train
})

# # Apply AutoArima
# sf = StatsForecast (models = [AutoARIMA (season_length = 10, d = 1)], freq='D') # Not optimal params
# sf.fit(df)
# forecast = sf.predict(h=300, level=[95])["AutoARIMA"].to_numpy()

# Put different methods here :-)
# Use methods from this url https://nixtlaverse.nixtla.io for docs about the libraries used
# AutoARIMA: https://nixtlaverse.nixtla.io/statsforecast/src/core/models.html

new_sf = StatsForecast(models=[AutoETS(season_length=10)], freq='D')
new_sf.fit(df)
forecast = new_sf.predict(h=300, level=[95])["AutoETS"].to_numpy()

# Plot end of train (last 600 values) and prediction then display error
qp (train[-600:], forecast, styles=["-", "a"], colors = ["b", "r"], where = [0, 0])
print ("MSE for AutoArima on Level1: ", calculate_error (test, forecast))