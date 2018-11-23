import json
from datetime import date
from pony.orm import Database, PrimaryKey, Set, Required


db = Database(provider='sqlite', filename='/database.sqlite', create_db=True)


class Calendar(db.Entity):
    id = PrimaryKey(int, auto=True)
    dates = Set('Date')
    title = Required(str, 128)

    def __str__(self):
        return "{}: {} ({} dates)".format(self.id, self.title, len(self.dates))

    def as_dict(self):
        data = dict(
            id=self.id, dates=[d.as_dict() for d in self.dates], title=self.title
        )
        return data


class Date(db.Entity):
    id = PrimaryKey(int, auto=True)
    calendar = Required(Calendar)
    date = Required(date)
    event = Required(str, 128)

    def __str__(self):
        return "{}.{}: {} {}".format(
            self.calendar.id, self.id, self.date, self.event
        )

    def as_dict(self):
        data = {str(self.date): self.event}
        return data


db.generate_mapping(create_tables=True)
