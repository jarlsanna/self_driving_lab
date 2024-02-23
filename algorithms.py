import random
import campaign_parameters as cp
import system_parameters as sp
import numpy as np

pressure_min = sp.pressure_lower_1
pressure_max = sp.pressure_upper_3
power_min = 15
power1_max = cp.MAX_POWERS[0] - 50
power2_max = cp.MAX_POWERS[1] - 50
power3_max = cp.MAX_POWERS[2] - 20

recording_time = 10


def generate_random_parameters(power_axes: np.array):
    new_pressure = random.randint(pressure_min, pressure_max)
    new_power1 = random.randint(power_min, power1_max)
    new_power2 = random.randint(power_min, power2_max)
    new_power3 = random.randint(power_min, power3_max)

    # modified to only return values on the active axes (because power values for the unused magnetrons were being stored in the database!)
    parameters = [[new_power1, new_power2,
                   new_power3, new_pressure, recording_time]]
    for k in range(3):
        if not power_axes[k]:
            parameters[0][k] = 0

    return parameters
