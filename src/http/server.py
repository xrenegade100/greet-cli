from http.server import BaseHTTPRequestHandler
import json
from typing import List
from src.model.greetentity import AbstractGreetEntity
from src.utils.parser import Parser
from src.classifier.classifier import greetClassifier

class Server(BaseHTTPRequestHandler):
    
  def do_GET(self):
    if self.path == '/quit':
      exit(0)
    
    if self.path == '/status':
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps({'status': 'ok'}).encode())
      return

    return

  def do_POST(self):
    if self.path == '/predict':
      length = int(self.headers.get('content-length'))
      body = json.loads(self.rfile.read(length)) 
      # To avoid python complaining about `entities` type
      entities: List[AbstractGreetEntity] = []
      if body['code']:
          p = Parser(body['code'])
          p.parse_file()
          functions = p.get_functions() or []
          attributes = p.get_attributes() or []
          entities: List[AbstractGreetEntity] = [*functions, *attributes] 
      else:
          self.send_response(400)
          self.end_headers()
      result = []
      for entity in entities:
          entity.setIssue(greetClassifier.predict(entity))
          result.append({'code': f'{entity.getString()}', 'prediction': entity.getIssue(), 'linestart': entity.getStartLine(), 'lineend': entity.getEndLine(), 'colstart': entity.getStartColumn(), 'coleend': entity.getEndColumn()}) 
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      self.wfile.write(json.dumps(result).encode('utf-8'))
      # predict
    return