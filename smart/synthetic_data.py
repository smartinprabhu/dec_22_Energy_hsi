import pandas as pd

def synthetic_process_algol(pplin, cost_per_hr):
    """
    Synthetic process algorithm to fill missing values and generate synthetic data.

    Parameters:
    pplin (pd.DataFrame): Input dataframe with hourly energy consumption data.
    cost_per_hr (float): Cost per kilowatt-hour.

    Returns:
    tuple: A tuple containing the combined dataframe with synthetic data, replaced values dataframe, and cost dataframe.
    """

    def calculate_patterns(pplin):
        """
        Calculate average and hourly patterns for each day of the week.

        Parameters:
        pplin (pd.DataFrame): Input dataframe with hourly energy consumption data.

        Returns:
        tuple: A tuple containing weekday patterns and hourly patterns dictionaries.
        """
        weekday_patterns = pplin.groupby(pplin.index.dayofweek)[
            "answer_value"
        ].mean()
        hourly_patterns = {}
        for weekday in range(7):
            weekday_data = pplin[pplin.index.dayofweek == weekday]
            hourly_patterns[weekday] = weekday_data.groupby(weekday_data.index.hour)[
                "answer_value"
            ].mean()
        return weekday_patterns, hourly_patterns

    def replace_missing_values(pplin, weekday_patterns, hourly_patterns):
        """
        Replace missing values and zero values in the dataframe using calculated patterns.

        Parameters:
        pplin (pd.DataFrame): Input dataframe with hourly energy consumption data.
        weekday_patterns (dict): Dictionary containing weekday patterns.
        hourly_patterns (dict): Dictionary containing hourly patterns.

        Returns:
        dict: A dictionary containing replaced values with their indices.
        """
        missing_indices = pplin[pplin["answer_value"].isna()].index
        zero_indices = pplin[pplin["answer_value"] == 0].index
        replaced_values = {}

        for index in missing_indices.union(zero_indices):
            weekday = index.dayofweek
            hour = index.hour
            replaced_value = hourly_patterns.get(weekday, {}).get(
                hour, weekday_patterns.get(weekday)
            )
            if replaced_value is not None:
                pplin.at[index, "answer_value"] = replaced_value
                replaced_values[index] = replaced_value

        return replaced_values

    def generate_synthetic_data(pplin, weekday_patterns, hourly_patterns):
        """
        Generate synthetic data for the missing hours.

        Parameters:
        pplin (pd.DataFrame): Input dataframe with hourly energy consumption data.
        weekday_patterns (dict): Dictionary containing weekday patterns.
        hourly_patterns (dict): Dictionary containing hourly patterns.

        Returns:
        pd.DataFrame: A dataframe containing synthetic data.
        """
        current_time = pd.Timestamp.now().floor("h")
        last_timestamp = pplin.index.max()
        synthetic_indices = pd.date_range(
            start=last_timestamp + pd.Timedelta(hours=1), end=current_time, freq="h"
        )

        synthetic_data = []
        for timestamp in synthetic_indices:
            weekday = timestamp.dayofweek
            hour = timestamp.hour
            synthetic_value = hourly_patterns.get(weekday, {}).get(
                hour, weekday_patterns.get(weekday)
            )
            synthetic_data.append((timestamp, synthetic_value))

        return pd.DataFrame(
            synthetic_data, columns=["measured_ts", "answer_value"]
        )

    # Main function logic
    weekday_patterns, hourly_patterns = calculate_patterns(pplin)
    replaced_values = replace_missing_values(pplin, weekday_patterns, hourly_patterns)
    synthetic_df = generate_synthetic_data(pplin, weekday_patterns, hourly_patterns)

    pplin.reset_index(inplace=True)
    energy_with_synthetic = pd.concat([pplin, synthetic_df], ignore_index=True)
    energy_with_synthetic.set_index("measured_ts", inplace=True)

    replaced_data = pd.DataFrame(
        list(replaced_values.items()), columns=["measured_ts", "Replaced Value"]
    )
    r_cost = pd.DataFrame()
    r_cost["cost"] = replaced_data["Replaced Value"] * cost_per_hr

    return energy_with_synthetic, replaced_data, r_cost
