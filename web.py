from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import re  # regular expression package

# Connect to database and create session
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Add new restaurantmenu
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data'"
                output += " action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text'"
                output += " placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            # Edit a restaurant name
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Search for the restaurant ID
                m = re.search('restaurants/(.+?)/edit', self.path)
                if m:
                    myID = int(m.group(1))
                    eRest = session.query(Restaurant).filter_by(id=myID).one()
                myAction = ('/restaurants/%d/edit' % (myID))
                print (eRest.name)
                output = ""
                output += "<html><body>"
                output += "<h1>Edit Restaurant Name</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data'"
                output += " action = "
                output += myAction
                output += "> <input name = 'editRestaurantName' type = 'text'"
                output += ' placeholder = "'
                output += eRest.name
                output += '"> <input type="submit" value="Update">'
                output += "</form></body></html>"
                print (output)
                self.wfile.write(output)
                return

            # Show all restaurants
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += '''<a href="/restaurants/new">Create a new
                  restaurant</a>'''
                output += "<h1>Restaurant List:</h1>"
                rests = session.query(Restaurant).all()
                for rest in rests:
                    editStr = ("/restaurants/%d/edit" % (rest.id))
                    output += "<p>"
                    output += rest.name
                    output += " "
                    output += ("<a href=%s>Edit</a>" % (editStr))
                    output += " "
                    output += '''<a href="#">Delete</a> '''
                    output += "</p>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # Handle POST form action for new restaurant
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                # Create new Restaurant Object
                print ("new rest name: " + messagecontent[0])
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                # Redirect back to restaurants page
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

            # Handle POST action for updating restaurant name
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('editRestaurantName')

                # Create new Restaurant Object
                # Search for the restaurant ID
                m = re.search('restaurants/(.+?)/edit', self.path)
                if m:
                    myID = int(m.group(1))
                    eRest = session.query(Restaurant).filter_by(id=myID).one()
                print ("updated rest name: " + messagecontent[0])
                eRest.name = messagecontent[0]
                session.add(eRest)
                session.commit()

                # Redirect back to restaurants page
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        except():
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print ("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()
