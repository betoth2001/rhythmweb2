# Rhythmweb - Rhythmbox web REST + Ajax environment for remote control
# Copyright (C) 2010  Pablo Carranza
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from serve.rest.base import BaseRest
from serve.log.loggable import Loggable
from serve.rest.json import JSon
from web.rest import Playlist, Song
from serve.request import ServerException

class Page(BaseRest, Loggable):
    
    def get(self):
        handler = self._components['RB']
        
        if self._path_params is None:
            rbplaylists = handler.get_playlists()
            sources = []
            for source in rbplaylists:
                jsource = Playlist.get_playlist_as_JSon(source)
                sources.append(jsource)
                
            playlists = JSon()
            playlists.put('playlists', sources)
            
            return playlists
        
        else:
            playlist_id = self._path_params[0]
            self.debug('Playlist id %s' % playlist_id)
            if not playlist_id.isdigit():
                raise ServerException(400, 'Bad request, path parameter must be an int')
            
            playlist_id = int(playlist_id)
            playlist = handler.get_playlist(playlist_id)
            if playlist is None:
                raise ServerException(400, 'Bad request, playlist id %d is not valid' % playlist_id)
            
            jplaylist = Playlist.get_playlist_as_JSon(playlist, self.get_playlist_entries(playlist_id))
            
            return jplaylist
            
    
    def post(self):
        params = self._parameters
        
        if not params:
            raise ServerException(400, 'Bad request, no parameters')

        if not 'action' in params:
            raise ServerException(400, 'Bad request, no action parameter')
        
        handler = self._components['RB']
        action = self.unpack_value(params['action'])
        
        json = JSon()
        
        if action == 'enqueue':
            if not 'playlist' in params:
                raise ServerException(400, 'Bad request, no playlist parameter to enqueue')
            
            playlist = self.unpack_value(params['playlist'])
            count = handler.enqueue_playlist(int(playlist))
            json.put('count', count)
            if count > 0:
                json.put('result', 'OK')
            
        return json


    def get_playlist_entries(self, id):
        handler = self._components['RB']
        entry_ids = handler.get_playlist_entries(id)
        
        entries = []
        for id in entry_ids:
            entry = Song.get_song_as_JSon(handler, id)
            entries.append(entry)
            
        return entries