from pywinauto.application import Application, WindowSpecification
from pywinauto import Desktop
import time
import os
import system_parameters as sp
import campaign_parameters as cp
import validate as vd

path = r"C:\\Program Files (x86)\\KJLC\\eKLipse"
os.chdir(path)
BACKEND = "uia"  # uia or win32
EKLIPSE_WINDOW_NAME = "Kurt J Lesker Company eKLipse Version: 20220224.3.0.149"


def start_eklipse() -> WindowSpecification:
    '''Starts the eklipse application

    Returns
    -------
    WindowSpecification
        Connected application window
    '''

    eklipse_instance = Application(backend=BACKEND).start("eKlipse.exe")
    time.sleep(20)
    eklipse_window = eklipse_instance.window(title=EKLIPSE_WINDOW_NAME)
    # main_window = timings.wait_until_passes(20, 0.5, lambda: eklipse_instance.window(title=EKLIPSE_WINDOW_NAME))
    return eklipse_window


def logInToEklipse(eklipse_window: WindowSpecification) -> None:
    '''Login to Eklipse

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    '''
    # first, check if already logged in (usually is)
    print("    checking login status...")
    try:
        login_panel = eklipse_window.child_window(auto_id="LogInPanel")
        if login_panel.exists() and login_panel.is_visible():
            eklipse_window.child_window(
                auto_id="LogInUsername").set_text('KJLC')
            eklipse_window.child_window(
                auto_id="LogInPassword").set_text('1515')
            eklipse_window.child_window(auto_id="LogInButton").click()
            print("    logged in")
        else:
            print("    Already logged in")

    except:
        print("    Already logged in")


def connect_to_instance_of_eklipse() -> WindowSpecification:
    '''Connect to the running application

    Returns
    -------
    WindowSpecification
        Connected application window
    '''

    eklipse_instance = Application().connect(path="eKlipse.exe")
    time.sleep(10)
    eklipse_instance.window(title=EKLIPSE_WINDOW_NAME).maximize().set_focus()
    eklipse_window = eklipse_instance.window(title=EKLIPSE_WINDOW_NAME)
    return eklipse_window


def is_application_connected(eklipse_window) -> bool:
    '''Check if connected to the application

    Parameters
    ----------
    eklipse_window : _type_
        Application window

    Returns
    -------
    bool
        If connected
    '''

    if eklipse_window.exists() and eklipse_window.is_visible():
        print("    Eklipse is connected")
        return True
    else:
        print("    Eklipse not connected")
        return False


def go_to_automation_tab(eklipse_window: WindowSpecification) -> None:
    '''Go to the automation tab in Eklipse

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    '''
    eklipse_window.wrapper_object().set_focus()
    eklipse_window.child_window(
        title="Automation", auto_id="Automation").click()
    go_to_io_item_editor_tab(eklipse_window)


def go_to_io_item_editor_tab(eklipse_window: WindowSpecification) -> None:
    '''<go to item editor tab in Eklipse

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    '''
    eklipse_window.wrapper_object().set_focus()
    eklipse_window.child_window(
        title="IO Item Editor", auto_id="IO Item Editor").click()


def check_running_recipe_name(eklipse_window: WindowSpecification) -> str:
    '''Check the name of running recipe

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state

    Returns
    -------
    str
        Name of recipe
    '''
    # go_to_automation_tab(eklipse_window)
    eklipse_window.wrapper_object().set_focus()
    eklipse_window.child_window(auto_id="Monitor").click()
    desktop = Desktop(BACKEND)
    recipe_monitor = desktop.window(auto_id="RecipeMonitor")
    if recipe_monitor.exists:
        field = recipe_monitor.child_window(
            auto_id="NameOfRecipe").wrapper_object()
        recipe_name = field.get_value()
        print("    Detected recipe name: " +
              recipe_name + " in Recipe Monitor window")
        return recipe_name
    else:
        print("    Could not read recipe monitor")
        return "False"


def check_running_recipe_step(eklipse_window: WindowSpecification) -> int:
    '''Check what step the recipe is at

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state

    Returns
    -------
    int
        Current recip step
    '''
    # go_to_automation_tab(eklipse_window)
    eklipse_window.wrapper_object().set_focus()
    eklipse_window.child_window(auto_id="Monitor").click()
    desktop = Desktop(BACKEND)
    recipe_monitor = desktop.window(auto_id="RecipeMonitor")
    if recipe_monitor.exists:
        field = recipe_monitor.child_window(
            auto_id="StepNumber").wrapper_object()
        step_number = int(field.get_value())
        print("    Recipe at step " + str(step_number))
        return step_number
    else:
        print("    Could not read recipe step")
        return -1


