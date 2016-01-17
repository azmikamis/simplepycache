from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
import re
from threading import Thread, Timer, Event, Lock
import time
from pprint import pprint

keypattern = re.compile("^/\w+$")

cache = {}

lock = Lock()
        

class SweepCacheThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._stopEvent = Event()
        
    def run(self):
        while not self._stopEvent.isSet():
            current_time = time.time()
            
            expired = []
            for key, (_, expiry_time) in cache.iteritems():
                if expiry_time != -1 and current_time > expiry_time:
                    expired.append(key)

            lock.acquire()
            for k in expired:
                cache.pop(k, None)
            lock.release()
            
            print('{} Cached content'.format(
                time.strftime('%H:%M:%S', time.localtime(current_time))))
            pprint(cache)
            
            print('Expired keys:')
            pprint(expired)
            
            print
            self._stopEvent.wait(5.0)
        
    def stop(self):
        self._stopEvent.set()


class CacheHandler(BaseHTTPRequestHandler):

    def getKey(self,path):
        result = keypattern.match(self.path)
        if result:
            return result.group()[1:]
        else:
            print None
            
    def process(key):
        pass
        
    def do_GET(self):
        key = self.getKey(self.path)
        print('GET {}'.format(key))
        if key:
            if key in cache:
                value = cache[key][0]
                print('value {}'.format()
                self.wfile.write(value)
            else:
                self.wfile.write('NULL')
        
    def do_POST(self):
        rawdata = self.rfile.read(int(self.headers['Content-Length']))
        print rawdata
        data = json.loads(rawdata)
        key, value = data['key'], data['value']
        
        print('{} SET key={} value={}'.format(
            time.strftime('%H:%M:%S'), key, value))
        print
        
        lock.acquire()
        cache[key] = (value, -1)
        lock.release()
        
    def do_PUT(self):
        rawdata = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(rawdata)
        key, duration = data['key'], data['duration']
        
        print('{} EXPIRE key={} duration={}'.format(
            time.strftime('%H:%M:%S'), key, duration))
        expiry_time = time.time()+int(duration)
        print('{} will expire at {}'.format(
            key, time.strftime('%H:%M:%S', time.localtime(expiry_time))))
        print
        
        if key in cache:
            lock.acquire()
            cache[key] = (cache[key][0], expiry_time)
            lock.release()

            
def run():
    try:
        sweepCacheThread = SweepCacheThread()
        sweepCacheThread.start()
        
        server = HTTPServer(('localhost', 8000), CacheHandler)
        server.serve_forever()
        print 'Server started'
    except KeyboardInterrupt:
        sweepCacheThread.stop()
        sweepCacheThread.join()
        
        print 'Shutting down server'
        server.socket.close()


run()
