import pandas as pd


#Question 1 #
def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')
car_matrix.fillna(0,inplace=True)

return df

#Question 2#

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Adding categorical column 'car_type'
    df['car_type'] = pd.cut(df['car_values'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each 'car_type'
    car_type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    sorted_car_type_counts = dict(sorted(car_type_counts.items()))

    return sorted_car_type_counts

    #question 3#
    def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Calculated the mean of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identified indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

    #question 4#
   

def filter_routes(df: pd.DataFrame) -> list:
    """
    Return the sorted list of values in the 'route' column for which
    the average of values in the 'truck' column is greater than 7.

    Args:
        df (pandas.DataFrame): Input DataFrame.

    Returns:
        list: Sorted list of values in the 'route' column.
    """
    # Group by 'route' and calculate the mean of 'truck' for each group
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average of 'truck' is greater than 7
    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of selected routes
    selected_routes.sort()

    return selected_routes

#question 5#
def multiply_matrix(car_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Modify each value in the car matrix based on specified logic.

    If a value is greater than 20, multiply by 0.75.
    If a value is 20 or less, multiply by 1.25.
    Round the values to 1 decimal place.

    Args:
        car_matrix (pandas.DataFrame): Input car matrix DataFrame.

    Returns:
        pandas.DataFrame: Modified car matrix.
    """
    modified_matrix = car_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    
    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


#question 6#


def check_timestamp_completeness(df: pd.DataFrame) -> pd.Series:
    """
    Check the completeness of timestamps for each (id_1, id_2) pair.

    Args:
        df (pandas.DataFrame): Input DataFrame with columns 'id_1', 'id_2', and 'timestamp'.

    Returns:
        pandas.Series: Boolean series indicating if each (id_1, id_2) pair has incorrect timestamps.
                       Multi-index (id_1, id_2).
    """
    # Combining 'startDay' and 'startTime' into a single datetime column
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    # Combining 'endDay' and 'endTime' into a single datetime column
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Calculating the time difference for each (id_1, id_2) pair
    df['time_difference'] = df['end_timestamp'] - df['start_timestamp']

    # Check if the time difference is equal to a full 24-hour period
    full_24_hours = df['time_difference'] == pd.Timedelta(days=1)

    # Checking if each unique (id_1, id_2) pair spans all 7 days of the week
    spans_all_days = df.groupby(['id_1', 'id_2'])['start_timestamp'].agg(lambda x: x.dt.dayofweek.nunique() == 7)

    # Combining the two conditions to check timestamp completeness
    completeness_check = full_24_hours & spans_all_days

    return completeness_check
    