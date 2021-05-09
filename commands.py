import datetime
import sys
from abc import ABC, abstractmethod

import requests

from peewee_database import PeeweeDatabaseManager, Bookmarks


db = PeeweeDatabaseManager()


class Command:
    @abstractmethod
    def execute(self, data):
        pass


class CreateBookmarkTableCommand(Command):
    def execute(self, data=None) -> None:
        db.create_table()


class AddBookmarkCommand(Command):
    def execute(self, data: dict, timestamp=None):
        data['date_added'] = timestamp or datetime.datetime.utcnow().isoformat()
        db.add(data)
        return 'Закладка добавлена'


class ListBookmarkCommand(Command):
    def __init__(self, order_by=Bookmarks.date_added):
        self.order_by = order_by

    def execute(self, data=None):
        return [
            f'{item.id}: {item.title}'
            for item in Bookmarks.select().order_by(self.order_by)
        ]


class DeleteBookmarkCommand(Command):
    def execute(self, data: str):
        db.delete({'id': data})
        return 'Bookmark deleted'


class EditBookmarkCommand(Command):
    def execute(self, data: dict):
        bookmark: Bookmarks = Bookmarks.get_or_none(
            Bookmarks.id == data['id']
        )

        if bookmark:
            bookmark.title = data['title']
            bookmark.url = data['url']
            bookmark.notes = data['notes']
            bookmark.save()
            return 'Bookmark updated'


class ImportGithubStarsCommand(Command):
    def _extract_bookmark_info(self, repo: dict):
        return {
            'title': repo['name'],
            'url': repo['html_url'],
            'notes': repo['description'],
        }

    def execute(self, data: dict):
        bookmarks_imported = 0

        github_username = data['github_username']
        next_page_of_results = \
            f'https://api.github.com/users/{github_username}/starred'
        while next_page_of_results:
            stars_response = requests.get(
                next_page_of_results,
                headers={
                    'Accept': 'application/vnd.github.v3.star+json'
                },
            )
            next_page_of_results = stars_response.links.get(
                'next', {}
            ).get('url')

            for repo_info in stars_response.json():
                repo = repo_info['repo']

                if data['preserve_timestamps']:
                    timestamp = datetime.datetime.strptime(
                        repo_info['starred_at'],
                        '%Y-%m-%dT%H:%M:%SZ'
                    )
                else:
                    timestamp = None

                bookmarks_imported += 1

                AddBookmarkCommand().execute(
                    self._extract_bookmark_info(repo),
                    timestamp=timestamp
                )
        return f'Импортировано {bookmarks_imported} закладок'


class QuitCommand(Command):
    def execute(self, data=None):
        sys.exit()
