from logging import getLogger
from unittest import TestCase

import requests


logger = getLogger(__name__)
BASE_URL = "http://calendar:8123"


def get_calendar(calendar, **params):
    # This will insert the number of the calendar into the url
    url = BASE_URL + "/calendars/{}/dates/".format(calendar)

    # This will send the request and return the response
    return requests.get(url, params=params)


def add_date(calendar, **data):
    url = BASE_URL + "/calendars/{}/".format(calendar)
    return requests.post(url, data=data)


class Base(TestCase):

    def setUp(self):
        super().setUp()
        requests.get(BASE_URL + "/reset_calendars")


class TestGetCalendar(Base):

    def setUp(self):
        super().setUp()

    def test_calendar_not_found(self):
        """
        This tests validates that we return an error for non-existing calendars
        """
        response = get_calendar(1000)

        # Checking the status code
        self.assertEqual(response.status_code, 404)

        # Checking the response itself
        self.assertEqual(response.json(), {})

    def test_get_empty_calendar(self):
        """
        This tests validates that we return an empty dict when a calendar is empty
        """
        response = get_calendar(0)

        # Checking the status code
        self.assertEqual(response.status_code, 200)

        # Checking the response itself
        self.assertEqual(response.json(), {})

    def test_get_calendar_with_data(self):
        response = get_calendar(1)
        data = {
            "2018-01-01": "Go fishing",
            "2018-01-11": "Go surfing",
            "2018-02-12": "Go skying",
            "2018-03-09": "Go swimming",
        }

        # Checking the status code
        self.assertEqual(response.status_code, 200)

        # Checking the response itself
        self.assertEqual(response.json(), data)


class TestAddEntry(Base):

    def test_add_event_to_available_date(self):
        """
        In this test, we'll heck that adding a date correctly returns a 201 status code
        and that the date is added
        """
        response = add_date(calendar=1, date="2019-10-10", event="Go hiking")
        # Checking the status code
        self.assertEqual(response.status_code, 201)

        # Confirmation that the entry has been added to the db
        all_dates = get_calendar(1).json()
        self.assertIn("2019-10-10", all_dates)

    def test_error_409_adding_event_when_date_is_taken(self):
        """
        In this test, we'll check that when we try to add an event to a date that
        already contain an event, we get an error with status 409, and the new event
        is not added.
        """
        # @todo: Write your test code here. Test it with calendar #1
        raise NotImplementedError("This test has yet to be implemented.")

    def test_error_404_adding_date_to_non_existing_calendar(self):
        """
        In this test, we'll check that if we try to add an event to a calendar that does
        not exist, we get an error with status 404, and the new event is not added.
        """
        # @todo: Write your test code here. Test it with calendar #1
        response = add_date(calendar=32, date="2018-01-11", event="Nomnomnom")

        self.assertEqual(response.status, 404)
        # raise NotImplementedError("This test has yet to be implemented.")
