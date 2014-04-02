import urllib
import urllib.parse
import urllib.request
import time
import json

class requester:
   def __init__(self):

      self.base_url = 'http://ws.spotify.com/'
      self.lookup = 'lookup/1/'
      self.search = 'search/1/'

   def build_query(self, path, searchType, searchTerm, page):

      url = self.base_url + path + searchType + '.json'
      data = {}
      data['q'] = searchType + ':' + searchTerm
      data['page'] = page

      url_values = urllib.parse.urlencode(data)
      
      full_url = url + '?' + url_values

      return full_url

   def perform(self, path, args):
      url = self.build_query(path, args['type'], args['terms'], args['page'])

      success = 0
      while success == 0:
         try:
            res = urllib.request.urlopen(url)
            success = 1
         except urllib.request.HTTPError as e:
            print(time.ctime() + ': HTTPError')
            time.sleep(5)
         except urllib.request.URLError:
            print(time.ctime() + ': URLError')
            time.sleep(5)
         
      return res.read().decode('utf-8')
      
      
