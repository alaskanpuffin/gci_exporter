from flask import Flask, Response
from gci import MyGCI
import os

username = os.environ['gci_username']
password = os.environ['gci_password']

app = Flask(__name__)

@app.route('/')
def landing_page():
    return '<h1>MyGCI Exporter</h1><a href="/metrics">/metrics</a>'

@app.route('/metrics/')
def get_usage():
    return Response(MyGCI().getUsage(username, password), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9769)