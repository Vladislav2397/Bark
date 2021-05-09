from peewee import (
    SqliteDatabase, Model, CharField, TextField
)

db = SqliteDatabase('bookmarks.db')


class Bookmarks(Model):
    title = CharField()
    url = TextField()
    notes = TextField(null=True)
    date_added = CharField()

    class Meta:
        database = db


class PeeweeDatabaseManager:
    def __init__(self):
        self.db = db

    def __del__(self):
        self.db.close()

    def create_table(self):
        with self.db:
            self.db.create_tables([Bookmarks])

    def add(self, data: dict):
        with self.db:
            m = Bookmarks.create(
                title=data['title'],
                url=data['url'],
                notes=data['notes'],
                date_added=data['date_added']
            )
            m.save()

    def delete(self, criteria: dict):
        Bookmarks.delete_by_id(criteria['id'])

    def select(self, criteria: dict = None, order_by=None):
        if criteria:
            return Bookmarks.select(criteria).order_by(order_by)
        return Bookmarks.select().order_by(order_by)


with db:
    db.create_tables([Bookmarks])
