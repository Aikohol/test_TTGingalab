from logging import getLogger

import hug
from falcon import HTTP_404, HTTP_201
from pony import orm

from models import Calendar, Date


logger = getLogger(__name__)


@hug.get('/reset_calendars')
def reset_calendars():
    """
    This function, used only for testing purposes, resets the calendars list to
    its initial states.
    :return: a simple status
    """
    # Removing all calendars and dates:
    with orm.db_session:
        # Deleting all dates and calendars
        Date.select().delete(bulk=True)
        Calendar.select().delete(bulk=True)

        # Creating sample calendars and dates
        Calendar(id=0, title="Empty calendar")
        c2 = Calendar(id=1, title="Sport and activities")
        Date(id=0, calendar=c2, date="2018-01-01", event="Go fishing")
        Date(id=1, calendar=c2, date="2018-01-11", event="Go surfing")
        Date(id=2, calendar=c2, date="2018-02-12", event="Go skying")
        Date(id=3, calendar=c2, date="2018-03-09", event="Go swimming")

    return dict(status="done")

@hug.post('/calendars/{calendar}/')
def add_date(response, calendar, date, event):
    with orm.db_session:
        if Calendar.get(id=calendar):
            calendar = Calendar.get(id=calendar)
            logger.warning("201")
            date = Date(calendar=calendar, date=date, event=event)
            response.status = HTTP_201
        else:
            logger.warning("404")
            response.status = HTTP_404
        return {}

@hug.get('/calendars/{calendar}/dates/')
def get_dates(response, calendar):

    with orm.db_session:
        # Deleting all dates and calendars
        calendar = Calendar.get(id=calendar)
        dates = {}
        try:
            calendar_dates = calendar.dates

        except AttributeError:
            # There are not dates for this calendar
            response.status = HTTP_404
            return {}

        for date in calendar_dates.order_by(Date.date):
            dates[str(date.date)] = date.event

        return dates
