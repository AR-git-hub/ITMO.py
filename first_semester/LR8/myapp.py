from http.server import HTTPServer
from server import SimpleHTTPRequestHandler

if __name__ == '__main__':
    PORT = 8080
    httpd = HTTPServer(('localhost', PORT), SimpleHTTPRequestHandler)
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()


