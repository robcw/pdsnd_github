"""
 Filename:  bikeshare_project.py
 Author:    Rob C Wild
 Email:     robcwild@gmail.com
 Date:      February 20, 2023
 Purpose:   Udacity Programming for Data Science with Python, Project 2
 Notes:     All work is solely my own.  I used the external website Stack Overflow for help converting seconds into
            human-readable time, displaying all columns of a dataframe, and formatting integers with commas.
 Reference: https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
            https://stackoverflow.com/questions/11361985/output-data-from-all-columns-in-a-dataframe-in-pandas
            https://stackoverflow.com/questions/1823058/how-to-print-a-number-using-commas-as-thousands-separators
"""

import time
import pandas as pd

city_data = {'Chicago': 'chicago.csv',
             'New York': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bike share data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_city = ['Chicago', 'New York', 'Washington']
    valid_month = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
    valid_day = ['All', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    while True:
        city = input('\nWould you like to see data for Chicago, New York, or Washington? ').title()
        if city in valid_city:
            break
        else:
            print('Please enter a valid city.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter month (all, January, February, ... , June): ').title()
        if month in valid_month:
            break
        else:
            print('Please enter a valid month.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter day of week (all, Sunday, Monday, ... , Saturday): ').title()
        if day in valid_day:
            break
        else:
            print('Please enter a valid day.')

    print('\n', '-'*50, '\n', '-'*50, sep='')
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = city_data[city]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()

    if month != 'All':
        df = df[df['month'] == month]

    if day != 'All':
        df = df[df['day'] == day]

    return df


def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        (dataframe) df - filtered city data
        (str) month - filter month, or "all" for no month filter
        (str) day - filter day, or "all" for no day filter
    """

    print('\nCalculating the most common times of travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
        most_common_month = df['month'].mode()[0]
        print('Month with most trips:   ', most_common_month)

    # display the most common day of week
    if day == 'All':
        most_common_day = df['day'].mode()[0]
        print('Most popular day of week:', most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular start hour: ', popular_hour)

    print("\nMost common times statistics took %s seconds." % (time.time() - start_time))
    print('\n', '-'*50, sep='')


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Arg:
        (dataframe) df - filtered city data
    """

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    df['Start and End Stations'] = df['Start Station'] + " to " + df['End Station']

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:         ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station:           ', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_stations = df['Start and End Stations'].mode()[0]
    print('Most popular trip from start to end:', popular_start_end_stations)

    print("\nStation and trip statistics took %s seconds." % (time.time() - start_time))
    print('\n', '-'*50, sep='')


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Arg:
        (dataframe) df - filtered city data
    """

    print('\nCalculating trip duration statistics...\n')
    start_time = time.time()

    # display total travel time
    minutes, seconds = divmod(df['Trip Duration'].sum(), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    print("Total travel time: {:,} days, {} hours, {} minutes, {} seconds".format(int(days), int(hours), int(minutes),
                                                                                  int(seconds)))

    # display mean travel time
    minutes, seconds = divmod(df['Trip Duration'].mean(), 60)
    hours, minutes = divmod(minutes, 60)
    print("Mean travel time:  {} hours, {} minutes, {} seconds".format(int(hours), int(minutes), int(seconds)))

    print("\nTrip duration statistics took %s seconds." % (time.time() - start_time))
    print('\n', '-'*50, sep='')


def user_stats(df, city):
    """
    Displays statistics on bike share users.

    Args:
        (dataframe) df - filtered city data
        (str) city - name of the city being analyzed
    """

    print('\nCalculating user statistics...\n')
    start_time = time.time()

    # Display counts of user types
    print("User type counts:\n", df['User Type'].value_counts(dropna=False).to_string(), sep="")

    if city.lower() != 'washington':

        # Display counts of gender
        print("\nGender counts:\n", df['Gender'].value_counts(dropna=False).to_string(), sep="")

        # Display earliest, most recent, and most common year of birth
        print("\nEarliest year of birth:   ", int(df['Birth Year'].min()))
        print("Most recent year of birth:", int(df['Birth Year'].max()))
        print("Most common year of birth:", int(df['Birth Year'].mode()[0]))

    else:
        print("\nThere are no gender or birth year statistics available for Washington.")

    print("\nUser statistics took %s seconds." % (time.time() - start_time))
    print('\n', '-'*50, '\n', '-'*50, sep='')


def show_data(df):
    """
    Displays raw data in increments of 5 rows.

    Args:
        (dataframe) df - filtered city data
    """

    while True:
        raw_data = input('\nWould you like to see the first 5 lines of raw data (y/n)? ').title()
        if raw_data in ['Yes', 'Y']:
            # Display first 5 lines of raw data
            pd.set_option('display.max_columns', None)
            line = 5
            print(df[:line])

            while True:
                more_raw_data = input('\nWould you like to see another 5 lines of raw data (y/n)? ').title()
                if more_raw_data in ['Yes', 'Y'] and (line+5 < len(df.index)):
                    # Display next 5 lines of raw data
                    print(df[line:line+5])
                    line += 5
                elif more_raw_data in ['No', 'N'] or (line+5 > len(df.index)):
                    break
                else:
                    continue
            break
        elif raw_data in ['No', 'N'] or (line+5 > len(df.index)):
            break
        else:
            continue

    print('\n', '-'*50, '\n', '-'*50, sep='')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_data(df)

        restart = input('\nWould you like to restart (y/n)? ').title()
        if restart not in ['Yes', 'Y']:
            break


if __name__ == "__main__":
    main()
