from wsgiref.simple_server import make_server
from Web import application

httpd = make_server('', 8002, application)
print('Serving HTTP on port 8002')
httpd.serve_forever()