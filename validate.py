import pandas as pd
import numpy as np
import glob
import os
from pymongo import MongoClient
import campaign_parameters as cp
import system_parameters as sp

'''
The Validator class validates the steadiness of magnetron sputter experiments based on their CSV outputs.
Steadiness is judged by a set of parameters settling below a given standard deviation before a given time limit.
Steady and completely unsteady experiments are evaluated to "True" by the validate function and stored in a MongoDB database. 
Experiments which settle after the given time limit are evaluated to "False" by the validate function and are not stored in 
the database. The False signal indicates that the experiment should be rerun.
'''


class Validator:

    # TODO: check that default filepath works on lab computer
    def __init__(self, database="BERTHA-Data", collection="Working Data", path_CSV=r"C:\\Program Files (x86)\\KJLC\\eKLipse\\Log\\RecordingData"):
        '''
        Initializer for the DatabaseLoader class

        Parameters
        ----------
        database: which mongodb database to use 
        collection: which collection of given database to enter experiment data in
        path_CSV: file path for experiment CSV files (defaults to Log/RecordingData)

        Class variables
        ---------------
        sigma_V: 
        sigma_P: 
        t:
        t_d:
        steady_params: 
        '''

        client = MongoClient()
        self.db = client[database]
        self.collection = self.db[collection]
        self.path_CSV = path_CSV

        self.sigma_V = 1
        self.sigma_P = 0.1
        self.t = 0.5
        self.t_d = 0.3
        self.thresholds = {
            'Actual_pressure_[mTorr]': self.sigma_P,
            "Voltage_Ax1_[V]": self.sigma_V,
            "Voltage_Ax2_[V]": self.sigma_V,
            "Voltage_Ax3_[V]": self.sigma_V
        }

    def process_df(self, df):
        '''
        Converts time stamp column from String datetime to seconds starting from 0 
        and rounds values of selected columns (all but PC Source columns) to 3 decimals

        Parameters
        ----------
        df: pandas df of experiment CSV


        Returns
        ---------
        date: string of experiment date (mm/dd/yy)
        df: pandas df with converted time column and 3 decimal values for all columns
        '''

        # Convert to datetime
        # df['Time Stamp'] = pd.to_datetime(df['Time Stamp'])

        df['Time Stamp'] = pd.to_datetime(
            df['Time Stamp'], format='%b-%d-%Y %H:%M:%S.%f %p')
        # Save date
        date = df['Time Stamp'].iloc[0].date().strftime('%m/%d/%Y')

        # Convert datetime to seconds starting from zero
        df['Time Stamp'] = (df['Time Stamp'] -
                            df['Time Stamp'].iloc[0]).dt.total_seconds()

        # Round selected columns to three decimals
        rounded_columns = []

        for i in df.columns.values:
            if 'QCM' not in i:
                rounded_columns.append(i)

        df[rounded_columns] = df[rounded_columns].round(3)

        return date, df

    def validate(self, metadata):
        '''
        The validate function is the core function of the Validator class. The function (1) retrieves the latest 
        sputtering experiment CSV file from a given filepath, (2) calculates if the experiment has settled
        according to given (time and std) thresholds, (3) stores settled and fully unsettled experiments in 
        the database, and returns a True bool, since these have clear results; alternatively, does not store
        the experiment if the experiment settles too late within given thresholds and returns False, indicating
        that the experiment controller should retry the experiment.
        '''

        # Get date of latest experiment and its CSV as dataframe
        date, df = self.getLastExperiment()

        # Create date dictionary
        date_dict = {'Date': date}

        # Get size of dataframe (n rows)
        rows = len(df.axes[0])

        # Find steady state and drag threshold as index
        n_t = int(self.t*rows)
        n_td = int(self.t_d*rows)

        for j in range(0, n_t + n_td):

            if all(df[p].tail(rows-j).std() <= self.thresholds[p] for p in self.thresholds.keys()):
                if (j <= n_t):
                    # Get settling time
                    settle_time_dict = {
                        'Settling time': df["Time Stamp"].iloc[j]}

                    # Create settled status entry (True)
                    status_dict = {"Settled": True}

                    # Get mean and stds for all columns
                    calc_dict = self.calculate_statistics(df, rows, index=j)

                    # Merge all dictionaries into a doc
                    doc = {**date_dict, **metadata, **status_dict, **
                           settle_time_dict, **df.to_dict('list'), **calc_dict}

                    # Insert doc into database collection
                    self.collection.insert_one(doc)

                    return True
                else:
                    # Return False if experiment settles between time t and t_d, indicating that the experiment should be rerun
                    return False

        '''Return True for fully unstable experiments, indicating that we have stored the result to database'''

        # Created settled status entry (False)
        status_dict = {"Settled": False}

        # Get mean and stds for all columns
        calc_dict = self.calculate_statistics(df, rows)

        # Merge all dictionaries into a doc
        doc = {**date_dict, **metadata, **status_dict,
               **df.to_dict('list'), **calc_dict}

        # Insert doc into database collection
        self.collection.insert_one(doc)

        return True

    def calculate_statistics(self, df, rows, index=1):
        '''
        Calculates mean and std for all fields (except time) in the dataframe

        Parameters
        ----------
        df: processed dataframe with experiment data  
        rows: amount of rows in the dataframe (already calculated in validate function)
        index: in settled experiments, index indicates where measurements become stable, so
        we only calculate statistics for where the experiment is steady

        Returns
        -------
        calc_dict: a dictionary of mean and std for all fields (except time) in the dataframe

        '''

        # Prepare calculation dictionary
        calc_keys = []
        calc_vals = []

        # Calculate settled mean and std for all columns
        for k in df.columns[1:]:
            mean_key = k + ' Mean'
            std_key = k + ' STD'
            mean = df[k].tail(rows-index).mean()
            std = df[k].tail(rows-index).std()

            # Round off values that are not PC Source
            if 'QCM' not in k:
                mean = np.round(mean, 3)
                std = np.round(std, 3)

            calc_keys.extend([mean_key, std_key])
            calc_vals.extend([mean, std])

        # Create calculation dictionary
        calc_dict = dict(zip(calc_keys, calc_vals))

        return calc_dict

    def getLastExperiment(self):
        '''
        Retrieves the latest modified file from the CSV filepath and processes it.    

        Returns
        -------
        date: String of date of the experiment
        df: A dataframe of the experiment CSV (Experiment parameters + time series measurements)
        '''

        os.chdir(self.path_CSV)

        files = os.listdir()

        latest_file = max(files, key=os.path.getctime)

        # Read csv
        df = pd.read_csv(latest_file, skiprows=[0, 1])

        # rename columns accoridng to current setup and our formats
        df.rename(columns=cp.RECORDING_NAMES, inplace=True)
        df.rename(columns=sp.BASIC_PARAMETERS_TS, inplace=True)

        print(df)

        # Retrieve date and processed df
        return self.process_df(df)
