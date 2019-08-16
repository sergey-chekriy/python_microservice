#!/usr/bin/env python3
from http.server import HTTPServer,SimpleHTTPRequestHandler
from socketserver import BaseServer
import ssl
import re
import json
from ecdsa import SigningKey, SECP256k1
import sha3



def checksum_encode(addr_str): # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

keccak = sha3.keccak_256()

def new_wallet():
   keccak = sha3.keccak_256()
   priv = SigningKey.generate(curve=SECP256k1)
   pub = priv.get_verifying_key().to_string()
   keccak.update(pub)
   address = keccak.hexdigest()[24:]
   privkey = priv.to_string().hex()
   pubkey = pub.hex()
   addr = checksum_encode(address)
   data = [ { 'privkey':privkey, 'pubkey':pubkey,'addr':addr } ]
   data_string = json.dumps(data)
   return data_string




# HTTPRequestHandler class
class testHTTPServer_RequestHandler(SimpleHTTPRequestHandler):
 
  # GET
  def do_GET(self):
      if None != re.search('/new_wallet/*', self.path):
          self.send_response(200)
          self.send_header('Content-Type', 'application/json')
          self.end_headers()
          self.wfile.write(bytes(new_wallet(), "utf8"))

      else:
          
        # Send response status code
         self.send_response(200)
 
        # Send headers
         self.send_header('Content-type','text/html')
         self.end_headers()
 
        # Send message back to client
         message = "wrong request"
        # Write content as utf-8 data
         self.wfile.write(bytes(message, "utf8"))
         return
 
def run():
  print('starting server...')
  httpd = HTTPServer(('0.0.0.0', 1445), testHTTPServer_RequestHandler)
  httpd.socket = ssl.wrap_socket (httpd.socket, keyfile='/etc/letsencrypt/live/wallet.i-chain.net/privkey.pem',certfile='/etc/letsencrypt/live/wallet.i-chain.net/fullchain.pem', server_side=True)
  print('running server...')
  httpd.serve_forever()
 
 
run()
