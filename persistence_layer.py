from abc import ABC, abstractmethod

from peewee_database import PeeweeDatabaseManager, Bookmarks


class PersistenceLayer(ABC):
    @abstractmethod
    def create(self, data: dict):
        raise NotImplementedError(
            'Слои постоянства должны реализовать метод create'
        )

    @abstractmethod
    def list(self, order_by=None):
        raise NotImplementedError(
            'Слои постоянства должны реализовать метод list'
        )

    @abstractmethod
    def edit(self, bookmark_id, bookmark_data):
        raise NotImplementedError(
            'Слои постоянства должны реализовать метод edit'
        )

    @abstractmethod
    def delete(self, bookmark_id):
        raise NotImplementedError(
            'Слои постоянства должны реализовать метод delete'
        )


class BookmarkDatabase(PersistenceLayer):
    def __init__(self):
        self.db = PeeweeDatabaseManager()

        self.db.create_table()

    def create(self, data: dict):
        self.db.add(data)

    def list(self, order_by=None):
        return self.db.select(order_by=order_by)

    def edit(self, bookmark_id, bookmark_data):
        bookmark: Bookmarks = Bookmarks.get_or_none(
            Bookmarks.id == bookmark_id
        )
        bookmark.title = bookmark_data['title']
        bookmark.url = bookmark_data['url']
        bookmark.notes = bookmark_data['notes']
        bookmark.date_added = bookmark_data['date_added']
        bookmark.save()

    def delete(self, bookmark_id):
        Bookmarks.delete_by_id(bookmark_id)
