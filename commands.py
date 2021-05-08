import datetime
import sys

from peewee_database import PeeweeDatabaseManager, Bookmarks


db = PeeweeDatabaseManager()


class CreateBookmarkTableCommand:
    def execute(self) -> None:
        db.create_table()


class AddBookmarkCommand:
    def execute(self, data: dict):
        data['date_added'] = datetime.datetime.utcnow().isoformat()
        db.add(data)
        return 'Закладка добавлена'


class ListBookmarkCommand:
    def __init__(self, order_by=Bookmarks.date_added):
        self.order_by = order_by

    def execute(self):
        return [item for item in Bookmarks.select().order_by(self.order_by)]


class DeleteBookmarkCommand:
    def execute(self, data):
        db.delete({'id': data})
        return 'Bookmark deleted'


class QuitCommand:
    def execute(self):
        sys.exit()