def resume_paused_recipe(eklipse_window: WindowSpecification) -> bool:
    '''Resume paused recipe

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state

    Returns
    -------
    bool
        If resumed
    '''
    # go_to_automation_tab(eklipse_window)
    eklipse_window.wrapper_object().set_focus()
    eklipse_window.child_window(auto_id="Monitor").click()
    desktop = Desktop(BACKEND)
    recipe_monitor = desktop.window(auto_id="RecipeMonitor")
    if recipe_monitor.exists:
        recipe_monitor.child_window(auto_id="ResumeRecipe").click()
        print("    Recipe resumed")
        return True
    else:
        print("    Could not resume paused recipe")
        return False


def skip_recipe_step(eklipse_window: WindowSpecification) -> bool:
    '''Skip step in recipe

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state

    Returns
    -------
    bool
        Step skipped
    '''
    # go_to_automation_tab(eklipse_window)
    eklipse_window.wrapper_object().set_focus()
    eklipse_window.child_window(auto_id="Monitor").click()
    desktop = Desktop(BACKEND)
    recipe_monitor = desktop.window(auto_id="RecipeMonitor")
    if recipe_monitor.exists:
        recipe_monitor.child_window(auto_id="SkipRecipeStep").click()
        print("    Recipe step skipped")
        return True
    else:
        print("    Could not skip recipe step")
        return False


def setup_data_recording(eklipse_window: WindowSpecification, samples: bool) -> None:
    '''Configure data recording, such as what signals to record 

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    samples : bool
        If have samples
    '''
    if samples:
        interval = cp.RECORDING_INTERVAL_SAMPLE
    else:
        interval = cp.RECORDING_INTERVAL_NO_SAMPLE

    go_to_automation_tab(eklipse_window)
    eklipse_window.child_window(auto_id="Recording Setup").click()
    time.sleep(1)
    eklipse_window.child_window(auto_id="RemoveAll").click()
    eklipse_window.child_window(
        auto_id="ListViewSavedSets").select(sp.BASIC_PARAMETER_SET)
    eklipse_window.child_window(auto_id="cmdUseSelectedSet").click()

    for power_supply in cp.POWER_SUPPLIES:
        P = sp.PS_READ_POWER_SIGNALS[power_supply-1]
        V = sp.PS_READ_VOLTAGE_SIGNALS[power_supply-1]
        eklipse_window.child_window(
            auto_id="ListBoxAvailableSignals").select(P)
        # time.sleep(cp.PWA_SET_WAIT_TIME)
        eklipse_window.child_window(auto_id="Add").click()
        eklipse_window.child_window(
            auto_id="ListBoxAvailableSignals").select(V)
        # time.sleep(cp.PWA_SET_WAIT_TIME)
        eklipse_window.child_window(auto_id="Add").click()

    eklipse_window.child_window(auto_id="RecordingInterval").type_keys(
        str(interval))  # + "{ENTER}")
    eklipse_window.child_window(auto_id="Generate").click()
    desktop = Desktop(BACKEND)
    popup_window = desktop.window(auto_id="eKLipseSmallMSGBOX")
    popup_window.type_keys("{ENTER}")
    go_to_io_item_editor_tab(eklipse_window)


def read_parameter(eklipse_window: WindowSpecification, signal_name: str) -> str:
    '''Reading the value of parameters

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    signal_name : str
        Signal to read

    Returns
    -------
    str
        Signal value
    '''
    go_to_automation_tab(eklipse_window)
    try:
        # select wanted signal
        eklipse_window.child_window(
            auto_id=sp.CHOOSE_SIGNAL_BOX_ID).select(signal_name)
        time.sleep(cp.PWA_READ_WAIT_TIME)
        # read the value
        value = eklipse_window.child_window(auto_id="Actual").window_text()
        # print("read_parameter() returned " + value + " for " + signal_name)
        return value
    except Exception as e:
        print("    Could not read parameter value: ", type(e).__name__)
        return "Failed to read value"


