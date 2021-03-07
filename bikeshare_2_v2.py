import time
import pandas as pd
import numpy as np

#Set up dictionary with city names as key and city csv data files as values
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


#Set up lists of months, days, and possible responses
months = ['all','january', 'february', 'march', 'april', 'may', 'june']
days = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
responses = ['yes', 'y', 'no', 'n']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('Please choose a Chicago, New York City, or Washington: ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('That city is not available, please choose again.')

    while True:
        # get user input for month (all, january, february, ... , june)
        month = input('Please choose one of the first six months or "all" for all months: ').lower()
        if month in months:
            break
        else:
            print('That is not a valid entry, please choose again.')

    while True:
        # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Please choose an individual day or "all" for the whole week: ').lower()
        if day in days:
            break
        else:
            print('That is not a valid entry, please choose again.')


    print('-'*40)
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
    #load cvs into dataframe
    df = pd.read_csv(CITY_DATA[city])

    #convert Start Time column unto datatime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day, and hour from dataframe to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common rental month is ' + common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common rental day is ' + common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common rental hour is ' + str(common_hour))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is ' + common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is ' + common_end_station)
    print()

    # display most frequent combination of start station and end station trip
    start_end_station = 'Start: ' + df['Start Station'] + ' & End: ' + df['End Station']
    df['Start End Stations'] = start_end_station
    common_stations = df['Start End Stations'].mode()[0]
    print('The most common combination of stations is ' + common_stations)
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = round(df['Trip Duration'].sum())
    print('The total durations of trips is : ' + str(total_time) + ' seconds')
    print()
    # display mean travel time
    average_trip_time = round(df['Trip Duration'].mean())
    print('The average trip duration is : ' + str(average_trip_time) + ' seconds')
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)
        print()
    else:
        print("No gender data is available")


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('The oldest person who rented was born in ' + str(int(oldest)))
        print('The youngest person who rented was born in ' + str(int(youngest)))
        print('The most common birth year of people rented is: ' + str(int(common_birth_year)))
    else:
        print("No birth year data is available")

    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Ask user if they would like to inspect the raw data"""

    count = 0
    header = input('Would you like to see 5 lines of data? (y or n): ')
    while (header == 'y' or header == 'yes') and count+5 < df.shape[0]:
        print(df.iloc[count:count+5])
        count += 5
        header = input('Would you like to see more data? ')

def restart():
    """Ask the user if they would like to restart the program"""
    ask_user = input('\nWould you like to restart? Enter yes or no.\n').lower()

    while ask_user not in ('yes', 'no'):
        print('This is not a valid response.')
        ask_user = input('\nWould you like to restart? Enter yes or no.\n').lower()

    while True:
        if ask_user == 'yes':
            main()
        else:
            quit()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart()


if __name__ == "__main__":
    main()
