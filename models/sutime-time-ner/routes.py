import os
import json
import logging

from sutime import SUTime
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Welcome to the Sutime Endpoint</h2>'

@app.route('/time', methods=['POST'])
def parse_time():
    query = request.json['query']
    logging.info(query)
    jar_files = "./jars/"
    sutime = SUTime(jars=jar_files, mark_time_ranges=True, include_range=True)
    result = sutime.parse(query)
    return json.dumps(result, sort_keys=True, indent=4)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)