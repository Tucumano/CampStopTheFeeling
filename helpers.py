"""Helper objects and functions."""
from dataclasses import dataclass
from datetime import date


@dataclass
class DateRange:
    """Wrapper around a date range for booking a campsite."""
    check_in: date
    check_out: date

    @property
    def total_nights(self):
        return (self.check_out - self.check_in).days

    def get_unique_year_month_combinations(self):
        """Get the different years & months spanned by the check in and check out dates.

        Returns:
            list: Each element in the list is a tuple of length two containing the year and month.

        """
        year_month_pairs = {
            (self.check_in.year, self.check_in.month),
            (self.check_out.year, self.check_out.month)
        }

        return list(year_month_pairs)


@dataclass
class CampgroundAvailability:
    """Wrapper around the availability results data."""