#!/usr/bin/env python3

import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

analyzer = None

class LocationAnalyzer():
  def __init__(self, filepath):
    self.data = []

    if not os.path.isfile(filepath):
      raise FileNotFoundError('Data file does not exist.')

    with open(filepath) as f:
      lines = f.read().split('\n')

    num_succ = 0
    num_err = 0
    try:
      for line in lines:
        self.data.append(json.loads(line))
        num_succ += 1
    except:
      num_err += 1

    print(len(self.data))
    print(self.get_bounds())

    print('Successfully imported %i items, %i failed to load' % (num_succ, num_err))

  def get_bounds(self, padding=0.0):
    min_lat=90
    min_long=180
    max_lat=-90
    max_long=-180

    for loc in self.data:
      if 'gps' in loc:
        min_lat = min(min_lat, loc['gps']['latitude'])
        min_long = min(min_long, loc['gps']['longitude'])
        max_lat = max(max_lat, loc['gps']['latitude'])
        max_long = max(max_long, loc['gps']['longitude'])

      if 'network' in loc:
        min_lat = min(min_lat, loc['network']['latitude'])
        min_long = min(min_long, loc['network']['longitude'])
        max_lat = max(max_lat, loc['network']['latitude'])
        max_long = max(max_long, loc['network']['longitude'])

    return [ [min_lat + padding, min_long + padding], [max_lat + padding, max_long + padding] ]

  def get_loc_by_time(dtime):
    pass

class S(BaseHTTPRequestHandler):
  def _set_response(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()

  def _set_response_json(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_GET(self):
    print(self.path)

    if self.path == '/api/bounds':
      self.wfile.write(json.dumps(analyzer.get_bounds()).encode('utf-8'))
      print('TESTSETSET')
    self._set_response()
    self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

  def do_POST(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length) # <--- Gets the data itself
    logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
            str(self.path), str(self.headers), post_data.decode('utf-8'))

    self._set_response_json()

    if self.path == '/api/bounds':
      print('HIER')
      self.wfile.write(json.dumps({}).encode('utf-8'))
    else:
      test = {}
      test['data'] = 'example'
      test['cool'] = True
      self.wfile.write(json.dumps(test).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
  logging.basicConfig(level=logging.INFO)
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  logging.info('Starting httpd...\n')

  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      pass
  httpd.server_close()
  logging.info('Stopping httpd...\n')

if __name__ == '__main__':
  from sys import argv

  analyzer = LocationAnalyzer('gps_2018-04-14.txt')

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()
