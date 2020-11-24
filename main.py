from flask import Flask, Response
from gci import MyGCI
import os
from cachetools import cached, LRUCache, TTLCache

username = os.environ['gci_username']
password = os.environ['gci_password']

app = Flask(__name__)

@cached(cache=TTLCache(maxsize=1024, ttl=14400))
def cached_usage():
    return Response(MyGCI().getUsage(username, password), mimetype='text/plain')

@app.route('/')
def landing_page():
    return '<h1>MyGCI Exporter</h1><a href="/metrics">/metrics</a>'

@app.route('/metrics/')
def get_usage():
    return cached_usage()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9769)