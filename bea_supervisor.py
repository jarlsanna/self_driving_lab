import time
import os
from pywinauto.application import WindowSpecification
import campaign_parameters as cp
import control_eklipse as ce
import system_parameters as sp
import numpy as np
import validate as vd
import workflow_control as wc
import experiment_series as es
import algorithms

path = r"C:\\Program Files (x86)\\KJLC\\eKLipse"
os.chdir(path)

class BeaSupervisor:
    def __init__(self, power_pad: bool, power_axes: np.array) -> None:
        '''Initialize a BeaSupervisor object

        Parameters
        ----------
        power_pad : bool
            If power padding
        power_axes : np.array
            Array specifying active power axes
        '''
        self.eklipse_window: WindowSpecification
        self.power_pad: bool = power_pad
        self.power_axes: np.array = power_axes

    def start_or_connect_to_eklipse(self):
        '''Start application or connect to running instance.
        '''
        path = r"C:\\Program Files (x86)\\KJLC\\eKLipse"
        os.chdir(path)
        try:
            self.eklipse_window = ce.connect_to_instance_of_eklipse()
            self.eklipse_window.child_window(auto_id="Automation").click()
            print("application is already running, connected!")
        except Exception as e:
            print("application is not running, starting!")
            self.eklipse_window = ce.start_eklipse()
            ce.logInToEklipse(self.eklipse_window)
            print("logged in to eklipse", type(e).__name__)

    def confirm_stack_light_status(self, target_status: str) -> bool:
        '''
        Checking for target stack light status

        Parameters
        ----------
        target_status : str
            Target status, "GREEN", "BLUE" etc..

        Returns
        -------
        bool
            Target status reached
        '''
        stack_light_status = ce.check_stack_light_status(self.eklipse_window)
        return stack_light_status == target_status

    def run_recipe(self, recipe_name: str, wait_for_step=99) -> bool:
        '''activating one of the recipe buttons to the right hand side, and then waiting for the recipe to complete

        Parameters
        ----------
        recipe_name : str
            Name of recipe to run
        wait_for_step : int, optional
            Time limit of how long to wait for completion, by default 99

        Returns
        -------
        bool
            Recipe ran
        '''
        # for speed, this function assumes that stacklights have been checked before calling it!
        ce.go_to_automation_tab(self.eklipse_window)
        print("Requesting to run recipe " + recipe_name + "...")
        self.eklipse_window.child_window(auto_id=recipe_name).click()
        # recipe_stage = "not running yet"
        time.sleep(5)
        is_blue = self.confirm_stack_light_status(
            self.eklipse_window, sp.STACK_LIGHT_GREEN_STEADY_BLUE)
        if (is_blue):
            # recipe_stage = "running"
            print(recipe_name + " running...")
        else:
            print(recipe_name + " did not start, checking stack light...")
            return False

        finished = self.wait_for_recipe(
            self.eklipse_window, recipe_name, wait_for_step)
        if finished:
            return True

        return False

    def wait_for_recipe(self, recipe_name: str, wait_for_step=99) -> bool:
        '''Waiting for recipe completion by checking the stack light status

        Parameters
        ----------
        recipe_name : str
            Current running recipe
        wait_for_step : int, optional
            Step in recipe, by default 99

        Returns
        -------
        bool
            If the recipe finished
        '''
        # waits for the recipe to complete, or for it to reach a specific step (wait_for_step)
        iterations = cp.WAIT_RECIPE_ITERATIONS
        wait_time = cp.WAIT_RECIPE_TIME
        for i in range(iterations):
            status = ce.check_stack_light_status(self.eklipse_window)
            if (status == sp.STACK_LIGHT_GREEN_STEADY_BLUE):
                step = ce.check_running_recipe_step(self.eklipse_window)
                if step >= wait_for_step:
                    print("recipe has reached or exceeded desired step (requested:" +
                          str(wait_for_step) + ", actual: " + str(step) + ")")
                    return True
                # print(recipe_name + " still running...checking again in " + str(wait_time) + " seconds...")
                print("...")
                time.sleep(wait_time)
            elif (status == sp.STACK_LIGHT_GREEN):
                print(recipe_name + " completed")
                return True
            elif (status == sp.STACK_LIGHT_GREEN_FLASH_BLUE):
                print(recipe_name + " has been paused")
                # perform some action such as giving the use option to wait or not
                return False
            else:
                print(recipe_name + " did not complete - check system status")
                return False
        print(recipe_name + " did not finish within expected timeframe of " +
              str(iterations*wait_time) + " seconds. Check system status")
        return False

    def begin_sputter_process(self) -> bool:
        '''Begin sputtering

        Returns
        -------
        bool
            Sputter process completed
        '''
        # check system ready
        print("Preparing to sputter - checking system status....")
        is_stacklight_ok = self.confirm_stack_light_status(
            self.eklipse_window, sp.STACK_LIGHT_GREEN)
        is_system_ready = ce.check_if_system_ready(self.eklipse_window)

        if (is_stacklight_ok and is_system_ready):

            # toggle gas injection valve:
            ce.set_parameter(self.eklipse_window, 1, sp.Check_GasInjValveOpen)
            time.sleep(cp.GAS_INJ_TOGGLE_TIME)
            ce.set_parameter(self.eklipse_window, 0, sp.Check_GasInjValveOpen)

            process_permission = ce.set_parameter(
                self.eklipse_window, 1, "PC Start Process")
            if not process_permission:
                print("process permission not granted - check system")
                return False

            started_OK = self.run_recipe(
                self.eklipse_window, sp.RECIPE_PREPARE)

            if not started_OK:
                print("Could not prepare system for sputtering")
                self.end_process(self.eklipse_window)
                return False

            # ignite targets (uses a pressure of 25 mTorr based on the defined Eklipse recipes, which also apply the ramp rates and pulse frequencies)
            for supply_number in cp.POWER_SUPPLIES[self.power_axes]:
                print("Igniting target connected to power supply " +
                      str(supply_number))
                ignited_OK = self.run_recipe(
                    self.eklipse_window, sp.PS_IGNITION_RECIPES[supply_number-1])
                if not ignited_OK:
                    print(
                        "Could not ignite target connected to Power Supply " + str(supply_number))
                    self.end_process(self.eklipse_window)
                    return False

            # reduce pressure to typical level for presputtering
            ce.set_pressure(self.eklipse_window, cp.PRESPUTT_PARAMS[3])
            time.sleep(5)
            print("All specified targets ignited, ready to continue")

            return True

        else:
            print(
                "Could not begin sputtering due to system warning or undefined system state")
            return False

    def presputter(self, ps_time: int) -> bool:
        '''Presputter before starting a series

        Parameters
        ----------
        ps_time : int
            Presputter time in seconds

        Returns
        -------
        bool
            presputtering completed
        '''
        print("Pre-sputtering for " + str(ps_time) + " s")
        time.sleep(ps_time)
        # check if target voltages are within an acceptable range to the expected values.
        for k in range(3):
            if self.power_axes[k]:
                power_supply_index = cp.POWER_SUPPLIES[k]-1
                ce.go_to_automation_tab(self.eklipse_window)
                voltage = float(ce.read_parameter(
                    self.eklipse_window, sp.PS_READ_VOLTAGE_SIGNALS[power_supply_index]))
                print("Voltage on Power Supply " +
                      str(cp.POWER_SUPPLIES[k]) + " = " + str(voltage) + " V,")
                error_prc = 100 * \
                    float(
                        abs(voltage-cp.PRESPUTT_VS[k]))/float(cp.PRESPUTT_VS[k])
                print("Voltage is within " + str(error_prc) +
                      " percent of expected value")
                if error_prc > cp.PRE_SPUTT_V_ERROR:  # NEEDS TO BE EVALUATED WHAT ERROR IS ALLOWABLE
                    return False
        return True

    def end_process(self):
        '''End process
        '''
        # Runs the "end process" recipe, or if the main recipe is already running, skips ahead so that it ends by itself.

        print("***end_process called - checking stack light")
        SL = ce.check_stack_light_status(self.eklipse_window)
        print(SL)
        if SL == sp.STACK_LIGHT_GREEN:
            ended = self.run_recipe(self.eklipse_window, sp.RECIPE_END_PROCESS)
            if ended:
                print("Process ended successfully")
                return
            else:
                print("Could not end process - check system")
        elif SL == sp.STACK_LIGHT_GREEN_STEADY_BLUE or sp.STACK_LIGHT_GREEN_FLASH_BLUE:
            paused = SL == sp.STACK_LIGHT_GREEN_FLASH_BLUE
            running_recipe = ce.check_running_recipe_name(self.eklipse_window)
            recipe_step = ce.check_running_recipe_step(self.eklipse_window)

            if sp.MAIN_RECIPE_NAME_NO_SAMPLE in running_recipe:
                if int(recipe_step) == sp.MAIN_RECIPE_DWELL_STEP_NO_SAMPLE:
                    if paused:
                        ce.resume_paused_recipe(self.eklipse_window)
                    ce.skip_recipe_step(self.eklipse_window)
                    print("Process ending...")
                    self.wait_for_recipe(
                        self.eklipse_window, sp.RECIPE_END_PROCESS)
                    return
                else:
                    print("cannot end process at current stage - check system")
                    return
            elif sp.MAIN_RECIPE_NAME_SAMPLE in running_recipe:
                if int(recipe_step) == sp.MAIN_RECIPE_DWELL_STEP_SAMPLE:
                    if paused:
                        ce.resume_paused_recipe(self.eklipse_window)
                    ce.skip_recipe_step(self.eklipse_window)
                    print("Process ending...")
                    self.wait_for_recipe(
                        self.eklipse_window, sp.RECIPE_END_PROCESS)
                    return
                else:
                    print("cannot end process at current stage - check system")
                    return
            else:
                print("cannot end process during current recipe - check system")
                return
        else:
            print("Cannot end process due to interlock or abort state - check system")
            return

    def calc_ramp_time(self, old_parameters, new_parameters) -> int:
        '''Calculate the ramp time

        Parameters
        ----------
        old_parameters : _type_
            Previous set of parameters
        new_parameters : _type_
            New set of parameters to be applied

        Returns
        -------
        int
            Ramp time in seconds
        '''
        ramp_time = 0
        power_ramp_times = [0, 0, 0]

        if self.power_pad:
            pad = cp.POWER_PADDING
        else:
            pad = 0

        for n in range(3):
            if (self.power_axes[n]):
                diff = abs(old_parameters[n]-(new_parameters[n]+pad))
                ramp = float(diff)/float(cp.RAMP_RATES[n])
                power_ramp_times[n] = ramp
        power_ramp_time = max(power_ramp_times)

        pressure_ramp_time = 0
        if (new_parameters[3] < old_parameters[3]):
            pressure_ramp_time = 5
            if (new_parameters[3] < (old_parameters[3]-15)):
                pressure_ramp_time = 10

        ramp_time_raw = max(power_ramp_time, pressure_ramp_time)
        ramp_time = min(ramp_time_raw, 10)
        print("ramp time: " + str(ramp_time) + "s")
        return ramp_time

    def exchange(self, new_substrate: bool) -> str:
        '''Uload or load substrate

        Parameters
        ----------
        new_substrate : bool
            If have new substrate

        Returns
        -------
        str
            Substrate ID or failed status
        '''
        check = self.run_recipe(sp.RECIPE_UNLOAD)
        if check:
            check = self.run_recipe(sp.RECIPE_VENTLL)
            if check:
                print("LL vented, ready to unload/load substrates")
                if new_substrate:
                    substrate_ID = input(
                        "----> Load new substrate if required. Enter substrate_ID to confirm and continue.")
                else:
                    substrate_ID = "no substrate"
                check = self.run_recipe(sp.RECIPE_PUMPLL)
                if check:
                    check = self.run_recipe(sp.RECIPE_LOAD)
                    if check:
                        return substrate_ID
        if not check:
            print("Problem with sample exchange - check system")
            choice = input(
                "----> Press 1 to continue with run, or any other key to end the current series.")

            if choice == "1":
                substrate_ID = input("Confirm substrate_ID to continue.")
                return substrate_ID

        return "FAIL"

    def ramp_to_setpoints(self, old_parameters=[0, 0, 0, 0, 0], new_parameters=[0, 0, 0, 0, 0]) -> bool:
        '''Apply new setpoints 

        Parameters
        ----------
        old_parameters : list, optional
            Previous setpoints, by default [0, 0, 0, 0, 0]
        new_parameters : list, optional
            New setpoints to be applied, by default [0, 0, 0, 0, 0]

        Returns
        -------
        bool
            Setpoints successfully applied
        '''

        set_power_result = True
        set_pressure_result = True
        update_params = [True, True, True, True]
        for n in range(4):
            if old_parameters[n] == new_parameters[n]:
                update_params[n] = False
        print("parameters to be updated: " + str(update_params))

        # Apply pressure setting
        if update_params[3]:
            set_pressure_result = ce.set_pressure(
                self.eklipse_window, new_parameters[3])
            if not set_pressure_result:
                print("ramp_to_process_point(): Could not set pressure")
                return False

        ramp_time = self.calc_ramp_time(
            self.power_axes, old_parameters, new_parameters, True)
        # Apply power settings
        # first set power higher than target value (WILL NEED TO EVALUATE IF THIS IS NEEDED AND HOW MUCH OF A DIFFERENCE)
        if self.power_pad:
            for j in range(3):
                if self.power_axes[j] and update_params[j]:
                    set_power_result = ce.set_power(
                        self.eklipse_window, new_parameters[j]+cp.POWER_PADDING, j+1)
                    if not set_power_result:
                        print(
                            "ramp_to_process_point(): Power settings could not be applied")
                        return False
            if set_power_result:
                # time needed to ramp slowest target to requested value
                time.sleep(ramp_time)

        # then set at target value
        for j in range(3):
            if self.power_axes[j] and update_params[j]:
                set_power_result = ce.set_power(
                    self.eklipse_window, new_parameters[j], j+1)
                if not set_power_result:
                    print(
                        "ramp_to_process_point(): Power settings could not be applied")
                    return False

        if not self.power_pad:
            time.sleep(ramp_time)  # i.e. if we are not doing the power padding step, we need to wait here for the targets to ramp to the new value. If we were doing power padding, we have already waited for most of the change, and what remains is not much

        return True


