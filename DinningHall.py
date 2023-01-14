from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class DinningHall(BaseHTTPRequestHandler):

    def _send_response(self, message):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        if self.path == '/produce':
            # Produce data on multiple threads
            threads = []
            for i in range(5):
                t = threading.Thread(target=self.produce_data)
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            self._send_response('Data produced')
        else:
            self._send_response('Invalid request')

    def produce_data(self):
        # Produce data and send to Server 2
        data = ...
        self.send_to_server2(data)

    def send_to_server2(self, data):
        # Send data to Server 2 over HTTP
        conn = http.client.HTTPConnection('server2:8000')
        conn.request("POST", "/consume", json.dumps(data))

def run():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, DinningHall)
    print('Starting producer server...')
    httpd.serve_forever()

run()