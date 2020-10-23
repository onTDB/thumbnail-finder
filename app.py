from flask import *
from flask_compress import Compress
import os
import ssl

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route('/')
def main():
    return render_template("main.html")

if __name__ == '__main__':
    app.debug = True
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.load_cert_chain(certfile='certfile.crt', keyfile='private.key', password='password')
    app.run(host="0.0.0.0", threaded=True, port=443, ssl_context=ssl_context)