#!/usr/bin/env python
# Server and HTTP Handler
from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class: handle GET, POST, other verbs
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        print (message)
        return


def run():
    try:
        print('starting server...')

        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http
        #   server, you need root access
        port = 8080
        server_address = ('127.0.0.1', port)
        httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        print('running server on localhost, port', port)
        httpd.serve_forever()
    # except (KeyboardInterrupt, SystemExit):
    #     print ("^C enterened, stopping web server...")
    #     httpd.shutdown()
    #     raise
    except ():
        print ("caught an error")


def main():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http
    #   server, you need root access
    port = 8080
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server on localhost, port', port)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
