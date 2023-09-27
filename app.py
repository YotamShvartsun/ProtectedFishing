from dataclasses import dataclass, asdict
from typing import List
from enum import IntEnum
from flask import Flask, jsonify, request
from apis.dbs_bootstrapper import initialize_dbs
from apis.validate_url_service import URLValidator

app = Flask(__name__, static_url_path='/', static_folder='static')
dbFactory = initialize_dbs()
dbs = dbFactory.get_dbs()
urlValidator: URLValidator = URLValidator(dbs.values())

class URLStatusCode(IntEnum):
    SafeURL = 0
    Fishing = 1,
    UnsafeSite = 2

@dataclass
class URLStatus:
    is_safe: bool
    status_code: URLStatusCode

async def validate_url(url: str) -> URLStatus:
    return await urlValidator.validate_url(url)

@app.post('/check-url')
async def check_url_status():
    request_body = dict(request.get_json())
    if 'url' not in request_body.keys():
        print('Invalid request')
        return jsonify({'message': 'No URL attribute in request!'}), 400
    status = await validate_url(request_body['url'])
    result = {'url': request_body['url'], 'result': status}
    return jsonify(result)

@app.get('/<path:path>')
def static_files(path):
    app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
