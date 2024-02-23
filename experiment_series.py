import campaign_parameters as cp
import workflow_control as wc
import datetime


class ExperimentSeries:
    def __init__(self, samples: bool, base_pressure: str, do_presputter: bool):
        '''Initialize ExperimentSeries object

        Parameters
        ----------
        samples : bool
            If have samples
        base_pressure : str
            Base pressure in the sputtering chamber
        do_presputter : bool
            Do presputter
        '''
        self.samples = samples
        self.sources_ignited = False
        self.get_new_recipe = True
        self.presputtered = False
        self.do_presputter = do_presputter
        self.recipe = []
        self.substrate_ID = "No substrate"
        self.series_description = ""
        self.series_ID = wc.get_next_series_id()
        self.base_pressure = base_pressure
        self.date_time_string = str(datetime.datetime.now())

        self.promt_series_description()

    def promt_series_description(self):
        '''Prompt the user for series description
        '''
        series_description = input("Enter series description: ")
        self.series_description = series_description

    def create_series_metadata(self):
        '''Create series metadata

        Returns
        -------
        series_metadata: dict
            Dict containing series metadata
        '''
        series_metadata = {
            # NS = no samples/substrates
            "Series ID": (cp.CAMP_CODE + "_" + self.series_ID),
            "Series description": self.series_description,
            "Sample produced?": self.samples,
            "Pre-sputter?": self.do_presputter,
            "Pre-sputter description": "no presputtering",
            "Series start date/time": self.date_time_string,
            "Base pressure (start) [Torr]": self.base_pressure,
            "SDL algorithm": "Random"
        }
        return series_metadata

    def update_run_metadata(self, metadata: dict):
        '''Append run metadata

        Parameters
        ----------
        metadata : dict
            Dict to be appended
        '''
        run_metadata = {
            "Run ID": "TBC",  # this is an individual experiment in a series,
            "Recipe_name": "recipe name",
            "Number_of_steps": 0,
            "Substrate_ID": self.substrate_ID
        }
        metadata.update(run_metadata)

    def set_recipe(self, recipe: list[list[int]]):
        self.recipe = recipe

    def set_presputtered(self, presputtered: bool):
        self.presputtered = presputtered

    def set_source_ignited(self, is_ignited: bool):
        self.sources_ignited = is_ignited

    def get_recipe(self):
        return self.recipe


def update_step_metadata(metadata: dict, step_number: int, step_setpoints: list[int]):
    '''Append step metadata

    Parameters
    ----------
    metadata : dict
        Dict to be appended
    step_number : int
    step_setpoints : list[int]
        Current setpoints
    '''
    step_metadata = {
        "Step_number": step_number,
        "Power_Ax1_setpoint_[W]": step_setpoints[0],
        "Power_Ax2_setpoint_[W]": step_setpoints[1],
        "Power_Ax3_setpoint_[W]": step_setpoints[2],
        "Pressure_setpoint_[mTorr]": step_setpoints[3],
        "Dwell_time_[s]": step_setpoints[4]
    }
    metadata.update(step_metadata)
