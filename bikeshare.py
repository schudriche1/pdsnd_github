import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city = ''
month = ''
day = ''
day_dict_in = {'monday' : 0, 'tuesday' : 1, 'wednesday' : 2, 'thursday' : 3, 'friday' : 4, 'saturday' : 5, 'sunday' : 6}
day_dict_out = {0 : 'Monday', 1 : 'Tuesday', 2 : 'Wednesday', 3 : 'Thursday', 4 : 'Friday', 5 : 'Saturday', 6 : 'Sunday'}
month_dict_out = {1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 10 : 'October', 11 : 'November', 12 : 'December'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Would you like to get information for Chicago, New York City, or Washington? ").lower()
            assert(city in ['chicago', 'new york city', 'washington', 'new york'])
            if city == 'new york':
                city = 'new york city'
            break
        except AssertionError as e:
            print('Please enter a valid city name!')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter a month to filter by.  If you wish to view all months, enter 'all': ").lower()
            assert(month in ['january', 'february', 'march', 'april', 'may', 'june', 'all'])
            break
        except AssertionError as e:
            print('Please enter a valid month!')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Please enter a day of the week to filter by.  If you wish to view all days, enter 'all': ").lower()
            assert(day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'])
            break
        except AssertionError as e:
            print('Please enter a valid day!')


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        day = day_dict_in[day]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

#This is where time statistics are computed
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month

    # TO DO: display the most common day of week
    df['dow'] = df['Start Time'].dt.day_of_week

    df['hour'] = df['Start Time'].dt.hour

    try:
        popular_month = df['month'].mode()[0]
        print('Most popular month: ', month_dict_out[popular_month])

        popular_dow = df['dow'].mode()[0]
        print('Most popular day of week: ', day_dict_out[popular_dow])

        popular_hour = df['hour'].mode()[0]
        print('Most popular hour: ' + str(popular_hour) + ':00')
    except:
        print('No time data is available for the selected filter(s).')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    try:
        popular_start = df['Start Station'].mode()[0]
        print('Most popular start station: ', popular_start)

        popular_end = df['End Station'].mode()[0]
        print('Most popular end station: ', popular_end)

        df['Station Combo'] = df['Start Station'] + " and " + df['End Station']
        popular_combo = df['Station Combo'].mode()[0]
        print('Most popular start and end station combination: ', popular_combo)
    except:
        print('No station data is available for the selected filter(s).')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # TO DO: display total travel time
    try:
        df['Time Traveled'] = df['End Time'] - df['Start Time']
        print('Total time traveled: ', df['Time Traveled'].sum())
        # TO DO: display mean travel time
        print('Mean time traveled: ', df['Time Traveled'].mean())
    except:
        print('No trip data is available for the selected filter(s).')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
    # TO DO: Display counts of user types
        user_types = df['User Type'].value_counts()
        print('User type breakdown:\n' + str(user_types) + '\n')
        try:
            # TO DO: Display counts of gender
            genders = df['Gender'].value_counts()
            print('User gender breakdown:\n' + str(genders))

            # TO DO: Display earliest, most recent, and most common year of birth
            print('\nUser birth year breakdown:')
            print('Earliest birth year: ', int(df['Birth Year'].min()))
            print('Latest birth year: ', int(df['Birth Year'].max()))
            print('Most common birth year: ', int(df['Birth Year'].mode()))
        except KeyError:
            print('No gender or birth year data available.')
    except:
        print('No user data is available for the selected filter(s).')
    finally:
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:
            try:
                view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no: ").lower()
                assert(view_data == 'yes' or view_data == 'no')
                break
            except AssertionError:
                print('Please enter yes or no!')

        start_loc = 0

        while view_data == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            while True:
                try:
                    view_data = input("Do you wish to continue? Enter yes or no: ").lower()
                    assert(view_data == 'yes' or view_data == 'no')
                    break
                except AssertionError:
                    print('Please enter yes or no!')

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            try:
                assert(restart == 'yes' or restart == 'no')
                break
            except AssertionError:
                print("Please enter yes or no!")

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
