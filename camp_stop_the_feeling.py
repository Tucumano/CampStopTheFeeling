"""Pull campsite availability data."""
from datetime import date, datetime

import requests

import constants
from helpers import DateRange

MIKES_CHANNEL_ISLANDS_DATES = [
    DateRange(check_in=date(2020, 11, 4), check_out=date(2020, 11, 7)),
    DateRange(check_in=date(2020, 12, 4), check_out=date(2020, 12, 6))
]

CONFIG = {
    'Santa Rosa Island': {
        'facility_id': 232497,
        'date_ranges': MIKES_CHANNEL_ISLANDS_DATES
    },
    'Santa Cruz Scorpion': {
        'facility_id': 232498,
        'date_ranges': MIKES_CHANNEL_ISLANDS_DATES,
        'campsites': [4926, 4927, 4928]
    }
}


def request_availability_data(facility_id, year, month):
    """Get campground availability data for a single month.

    Args:
        facility_id (int): The campground/facility_id value.
        year (int): The year for the request.
        month (int): The month for the request.

    Returns:
        dict: Where keys are the campsite IDs and values contain availability and misc info about the campsite.

    """
    request_url = constants.URL_TEMPLATE_MONTHLY_AVAILABILITY.format(facility_id=facility_id)

    # The API returns data for the whole month and requires the day to be the first.
    start_date_string = date(year, month, 1).strftime(constants.UTC_TIME_FORMAT)
    request_parameters = {'start_date': start_date_string}

    response = requests.get(request_url,
                            params=request_parameters,
                            headers=constants.AVAILABILITY_REQUEST_HEADERS)

    return response.json()['campsites']


def get_campground_availability(facility_id, date_range):
    """Return availability data for a single campground for the given date range.

    Args:
        facility_id (int): The campground/facility_id value.
        date_range (DateRange): The date range we're interested in.

    """
    # If the date range spans multiple months, we'll need to hit the API once for each month's availability.
    year_month_pairs = date_range.get_unique_year_month_combinations()

    campsite_availability_info = {}
    for (year, month) in year_month_pairs:

        campsite_availability = request_availability_data(facility_id, year, month)
        for campsite, campsite_data in campsite_availability.items():

            if campsite not in campsite_availability_info:
                # If we haven't encountered this campsite in a prior loop, add its info to the info dict
                campsite_availability_info[campsite] = campsite_data
            else:
                # If we've encountered it, combine its `availabilities` dict with additional data.
                campsite_availability_info[campsite]['availabilities'].update(campsite_data['availabilities'])

    return campsite_availability_info


def convert_dates(campsite_availability_info):
    pass  # pylint: disable=unnecessary-pass
    '''
    d = '2020-11-27T00:00:00Z'
    format = '%Y-%m-%dT%H:%M:%SZ'

    date_object = datetime.strptime(d, format).date()
    date_object2 = date(2020,11,27)

    print(f'formatted date: {date_object}')'''


def main():
    """Loop through each campground/facility in CONFIG and check availability.

    Example availability URL:
    - https://www.recreation.gov/api/camps/availability/campground/234038/month?start_date=2020-11-01T00%3A00%3A00.000Z

    """
    for name, campground_info in CONFIG.items():

        # Loop over each defined date range for the campground.
        for date_range in campground_info['date_ranges']:

            campsite_availability_info = get_campground_availability(campground_info['facility_id'], date_range)

            convert_dates(campsite_availability_info)

            # TODO: write a function that returns campsite ID & info  # pylint: disable=fixme

            print('\n--- Availability Information ---')
            print(f'{name} - Check in: {date_range.check_in}  Check out: {date_range.check_out}')

            # We still need to filter down the returned campsite availability info to the specific dates requested.
            # Right now we have it for the entire month(s) and it's not filtered down to only available days.

            # MDG's best attempt to pull open availability
            print('\n--- Open Availability ---')
            for site, site_info in campsite_availability_info.items():

                print(f'Site:{site} Available on:')

                avail = site_info['availabilities']

                for d, status in avail.items():
                    if status == 'Available':
                        print(f'{d}')

        # print(f'Unfiltered campsite availability:\n{campsite_availability_info}')


if __name__ == '__main__':
    main()
