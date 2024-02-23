import os

path = r"C:\\Users\\BERTHA\\Documents\\AutomateEklipse\\Workflow"


def get_next_series_id(file_path='BEA_SeriesID_tracker.txt') -> str:
    '''Get next series ID

    Parameters
    ----------
    file_path : str, optional
        From where to get the ID, by default 'BEA_SeriesID_tracker.txt'

    Returns
    -------
    str
        Series ID
    '''

    os.chdir(path)

    # Check if the file that stores the last seriesID exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            # Read the last seriesID and convert it to an integer
            last_series_id = int(file.read().strip())
    else:
        # If the file does not exist, assume starting with seriesID 0
        last_series_id = 0

    # The next seriesID is one more than the last seriesID
    next_series_id = last_series_id + 1

    # Update the file with the next seriesID for future seriess
    with open(file_path, 'w') as file:
        file.write(str(next_series_id))

    formatted_ID = "{:03d}".format(next_series_id)
    return formatted_ID


def reset_series_id(file_path='BEA_SeriesID_tracker.txt'):
    '''Resetting the series ID

    Parameters
    ----------
    file_path : str, optional
        Where to reset it, by default 'BEA_SeriesID_tracker.txt'
    '''
    os.chdir(path)

    with open(file_path, 'w') as file:
        file.write('0')


# Example usage
if __name__ == "__main__":
    reset_series_id()
    # series_id = get_next_series_id()
    # print(f"The current seriesID is: {series_id}")
   # print(series_id)
    # Proceed with your lab process automation u
