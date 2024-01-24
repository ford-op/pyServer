#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import ssl
import time
import json
from socketserver import ThreadingMixIn
import threading

hostName = "0.0.0.0"
#serverPort = 443
serverPort = 8080
recordingsPath = "/recordings/"

LOGS = ["rlog"]
QLOGS = ["qlog"]
QCAMERAS = ["qcamera.ts"]

class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
    aPath = self.path.split("/")
    aDirs = []    

    jsonOut = {}

    if len(aPath) > 3 and aPath[2] == "route":
      cameras = []
      dcameras = []
      ecameras = []
      logs = []
      qcameras = []
      qlogs = []
      aRoute = aPath[3].split("%7C")
      dID = aRoute[0]
      route = aRoute[1]
      subFolders = os.walk(recordingsPath + "/" + route)
      for root, dirs, files in subFolders:
         for dir in dirs:
            if dir.startswith(route + "--"):
              aDirs.append(os.path.join(root, dir))
      if len(aDirs) > 0:
        aDirs.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))      
        for dir in aDirs:
          subFolders = os.walk(dir)          
          pos = dir.split("--")
          for root, dirs, files in subFolders:
            for file in files:
               if file in LOGS:
                  logs.append(f"http://localhost:{serverPort}/qlog/{dID}/{route}/{pos[-1]}/{file}")
               if file in QCAMERAS:
                  qcameras.append(f"http://localhost:{serverPort}/qlog/{dID}/{route}/{pos[-1]}/{file}")
               if file in QLOGS:
                  qlogs.append(f"http://localhost:{serverPort}/qlog/{dID}/{route}/{pos[-1]}/{file}")

        jsonOut['logs'] = logs
        jsonOut['qcameras'] = qcameras
        jsonOut['qlogs'] = qlogs

        
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write(bytes(json.dumps(jsonOut), "utf-8"))
    elif len(aPath) > 2 and aPath[1] == "qlog":
      file = os.path.join(recordingsPath, aPath[3], f"{aPath[3]}--{aPath[4]}", aPath[5])
      f = open(file, 'rb') 
      self.send_response(200)
      self.end_headers()
      self.wfile.write(f.read())
      f.close()

    else:
        self.send_response(404)

    return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

if __name__ == "__main__":
  webServer = ThreadedHTTPServer((hostName, serverPort), Handler)
  print("Server started http://%s:%s" % (hostName, serverPort))

  try:
      if serverPort == "443":
        webServer.socket = ssl.wrap_socket(webServer.socket, server_side=True)
      
      webServer.serve_forever()
  except KeyboardInterrupt:
      pass

  webServer.server_close()
  print("Server stopped.")