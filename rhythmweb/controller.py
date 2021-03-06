
from collections import defaultdict

from rhythmweb.model import get_song, get_playlist
from rhythmweb.rb import RBHandler, RBEntry
from rhythmweb import rb

import logging
log = logging.getLogger(__name__)

rb_handler = {}

def set_shell(shell):
    rb_handler['rb'] = RBHandler(shell)
    rb_handler['shell'] = shell

def get_handler():
    return rb_handler.get('rb', None)

def get_shell():
    return rb_handler.get('shell', None)

class Song(object):

    def __init__(self):
        self.rb = get_handler()

    def find_by_id(self, song_id):
        entry = self.rb.get_entry(song_id)
        if not entry:
            return None
        log.debug('Found song %d', song_id)
        return get_song(entry)

    def rate(self, song):
        self.set_rating(song, song['rating'])

    def set_rating(self, song, rating):
        song_id = song['id']
        self.rb.set_rating(song_id, rating)
        song['rating'] = rating
        log.debug('Song %d rated as %d', song_id, rating)


class Queue(object):

    def __init__(self):
        self.rb = get_handler()
        self.queue = rb.Queue(get_shell())

    def get_queue(self):
        entries = self.queue.get_play_queue()
        queue = defaultdict(lambda:[])
        for entry in entries:
            queue['entries'].append(get_song(entry))
        return queue

    def enqueue(self, entry_id):
        self.queue.enqueue(as_list(entry_id))

    def dequeue(self, entry_id):
        self.queue.dequeue(as_list(entry_id))

    def shuffle_queue(self):
        self.queue.shuffle_queue()

    def clear_queue(self):
        self.queue.clear_play_queue()


class Player(object):

    def __init__(self):
        self.rb = get_handler()

    def next(self):
        self.rb.play_next()

    def previous(self):
        self.rb.previous()

    def play_pause(self):
        self.rb.play_pause()

    def seek(self, time=0):
        self.rb.seek(time)

    def play_entry(self, entry_id=None):
        self.rb.play_entry(entry_id)

    def mute(self):
        self.rb.toggle_mute()

    def set_volume(self, volume=1.0):
        self.rb.set_volume(volume)

    def status(self):
        status = {}
        handler = self.rb
        status['playing'] = handler.get_playing_status()
        if status['playing']:
            playing_entry = handler.get_playing_entry()
            if playing_entry:
                status['playing_entry'] = get_song(playing_entry)
                status['playing_time'] = handler.get_playing_time()
        status['playing_order'] = handler.get_play_order()
        status['muted'] = handler.get_mute()
        status['volume'] = handler.get_volume()
        return status


def query_library(what):
    log.debug('Looking for library %s', what)
    return getattr(get_handler().library, what, {})


class Query(object):

    def __init__(self):
        self.rb = get_handler()

    def query(self, query_filter):
        entries = defaultdict(lambda: [])
        for entry in self.rb.query(query_filter):
            entries['entries'].append(get_song(entry))
        return entries


class Source(object):

    def __init__(self):
        self.rb = get_handler()

    def get_sources(self):
        return self.rb.get_playlists()

    def get_source(self, source_id):
        sources = self.rb.get_playlists()
        source = sources[source_id] if sources else None
        if source:
            self.rb.load_source_entries(source)
        return source

    def enqueue_by_id(self, source_id):
        playlist = self.get_source(source_id) 
        if not playlist:
            return None
        return self.rb.enqueue_source(playlist)

    def play_source(self, source_id):
        source = self.get_source(source_id)
        if not source:
            return False
        return self.rb.play_source(source)

    def get_playlist(self, playlist_id):
        return get_playlist(self.get_source(playlist_id))

    def get_playlists(self):
        return [get_playlist(source) for source in self.get_sources()]


def as_list(value):
    value = [value] if not isinstance(value, list) else value
    return value
