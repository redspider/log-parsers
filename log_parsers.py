"""
Copyright (c) 2009, Richard Clark, Red Spider Limited <richard@redspider.co.nz>
See LICENSE file for details.

"""

from datetime import datetime, tzinfo
import re

class InvalidFormat(Exception):
    pass

class CommonLogEntry(object):
    """ Parses an Apache Common Log Entry line
        Does not deal with Timezones.
    """
    ip = None
    ident = None
    auth = None
    _date_time = None
    _date_time_cached = None
    time_zone = None
    method = None
    path = None
    version = None
    code = None
    size = None
    referer = None
    user_agent = None
    
    def __init__(self, line):
        """ Create CLE from line """
        m = re.match(r'(\S+) (\S+) (\S+) \[(\S+) ([^\]]+)\] "(\S+) (\S+) ([^"]+)" (\d+) (\S+) "(.*)" "(.*)"', line)
        if not m:
            raise InvalidFormat(line)
        
        (self.ip, ident, auth, date_time, timezone, self.method, self.path, self.version, code, size, self.referer, self.user_agent) = m.groups()
        
        if ident != '-':
            self.ident = ident
        if auth != '-':
            self.auth = auth
        
        self._date_time = date_time
        self.time_zone = timezone
        
        self.code = int(code)
        if size != '-':
            self.size = int(size)
        
    def __str__(self):
        """ Return a string in CLE format """
        return '%s %s %s [%s %s] "%s %s %s" %d %s "%s" "%s"' % (self.ip, self.ident or '-', self.auth or '-', self.date_time.strftime('%d/%b/%Y:%H:%M:%S'), self.time_zone, self.method, self.path, self.version, self.code, str(self.size) or '-', self.referer, self.user_agent)

    def __getattr__(self, name):
        if name == 'date_time':
            if not self._date_time_cached:
                self._date_time_cached = datetime.strptime(self._date_time, '%d/%b/%Y:%H:%M:%S')
            return self._date_time_cached
        raise AttributeError('CommonLogEntry object has no attribute %s' % name)
            