def set_parameter(eklipse_window: WindowSpecification, new_value: int, signal_name: str) -> bool:
    '''Set value of specified signal

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    new_value : int
        New value to set
    signal_name : str
        Signal name

    Returns
    -------
    bool
        Value is set
    '''
    go_to_automation_tab(eklipse_window)
    if new_value > sp.MAX_PARAM:
        print("    Requested value in set_parameter was above maximum allowed (" +
              str(sp.MAX_PARAM) + ")")
        return False
    eklipse_window.child_window(
        auto_id=sp.CHOOSE_SIGNAL_BOX_ID).select(signal_name)
    time.sleep(cp.PWA_SET_WAIT_TIME)
    eklipse_window.child_window(
        auto_id=sp.REQUEST_EDIT_BOX_ID).set_edit_text('')
    eklipse_window.child_window(auto_id=sp.REQUEST_EDIT_BOX_ID).type_keys(
        str(new_value) + "{ENTER}")
    verified = verify_parameter(eklipse_window, new_value)
    if verified:
        print("    "+signal_name + " was changed to", new_value)
        return True
    else:
        print("    Change of "+signal_name +
              " could not be verified, setting to zero")
        eklipse_window.child_window(
            auto_id=sp.REQUEST_EDIT_BOX_ID).set_edit_text('')
        eklipse_window.child_window(
            auto_id=sp.REQUEST_EDIT_BOX_ID).type_keys("0" + "{ENTER}")
        return False


def set_power(eklipse_window: WindowSpecification, new_value: int, power_axis: int) -> bool:
    '''Set the power of the source specified

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    new_value : int
        New power
    power_axis : int
        Axis to where apply the power

    Returns
    -------
    bool
        Power applied
    '''

    # this function allows up to 10W extra to be applied to accomodate power padding, but any functions providing power values to BEA supervisor should still respect the MAX_POWERS values.
    power_padding = min(cp.POWER_PADDING, 10)
    power_supply_index = cp.POWER_SUPPLIES[power_axis-1]-1
    if (new_value <= (cp.MAX_POWERS[power_axis-1]+power_padding)):

        go_next = set_parameter(eklipse_window, new_value,
                                sp.PS_SET_OUTPUT_SIGNALS[power_supply_index])

        if go_next:
            print("    Set power " + str(new_value) + " W on " +
                  str(cp.MATERIALS[power_axis-1]) + ", power supply " + str(cp.POWER_SUPPLIES[power_axis-1]))
            return True
        else:
            print("    Failed to set power " + str(new_value) + " W on " +
                  str(cp.MATERIALS[power_axis-1]) + ", power supply " + str(cp.POWER_SUPPLIES[power_axis-1]))
            return False
        # power_supply_index is the index of the power supply in the arrays of power supply information in system_parameters

    else:
        print("    Could not set power value, out of range or other error")
        return False


def set_pressure(eklipse_window: WindowSpecification, new_value: int) -> bool:
    '''Set the capman pressure

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    new_value : int
        New pressure

    Returns
    -------
    bool
        Pressure is set
    '''

    valve_position = sp.valve_position_1
    if (new_value >= sp.pressure_lower_1 and new_value <= sp.pressure_upper_1):
        valve_position = sp.valve_position_1

    elif (new_value >= sp.pressure_lower_2 and new_value <= sp.pressure_upper_2):
        valve_position = sp.valve_position_2

    elif (new_value >= sp.pressure_lower_3 and new_value <= sp.pressure_upper_3):
        valve_position = sp.valve_position_3

    else:
        print("    Requested pressure " + str(new_value) + "mTorr out of range")
        return False
    go_next = set_parameter(eklipse_window, valve_position, sp.SET_VALVE_POS)
    if go_next:
        go_next = set_parameter(
            eklipse_window, new_value, sp.SET_SPUTTER_PRESSURE)
        if go_next:
            return True
    return False


def verify_parameter(eklipse_window: WindowSpecification, new_value: int) -> bool:
    '''Verifies the value got changed, and avoids extreme values

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    new_value : int
        _description_

    Returns
    -------
    bool
        Paramerter is verified
    '''
    value = int(eklipse_window.child_window(
        auto_id=sp.REQUEST_EDIT_BOX_ID).window_text())
    if (value != new_value):
        return False
    else:
        return True


