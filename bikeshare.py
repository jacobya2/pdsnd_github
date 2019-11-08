import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = ''
    while city.lower() not in CITY_DATA.keys():
        if city == '':
            city = input("For which city would you like to see data? Chicago, New York City, or Washington?\n\t")
        else:
            print("\nOops! The value you entered '",city, "', is not a valid selection. \n\tPlease choose from: Chicago, New York City, or Washington.")
            city = input('\t')



    # TO DO: get user input for month (all, january, february, ... , june)
    month = ''
    while month.lower() not in ['all','january', 'february','march','april','may','june']:
        if month == '':
            month = input('\nPlease enter a month name or enter "all" to return data for all months:\n\t')
        elif month.lower() in ['july','august','september','october','november','december']:
            #User enters valid month, but a month for which there is no data.
            print('\nWe apologize. We do not have data for your selected month. Please enter a month from January to June.')
            month = input('\t')
        else:
            print("\nOops! ''", month, "'is not a valid value. Please try again. (Becareful of spelling!)")
            month = input('Please enter a month name or enter "all" to return data for all months.\n\t')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day.title() not in ['All','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']:
        if day == '':
            day = input('\nPlease enter a day of the week or enter "all" to return data for all days of the week.\n\t')
        else:
            print("\nOops! You've entered an invalid value. Becareful of spelling and be sure to give the full weekday name, e.g. 'Monday', 'Tuesday', etc.'")
            day = input('Please enter a day of the week or enter "all" to return data for all days of the week.\n\t')

    print('-'*40)
    return city.lower(), month.lower(), day.title()

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['Hour'] = df['Start Time'].dt.hour
    df['weekday'] = df['Start Time'].dt.weekday_name

    #match user string entry for month with numeric equivalent(1-12) for later filtering
    month_convert = {'january': 1, 'february': 2, 'march':3, 'april':4, 'may': 5, 'june': 6}

    #Filter DataFrame based on user inputs
    if month != 'all' and day != 'All':
        df = df[(df['month'] == month_convert[month]) & (df['weekday'] == day)]
    elif month != 'all':
        df = df[(df['month'] == month_convert[month])]
    elif day != 'All':
        df = df[(df['weekday'] == day)]
    else:
        None

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january','february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    print('Most common month:','\t'*2,months[df['month'].mode()[0] - 1].title())

    # TO DO: display the most common day of week
    print('Most common day of week:','\t'*1,df['weekday'].mode()[0].title())

    # TO DO: display the most common start hour
    print('Most common start hour:','\t'*1,df['Hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most common starting station:','\t'*1,df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('Most common ending station:', '\t'*2, df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    routes = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print('Most popular route:','\t'*2, ' -to- '.join(routes.index[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['True_Duration'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
            #Created True_Duration because I found inaccurate values in the given Trip_Duration column
    print('Total travel time:','\t'*2,df['True_Duration'].sum())

    # TO DO: display mean travel time
    print('Mean travel time:','\t'*2,df['True_Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    df['User Type'].fillna('No User Type specified',inplace = True)
    print('\nBREAKDOWN BY USER TYPE:\n', pd.value_counts(df['User Type'].values))

    # TO DO: Display counts of gender
    df['Gender'].fillna('No Gender specified', inplace = True)
    print('\nBREAKDOWN BY GENDER:\n',pd.value_counts(df['Gender'].values))

    # TO DO: Display earliest, most recent, and most common year of birth
    print('\nBIRTH YEAR DATA')
    print('Earliest birth year among users:','\t'*1, df['Birth Year'].min())
    print('Most recent birth year among users:', '\t'*1, df['Birth Year'].max())
    print('Most common birth year among users:','\t'*1,df['Birth Year'].mode()[0])

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

        #ask user if he/she'd like to restart or view raw data
        restart = input('\nWould you like to restart? Enter yes or no.\t')
        if restart.lower() != 'yes':
            dataview = input('\nWould you like to see the raw data for your current paramater selections? Enter yes or no.\n')
            i = 0
            p = 0  #number of lines user would like to view at one time
            if dataview == 'yes':
                p = int(input('How many lines would you like to view at time? (Enter an integer)\t'))
            while dataview == 'yes':
                print(df.iloc[i:i+p,1:9])
                #view next batch of lines
                i += p
                dataview = input('\n\n Would you like to see the next {} lines? yes or no     '.format(p))
            if input('\n\nWould you like to exit at this time? yes or no\t') != 'no':
                break


if __name__ == "__main__":
	main()
