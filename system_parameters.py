# Parameters to edit
SET_SPUTTER_PRESSURE = "PC Capman Pressure Setpoint"
SET_VALVE_POS = "PC High Vac Valve Position Setpoint"
SET_FLOW_RATE = "PC MFC 1 Setpoint"

# power supply information:
# these arrays are defined for the power supplies 1-6 - they would never change and can go to "Sputtering parameters"
# which recipes are used to ignite the poewr supplies
PS_IGNITION_RECIPES = ["Ignite Source 1", "Ignite Source 2",
                       "Ignite Source 3", "Ignite Source 4", "Ignite Source 5", "Ignite Source 6"]
# which power supply setpoints signals are used for each supply
PS_SET_OUTPUT_SIGNALS = ["Power Supply 1 Output Setpoint", "Power Supply 2 Output Setpoint", "Power Supply 3 Output Setpoint",
                         "Power Supply 4 Output Setpoint", "Power Supply 5 Output Setpoint", "Power Supply 6 Output Setpoint"]
# which signals are used for checking power supply status
PS_STATUS_SIGNALS = ["Power Supply 1 Enabled", "Power Supply 2 Enabled", "Power Supply 3 Enabled",
                     "Power Supply 4 Enabled", "Power Supply 5 Enabled", "Power Supply 6 Enabled"]
# which signals are used to read the power outputs
PS_READ_POWER_SIGNALS = ["Power Supply 1 Power", "Power Supply 2 Power", "Power Supply 3 Power",
                         "Power Supply 4 Power", "Power Supply 5 Fwd Power", "Power Supply 6 Fwd Power"]
# which signals are used to read the voltage outputs
PS_READ_VOLTAGE_SIGNALS = ["Power Supply 1 Voltage", "Power Supply 2 Voltage", "Power Supply 3 Voltage",
                           "Power Supply 4 Voltage", "Power Supply 5 DC Bias", "Power Supply 6 DC Bias"]
# which type (DC/RF) the power supplies are
PS_TYPES = ["DC", "DC", "DC", "DC", "RF", "RF"]

# some other parameters to read
ACT_FLOW_RATE = "PC MFC 1 Flow"


# parameters to record as metadata
BASE_PRESSURE = "PC Wide Range Gauge"

# parameters to record in time series, with Eklipse names and our preferred names
BASIC_PARAMETERS_TS = {
    "PC Capman Pressure": "Actual_pressure_[mTorr]",
    "PC Source 2 Freq": "QCM_1_frequency_[Hz]",
    "PC Source 4 Freq": "QCM_2_frequency_[Hz]",
    "PC Source 6 Freq": "QCM_3_frequency_[Hz]",
    "PC MFC 1 Flow": "Gas_flow_[sccm]"
}
# name of the basic recording set contining the above
BASIC_PARAMETER_SET = "automation_basic_parameters"


# allowed combinations of pressure and valve positions for upstream presure control
valve_position_1 = 55
valve_position_2 = 36
valve_position_3 = 15
pressure_lower_1 = 1
pressure_upper_1 = 3
pressure_lower_2 = 4
pressure_upper_2 = 14
pressure_lower_3 = 15
pressure_upper_3 = 50

# Discrete parameters
Check_GasInjValveOpen = "PC Gas Injection Valve Open"
Check_GasIsoValveOpen = "PC MFC 1 Iso Valve Open"
Check_ShutterOpen = "PC Substrate Shutter Open"
Check_StackLight_Blue = "StackLightBlue"
Check_StackLight_Green = "StackLightGreen"
Check_StackLight_Red = "StackLightRed"
Check_StackLight_Yellow = "StackLightYellow"

# Window parameters
EKLIPSE_MAIN_WINDOW_NAME = "Kurt J Lesker Company eKLipse Version: 20220224.3.0.149"
AUTOMATION_TAB_ID = "Automation"
LOGIN_USER_NAME_ID = "LogInUsername"
LOGIN_PASSWORD_ID = "LogInPassword"
LOGIN_BUTTON_ID = "LogInButton"
CHOOSE_SIGNAL_BOX_ID = "SelectedSignal"
PANEL_SIGNAL_SETTINGS_WINDOW_ID = "PanelSignalSettingsVisibility"
READ_SIGNAL_ACTUAL_VALUE_BOX_HANDLE = "Edit8"
REQUEST_EDIT_BOX_ID = "Request"

# Other parameters
EKLIPSE_LOGIN_USER_NAME = "KJLC"
EKLIPSE_LOGIN_PASSWORD = "1515"
STACK_LIGHT_RED = "RED"
STACK_LIGHT_YELLOW = "YELLOW"
STACK_LIGHT_GREEN = "GREEN"
STACK_LIGHT_GREEN_STEADY_BLUE = "GREEN steady BLUE"
STACK_LIGHT_GREEN_FLASH_BLUE = "GREEN flashing BLUE"
STACK_LIGHT_UNDEFINED = "UNDEFINED"

# Preset Recipes auto_ids
RECIPE_VENTLL = "Vent Load Lock"
RECIPE_PUMPLL = "Pump Load Lock"
RECIPE_LOAD = "Load Sample"
RECIPE_UNLOAD = "Unload Sample"
RECIPE_PREPARE = "Prep for Sputtering"
RECIPE_SPUTTER_SAMPLE = "Sputter (Sample)"
RECIPE_SPUTTER_NO_SAMPLE = "Sputter (no Sample)"
RECIPE_END_PROCESS = "End Process"

MAIN_RECIPE_NAME_NO_SAMPLE = "MX Master - Proceed (no"
MAIN_RECIPE_NAME_SAMPLE = "MX Master - Proceed (with"
MAIN_RECIPE_DWELL_STEP_SAMPLE = 5
MAIN_RECIPE_DWELL_STEP_NO_SAMPLE = 4

MAX_PARAM = 150
MAX_RECORDING_TIME = 60