def open_or_close_all_shutters(power_axes: list[bool], operation: str):
    '''Open or close all shutters

    Parameters
    ----------
    power_axes : list[bool]
        Which power axes that are switched on
    operation : str
        Open or Close
    '''
    for j in range(3):
        if power_axes[j]:
            ce.operate_target_shutter(BEA.eklipse_window, operation, j+1)


def execute_step_in_recipe(BEA: BeaSupervisor, series: es.ExperimentSeries, step_number: int, step_setpoints: list[int], old_setpoints: list[list[int]], metadata: dict):
    '''Execute one step in a recipe

    Parameters
    ----------
    BEA : BeaSupervisor
    series : es.ExperimentSeries
    step_number : int
    step_setpoints : list[int]
    old_setpoints : list[list[int]]
    metadata : dict
    '''
    print("Run ID:" + " TBC " + ", step: " + str(step_number))
    # Generate and add step metadata
    es.update_step_metadata(metadata, step_number, step_setpoints)

    # apply new conditions including any ramping time
    # OBS! NEED TO CHECK IF TARGETS ARE BEING IGNITED THAT WERE FORMERLY OFF, AND USE HIGHER PRESSURE FOR THAT (CAN FIX IN RAMP_TO_SETPOINTS)
    set_conditions = BEA.ramp_to_setpoints(old_setpoints, step_setpoints)
    if not set_conditions:
        print(
            "Step setpoints could not be applied, ending process and series...")
        BEA.end_process()
        return

    # open relevant shutters
    if series.samples:
        open_or_close_all_shutters(BEA.power_axes, operation="open")

    # Dwell, record data
    ce.record_data(BEA.eklipse_window, step_setpoints[4])

    # Check still running (i.e. that the main recipe has not timed out)
    step = ce.check_running_recipe_step(BEA.eklipse_window)
    if step != (sp.MAIN_RECIPE_DWELL_STEP_NO_SAMPLE or sp.MAIN_RECIPE_DWELL_STEP_SAMPLE):
        print("Run interrupted due to main recipe timeout - data not saved for current step, and run is not complete. Ending process and restarting run...")
        series.sources_ignited = False
        series.get_new_recipe = False
        BEA.end_process()
        return

    # close relevant shutters
    if series.samples:
        open_or_close_all_shutters(BEA.power_axes, operation="close")