def operate_target_shutter(eklipse_window: WindowSpecification, state: str, power_axis: int):
    '''Open or close a single target shutter

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    state : str
        Open or closed
    power_axis : int
        Which axis the shutter belongs to
    '''
    if (state == "open"):
        ps = sp.POWER_SUPPLIES[power_axis]
        set_parameter(eklipse_window, 1, sp.PS_SHUTTER_OPEN[ps-1])
        print("    PS" + str(ps) + " shutter opened")
    else:
        set_parameter(eklipse_window, 0, sp.PS_SHUTTER_OPEN[ps-1])
        print("    PS" + str(ps) + " shutter closed")


def check_if_system_ready(eklipse_window: WindowSpecification) -> bool:
    '''Checking that a set of signals are switched off, meaning the read value should be 0

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state

    Returns
    -------
    bool
        System is ready
    '''

    go_to_automation_tab(eklipse_window)
    signals = [sp.Check_GasInjValveOpen,
               sp.Check_GasIsoValveOpen] + sp.PS_STATUS_SIGNALS

    def map_status(signal): return int(read_parameter(eklipse_window, signal))
    status = list(map(map_status, signals))

    if (sum(status) > 0):
        print("    Checks indicate a process may be running or paused, not ready")
        return False
    else:
        print("    Checks indicate that no process is currently running or paused, ready")
        return True


def check_stack_light_status(eklipse_window: WindowSpecification, check_blue: bool = True) -> str:
    '''Checking the staus of the stack light. Possible combinations are RED, YELLOW, GREEN, GREEN + steady BLUE, GREEN + flashing BLUE

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    check_blue : bool, optional
        Check for "BLUE" light, by default True

    Returns
    -------
    str
        Stack light status
    '''

    go_to_automation_tab(eklipse_window)
    green_light = int(read_parameter(
        eklipse_window, sp.Check_StackLight_Green)) == 1
    red_light = int(read_parameter(
        eklipse_window, sp.Check_StackLight_Red)) == 1
    yellow_light = int(read_parameter(
        eklipse_window, sp.Check_StackLight_Yellow)) == 1

    if red_light:
        print("    Status is RED (Abort) - check system!")
        return sp.STACK_LIGHT_RED
    elif yellow_light:
        print("    Status is YELLOW (Interlock triggered) - check system!")
        return sp.STACK_LIGHT_YELLOW
    elif green_light:
        if (check_blue):
            eklipse_window.child_window(auto_id=sp.CHOOSE_SIGNAL_BOX_ID).select(
                sp.Check_StackLight_Blue)
            time.sleep(cp.PWA_READ_WAIT_TIME)
            blue_readings = []
            flashes = 0
            for i in range(cp.BLUE_FLASH_REPEATS):
                blue_readings.append(
                    int(eklipse_window.child_window(auto_id="Actual").window_text()))
                if (i > 0):
                    if (blue_readings[i] != blue_readings[i-1]):
                        flashes += 1
                time.sleep(cp.BLUE_FLASH_WAIT)

            # print(blue_readings)
            # print(flashes)

            if (flashes > 1):
                print("    Status is FLASHING BLUE (process running and paused)")
                return sp.STACK_LIGHT_GREEN_FLASH_BLUE
            elif blue_readings[-1] == 1:
                print("    Status is BLUE (process running)")
                return sp.STACK_LIGHT_GREEN_STEADY_BLUE
            elif blue_readings[-1] == 0:
                print("    Status is GREEN (ready)")
                return sp.STACK_LIGHT_GREEN
    else:
        print("    Could not determine system status")
        return sp.STACK_LIGHT_UNDEFINED


def record_data(eklipse_window: WindowSpecification, recording_time: int):
    '''Record data

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Window of running application
    recording_time : int
        Time to record in seconds
    '''
    eklipse_window.wrapper_object().set_focus()
    act_record_time = min(recording_time, sp.MAX_RECORDING_TIME)
    eklipse_window.child_window(auto_id="RecordingButton").click()
    print("Recording data... (recording time: " + str(act_record_time), "s)")
    time.sleep(act_record_time)
    eklipse_window.child_window(auto_id="RecordingButton").click()
    print("Recorded OK")


def record_toggle(eklipse_window: WindowSpecification):
    '''Click on record/stor record button

    Parameters
    ----------
    eklipse_window : WindowSpecification
        Application window in connected state
    '''
    eklipse_window.wrapper_object().set_focus()
    eklipse_window.child_window(auto_id="RecordingButton").click()
