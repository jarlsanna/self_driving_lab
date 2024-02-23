import numpy as np
import system_parameters as sp

# campaign code
CAMP_CODE = "BaZrSn_001"
CAMP_DESC = "Sputter setup with Ba, Zr and Sn for development of BEA supervisor"

# these arrays are defined based on the three power variables in the parameter space, 1-3
# e.g. in MATERIALS, the first entry in the list is associated with power axis 1, the second entry with power axis 2, etc.
# we are unlikely to ever have more than 3 power axes
MATERIALS = ["Ba", "Zr", "Sn"]  # chemical names of material on each power axis
# which magnetron are being used for the powers/materials
MAGNETRONS = [5, 1, 3]
POWER_SUPPLIES = np.array([5, 1, 3])  # the power supplies responsible
MAX_POWERS = [120, 120, 70]  # upper limit of the respective power axis
RAMP_RATES = [5, 10, 10]  # we should implement these settings
# we should implement these settings (-1 corresponds to RF; we should not try to add a frequency to an RF supply)
PULSE_FREQUENCIES = ["RF", "50", "50"]
# power, power, power, pressure, values which are in place after ignition and pressure regulation
PRESPUTT_PARAMS = [50, 50, 35, 5]
# voltages which are found for the above conditions after run-in of a SINGLE target, with target shutters open. With several targets the values are slightly different.
PRESPUTT_VS = [77, 242, 315]
SPUTTER_GAS = "Ar"

# PARAMETERS TO BE EVALUTED AND FIXED FOR CAMPAIGN AND OR SYSTEM
RECORDING_INTERVAL_SAMPLE = 1
RECORDING_INTERVAL_NO_SAMPLE = 0.1
RECORDING_TIME = 10
PRESPUTT_TIME = 30  # seconds
PRE_SPUTT_V_ERROR = 3  # %
PWA_READ_WAIT_TIME = 0.2  # s
PWA_SET_WAIT_TIME = 0.5  # s
BLUE_FLASH_REPEATS = 10
BLUE_FLASH_WAIT = 0.1  # s
WAIT_RECIPE_ITERATIONS = 20
WAIT_RECIPE_TIME = 5  # s
GAS_INJ_TOGGLE_TIME = 2  # s
POWER_PADDING = 5  # W
POWER_PADDING_WAIT = 2  # s

CAMPAIGN_METADATA = {
    "Campaign code": CAMP_CODE,  # taken from some function
    "Campaign description": CAMP_DESC,
    "Material Ax1": MATERIALS[0],
    "Material Ax2": MATERIALS[1],
    "Material Ax3": MATERIALS[2],
    "Magnetron Ax1": MAGNETRONS[0],
    "Magnetron Ax2": MAGNETRONS[1],
    "Magnetron Ax3": MAGNETRONS[2],
    "Power Supply Ax1": int(POWER_SUPPLIES[0]),
    "Power Supply Ax2": int(POWER_SUPPLIES[1]),
    "Power Supply Ax3": int(POWER_SUPPLIES[2]),
    "Power Supply Ax1 Ramp Rate [W/s]": RAMP_RATES[0],
    "Power Supply Ax2 Ramp Rate [W/s]": RAMP_RATES[1],
    "Power Supply Ax3 Ramp Rate [W/s]": RAMP_RATES[2],
    "Power Supply Ax1 Pulse Rate [kHz or RF]": PULSE_FREQUENCIES[0],
    "Power Supply Ax2 Pulse Rate [kHz or RF]": PULSE_FREQUENCIES[1],
    "Power Supply Ax3 Pulse Rate [kHz or RF]": PULSE_FREQUENCIES[2],
    "Sputter gas": SPUTTER_GAS
}

# parameters to record in time series, with Eklipse names and our preferred names
RECORDING_NAMES = {
    sp.PS_READ_POWER_SIGNALS[POWER_SUPPLIES[0]-1]: "Actual_Power_Ax1_[W]",
    sp.PS_READ_VOLTAGE_SIGNALS[POWER_SUPPLIES[0]-1]: "Voltage_Ax1_[V]",
    sp.PS_READ_POWER_SIGNALS[POWER_SUPPLIES[1]-1]: "Actual_Power_Ax2_[W]",
    sp.PS_READ_VOLTAGE_SIGNALS[POWER_SUPPLIES[1]-1]: "Voltage_Ax2_[V]",
    sp.PS_READ_POWER_SIGNALS[POWER_SUPPLIES[2]-1]: "Actual_Power_Ax3_[W]",
    sp.PS_READ_VOLTAGE_SIGNALS[POWER_SUPPLIES[2]-1]: "Voltage_Ax3_[V]"

}
