# -*- coding: utf-8 -
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

from serve.log.loggable import Loggable
from gi.repository import RB

class EntryHandler(Loggable):
    
    def __init__(self, shell):
        self.db = shell.props.db
        
        
    def get_entry(self, entry_id):
        '''
        Returns an entry by its id
        '''
        if not str(entry_id).isdigit():
            raise Exception('entry_id parameter must be an int')
        
        entry_id = int(entry_id)
        
        self.trace('Getting entry %d' % entry_id)
        return self.db.entry_lookup_by_id(entry_id)
        
        
    def load_rb_entry(self, entry_id):
        '''
        Returns a RBEntry with the entry information fully loaded for the given id 
        '''
        self.debug('Loading entry %s' % str(entry_id))
        entry = self.get_entry(entry_id)
        if entry is None:
            self.info('Entry %s not found' % str(entry_id))
            return None
        
        rbentry = RBEntry()
        rbentry.id = self.get_entry_id(entry)
        rbentry.title = entry.get_string(RB.RhythmDBPropType.TITLE) # self.get_value(entry, RB.RhythmDBPropType.TITLE)
        rbentry.artist = entry.get_string(RB.RhythmDBPropType.ARTIST) # self.get_value(entry, RB.RhythmDBPropType.ARTIST)
        rbentry.album = entry.get_string(RB.RhythmDBPropType.ALBUM)
        rbentry.track_number = entry.get_ulong(RB.RhythmDBPropType.TRACK_NUMBER)
        rbentry.duration = entry.get_ulong(RB.RhythmDBPropType.DURATION)
        rbentry.rating = entry.get_double(RB.RhythmDBPropType.RATING)
        rbentry.year = entry.get_ulong(RB.RhythmDBPropType.YEAR)
        rbentry.genre = entry.get_string(RB.RhythmDBPropType.GENRE)
        rbentry.play_count = entry.get_ulong(RB.RhythmDBPropType.PLAY_COUNT)
        rbentry.location = entry.get_string(RB.RhythmDBPropType.LOCATION)
        rbentry.bitrate = entry.get_ulong(RB.RhythmDBPropType.BITRATE)
        rbentry.last_played = entry.get_ulong(RB.RhythmDBPropType.LAST_PLAYED)
        
        return rbentry
    
    
    def set_rating(self, entry_id, rating):
        '''
        Sets the provided rating to the given entry id, int 0 to 5 
        '''
        if not type(rating) is int:
            raise Exception('Rating parameter must be an int')
        
        self.info('Setting rating %d to entry %s' % (rating, entry_id))
        entry = self.get_entry(entry_id)
        if not entry is None:
            self.db.entry_set(entry, RB.RhythmDBPropType.RATING, rating)
    
    
    def get_entry_id(self, entry):
        return entry.get_ulong(RB.RhythmDBPropType.ENTRY_ID)
    
    
#    def get_value(self, entry, property_type):
#        return entry.get_string(property_type)
#        
##
##        t = self.db.get_property_type(property_type)
##        value = GObject.Value()
##        value.init(t)
##        
##        self.db.entry_get(entry, property_type, value)
##        
##        entry.get_string(property_type)
##        
##        if t.name == 'gulong':
##            return value.get_ulong()
##            
##        elif t.name == 'gchararray':
##            return value.get_string()
##            
##        elif t.name == 'gboolean':
##            return value.get_boolean()
##            
##        elif t.name == 'gboxed':
##            return value.get_boxed()
##            
##        elif t.name == 'gchar':
##            return value.get_char()
##            
##        elif t.name == 'gdouble':
##            return value.get_double()
##            
##        elif t.name == 'genum':
##            return value.get_enum()
##            
##        elif t.name == 'gflags':
##            return value.get_flags()
##            
##        elif t.name == 'gfloat':
##            return value.get_float()
##            
##        elif t.name == 'gint':
##            return value.get_int()
##            
##        elif t.name == 'gint64':
##            return value.get_int64()
##            
##        elif t.name == 'glong':
##            return value.get_long()
##            
##        elif t.name == 'gobject':
##            return value.get_object()
##            
##        elif t.name == 'gparam':
##            return value.get_param()
##            
##        elif t.name == 'gpointer':
##            return value.get_pointer()
##            
##        elif t.name == 'gstring':
##            return value.get_string()
##            
##        elif t.name == 'guchar':
##            return value.get_uchar()
##            
##        elif t.name == 'guint':
##            return value.get_uint()
##            
##        elif t.name == 'guint64':
##            return value.get_uint64()
##            
##        elif t.name == 'gvariant':
##            return value.get_variant()
##            
##        else:
##            self.warning('Unknown type %s' % t.name)
##            return None


class RBEntry():
    '''
    Rhythmbox entry wrapper, loads all entry data on initialization
    '''
    def __init__(self):
        self.id = None
        self.artist = None
        self.album = None
        self.track_number = None
        self.title = None
        self.duration = None
        self.rating = None
        self.year = None
        self.genre = None
        self.play_count = None
        self.location = None
        self.bitrate = None
        self.last_played = None

