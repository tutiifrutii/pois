from http.server import HTTPServer, BaseHTTPRequestHandler
from html.parser import HTMLParser
import re
import urllib.parse


APP_HOST = '127.0.0.1'
APP_PORT = 133


def parse_images(file, search_text):
    result = []
    tag_pattern = r'([a-zA-Z][^\t\n\r\f />\x00]*)'
    alt_pattern = r'alt="(.*)"'
    img_pattern = r'([-\w]+\.(?:jpg|gif|png|webp))'

    with open(file, 'r') as HTML_file:
        for raw in HTML_file:
            tag = re.findall(tag_pattern, raw, re.IGNORECASE)
            if len(tag) > 0:
                if tag[0] == 'img':
                    alt_attribute = re.findall(alt_pattern, raw, re.IGNORECASE)
                    if alt_attribute[0] != '':
                        alt_text = alt_attribute[0]
                        print(alt_text)

                        if search_text == alt_text:
                            result.append(raw)
                    else:
                        src_file = re.findall(img_pattern, raw, re.IGNORECASE)
                        if search_text == src_file[0].split('.')[0]:
                            result.append(raw)
    return ''.join(result)


class SimpleGetHandler(BaseHTTPRequestHandler):
    __image = None

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        if self.path == '/index.html':
            try:
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
                self.end_headers()
                image_tag = 'Image not found' if SimpleGetHandler.__image is None or SimpleGetHandler.__image == '' else SimpleGetHandler.__image
                self.wfile.write(bytes(file_to_open.format(image=image_tag), 'utf-8'))
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 - Not Found')
        else:
            self.send_response(200)
            self.end_headers()
            with open(self.path[1:], 'rb') as file:
                content = file.read()
            self.wfile.write(content)

    def do_POST(self):
        if self.path.startswith('/search'):
            search_text = urllib.parse.unquote(self.path.split('?')[1])
            SimpleGetHandler.__image = parse_images('images.html', search_text).strip()
            self.send_response(200)
            self.end_headers()



# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print("Start tag:", tag)
#         for attr in attrs:
#             print("     attr:", attr)
# parser = MyHTMLParser()


def run_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (APP_HOST, APP_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run_server(handler_class=SimpleGetHandler)