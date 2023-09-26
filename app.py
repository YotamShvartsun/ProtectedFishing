from dataclasses import dataclass, asdict
from typing import List
from enum import IntEnum
from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path='/', static_folder='static')

class URLStatusCode(IntEnum):
    SafeURL = 0
    Fishing = 1,
    UnsafeSite = 2

@dataclass
class URLStatus:
    is_safe: bool
    status_code: URLStatusCode

def validate_url(url: str) -> URLStatus:
    if 'www.' not in url:
        return URLStatus(False, URLStatusCode.UnsafeSite)
    if '.com' not in url:
        app.logger.error(url)
        return URLStatus(False, URLStatusCode.Fishing)
    return URLStatus(True, URLStatusCode.SafeURL)

@app.post('/check-url')
def check_url_status():
    request_body = dict(request.get_json())
    if 'url' not in request_body.keys():
        print('Invalid request')
        return jsonify({'message': 'No URL attribute in request!'}), 400
    status = validate_url(request_body['url'])
    result = {'url': request_body['url'], 'result': asdict(status)}
    return jsonify(result)

@app.get('/<path:path>')
def static_files(path):
    app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