def perform_series(do_presputter: bool, samples: bool, power_axes: np.array,
                   max_runs: int, power_pad: bool, metadata: dict, algorithm):
    '''Run an entire series

    Parameters
    ----------
    do_presputter : bool
    samples : bool
        If there is a sample
    power_axes : np.array
        Active power axes
    max_runs : int
        Maxumim number of runs
    power_pad : bool
        If power padding
    metadata : dict
    algorithm : function
        What function to be used to generate new parameter values
    '''

    BEA = BeaSupervisor(power_pad, power_axes)

    series_ID = wc.get_next_series_id()
    base_pressure = ce.read_parameter(BEA.eklipse_window, sp.BASE_PRESSURE)

    series = es.ExperimentSeries(
        BEA, samples, base_pressure, do_presputter)

    presputter_setpoints = cp.PRESPUTT_PARAMS + [cp.PRESPUTT_TIME]
    recipe = [presputter_setpoints]
    series.set_recipe(recipe)

    validator = vd.Validator()
    ce.setup_data_recording(BEA.eklipse_window, series.samples)

    series_metadata = series.create_series_metadata()
    metadata.update(series_metadata)

    for i in range(max_runs):  # this loop goes through the series of runs (experiments)

        print("Series " + series_ID + ", Run number " + str(i+1))

        if series.samples:
            # substrate holder removed, vent LL, ask for sample number, pump LL, reload
            series.substrate_ID = BEA.exchange(new_substrate=True)
            series.set_source_ignited(False)
            if series.substrate_ID == "FAIL":
                return

        if not series.sources_ignited:
            ready = BEA.begin_sputter_process()
            if ready:
                series.set_source_ignited(True)
            else:
                print("Could not start series, check system status")
                BEA.end_process()
                return

        # note that without samples, the target shutters will be open, otherwise they will be closed, and the sample at max height with substrate shutter open
        if series.do_presputter and not series.presputtered:
            presputter_result = BEA.presputter(cp.PRESPUTT_TIME)
            series.set_presputtered(presputter_result)
            if series.presputtered:
                print("Presputtering completed with voltages reaching expected values")
                presputter_info = "Presputtered for " + \
                    str(cp.PRESPUTT_TIME) + \
                    " s, with voltages reaching expected values"
            else:
                print(
                    "One or more targets did not reach expected voltage during pre-sputtering")
                presputter_info = "Presputtered for " + \
                    str(cp.PRESPUTT_TIME) + \
                    " s, voltages did not reach expected values"
                # because we just want to move on
                series.set_presputtered(True)
        else:
            presputter_info = "No presputtering"

        metadata["Pre-sputter description"] = presputter_info

        if series.samples:
            ready = BEA.run_recipe(sp.RECIPE_SPUTTER_SAMPLE,
                                   wait_for_step=sp.MAIN_RECIPE_DWELL_STEP_SAMPLE)
        else:
            ready = True
            if i == 0:
                ready = BEA.run_recipe(sp.RECIPE_SPUTTER_NO_SAMPLE,
                                       wait_for_step=sp.MAIN_RECIPE_DWELL_STEP_NO_SAMPLE)

        if not ready:
            print("Could not start series, check system status")
            BEA.end_process()
            return

        if series.get_new_recipe:
            # use try/except when getting new parameters, if the function does not work use default cp.PRESPUTT_PARAMS
            series.set_recipe(algorithm(power_axes))
            # !!!! should be function to get next set of new_parameters, returns a list of lists, with each sub-list having format power, power, power, pressure, dwell time
            print("The following parameters will be applied:")
            # could be nice to add names to the columns/rows of the recipe
            print(series.get_recipe())

        series.update_run_metadata(
            metadata, series.substrate_ID)

        # now iterate through the steps of each recipe (rows in dataframe)
        old_setpoints = presputter_setpoints
        step_number = 1

        for step_setpoints in series.recipe:
            execute_step_in_recipe(
                BEA, series, step_number, step_setpoints, old_setpoints, metadata)
            data_ok = validator.validate(metadata)
            # might be that we want differnt validators for different "algorithms"

            # based on our experience, don't need to have the "did not stabilise, repeat" category. Just save and move on
            if data_ok:
                print("***Data saved***")
            else:
                print("Recording failed (e.g. readings did not settle) - Data not saved")
            # call data validator to check and save data, check if run should be repeated or not.
            # output from Emirs function - True if steady state was reached (or "unstable" process detected). False if the settings should be repeated

            step_number += 1
            old_setpoints = step_setpoints
        series.get_new_recipe = True
        # goes to next run in the series

    if samples:
        print(
            "Series ended after reaching maximum allowed number of runs (or recipe timeout)")
        BEA.exchange()
        return  # process should already have ended

    print("Series ended after reaching maximum allowed number of runs (or recipe timeout); ending process...")
    BEA.end_process()
    return


if __name__ == "__main__":
    perform_series(do_presputter=True, samples=False, power_pad=True, power_axes=np.array([False, True, True]), max_runs=100, metadata=cp.CAMPAIGN_METADATA,
                   algorithm=algorithms.generate_random_parameters)
