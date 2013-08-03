import socket
import SocketServer
import ssl
import pickle
import xmlrpclib
import SimpleXMLRPCServer 
import BaseHTTPServer
import math
import requests, json, webbrowser, time, sys, math, logging, types, string, os
from pprint import pprint
import urllib

import BeautifulSoup



try:
    import fcntl
except ImportError:
    fcntl = None

#    Easiest way to create the key file pair was to use OpenSSL -- http://openssl.org/ Windows binaries are available
#    You can create a self-signed certificate easily "openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout privatekey.pem"
#    for more information --  http://docs.python.org/library/ssl.html#ssl-certificates
KEYFILE='hostkey.pem'    # Replace with your PEM formatted key file
CERTFILE='hostcert.pem'  # Replace with your PEM formatted certificate file

userPassDict = {"shemer77":"boktai2",
                "jsmith":"hellow"}
    
class SimpleXMLRPCServerTLS(BaseHTTPServer.HTTPServer,SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    def __init__(self, addr, requestHandler=SimpleXMLRPCServer.SimpleXMLRPCRequestHandler,
                 logRequests=True, allow_none=False, encoding=None, bind_and_activate=True):
        """Overriding __init__ method of the SimpleXMLRPCServer

        The method is an exact copy, except the TCPServer __init__
        call, which is rewritten using TLS
        """
        self.logRequests = logRequests

        SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self, allow_none, encoding)

        """This is the modified part. Original code was:

            socketserver.TCPServer.__init__(self, addr, requestHandler, bind_and_activate)

        which executed:

            def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
                BaseServer.__init__(self, server_address, RequestHandlerClass)
                self.socket = socket.socket(self.address_family,
                                            self.socket_type)
                if bind_and_activate:
                    self.server_bind()
                    self.server_activate()

        """
        
        class VerifyingRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
            '''
            Request Handler that verifies username and password passed to
            XML RPC server in HTTP URL sent by client.
            '''
            # this is the method we must override
            def parse_request(self):
                # first, call the original implementation which returns
                # True if all OK so far
                if SimpleXMLRPCServer.SimpleXMLRPCRequestHandler.parse_request(self):
                    # next we authenticate
                    if self.authenticate(self.headers):
                        return True
                    else:
                        # if authentication fails, tell the client
                        self.send_error(401, 'Authentication failed')
                return False
            
            def authenticate(self, headers):
                from base64 import b64decode
                #    Confirm that Authorization header is set to Basic
                (basic, _, encoded) = headers.get('Authorization').partition(' ')
                assert basic == 'Basic', 'Only basic authentication supported'
                
                #    Encoded portion of the header is a string
                #    Need to convert to bytestring
                encodedByteString = encoded.encode()
                #    Decode Base64 byte String to a decoded Byte String
                decodedBytes = b64decode(encodedByteString)
                #    Convert from byte string to a regular String
                decodedString = decodedBytes.decode()
                #    Get the username and password from the string
                (username, _, password) = decodedString.partition(':')
                #    Check that username and password match internal global dictionary
                if username in userPassDict:
                    if userPassDict[username] == password:
                        return True
                return False
        
        #    Override the normal socket methods with an SSL socket
        SocketServer.BaseServer.__init__(self, addr, VerifyingRequestHandler)
        self.socket = ssl.wrap_socket(
            socket.socket(self.address_family, self.socket_type),
            server_side=True,
            keyfile=KEYFILE,
            certfile=CERTFILE,
            cert_reqs=ssl.CERT_NONE,
            ssl_version=ssl.PROTOCOL_SSLv23,
            )
        if bind_and_activate:
            self.server_bind()
            self.server_activate()

        # [Bug #1222790] If possible, set close-on-exec flag; if a
        # method spawns a subprocess, the subprocess shouldn't have
        # the listening socket open.
        if fcntl is not None and hasattr(fcntl, 'FD_CLOEXEC'):
            flags = fcntl.fcntl(self.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(self.fileno(), fcntl.F_SETFD, flags)

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def executeRpcServer():
    # Create server
    server = SimpleXMLRPCServerTLS(("108.61.63.199", 8000), requestHandler=RequestHandler, allow_none=True)
    server.register_introspection_functions()

   
    class MyFuncs:
        def cancel(self,item_id,listing_id,char_id,session_key):
            google = 'https://tradingpost-live.ncplatform.net/ws/item/'+str(item_id)+'/cancel.json'+'?'+'listing='+str(listing_id)+'&isbuy=1&charid='+char_id
            print google
            headers = {'Cookie': 's='+session_key,'Referer': 'https://tradingpost-live.ncplatform.net/me'}
            print headers
            r5 = requests.post(google, headers = headers)
            print r5

        def buy(self,item_id,amount,price,char_id,session_key):
            yolo = 'https://tradingpost-live.ncplatform.net/ws/item/'+str(item_id)+'/buy'+'?'+'count='+str(amount)+'&price='+str(price)+'&charid='+char_id
            print yolo
            headers = {'Cookie': 's='+session_key,'Referer': 'https://tradingpost-live.ncplatform.net/me'}
            print headers
            r6 = requests.post(yolo, headers = headers)
            print r6

        def increase_coord(self,l,ycoordfirstitem,ycoordremoveitem,xcoordfirstitem,xcoordremoveitem,removeitempages,pages,pagecounter):
            if l <= 7:
                ycoordfirstitem += 48
                ycoordremoveitem += 48
                l += 1
                
            elif l == 8:
                removeitempages = 1
                ycoordfirstitem += 48
                ycoordremoveitem += 48 
                l += 1
                
            else:
                xcoordfirstitem = 250
                ycoordfirstitem = 151
                xcoordremoveitem = 96
                ycoordremoveitem = 154
                time.sleep(1)
                pages += 1
                pagecounter +=1
                #ichanged l = 1 to 0 
                l = 0
            return l,ycoordfirstitem,ycoordremoveitem,xcoordfirstitem,xcoordremoveitem,removeitempages,pages,pagecounter

    server.register_instance(MyFuncs())

    # Run the server's main loop
    print("Starting XML RPC Server")
    server.serve_forever()

if __name__ == '__main__':   
    executeRpcServer()
