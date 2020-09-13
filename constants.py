"""Constants."""

URL_TEMPLATE_MONTHLY_AVAILABILITY = 'https://www.recreation.gov/api/camps/availability/campground/{facility_id}/month'


AVAILABILITY_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}
UTC_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'