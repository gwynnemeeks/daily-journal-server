from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from entries import get_all_entries, get_single_entry, delete_entry
from moods import get_all_moods, get_single_mood, delete_mood

class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
    # Set the response code to 'Ok'
        self._set_headers(200)

        # Your new console.log() that outputs to the terminal
        print(self.path)

         # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        print(id)

        if resource == "entries":
            if id is not None:
                response = f"{get_single_entry(id)}"
            else:
                response = f"{get_all_entries()}"
        elif resource == "moods":
            if id is not None:
                response = f"{get_single_mood(id)}"
            else:
                response = f"{get_all_moods()}"
        else:
            response = []

        self.wfile.write(response.encode())

    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        # Delete single entry and mood from the list
        if resource == "entries":
            delete_entry(id)
        elif resource == "moods":
            delete_mood(id)

        self.wfile.write("".encode())

def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()