from dataclasses import dataclass
from enum import IntEnum
from flask import Flask, jsonify, request, render_template
from apis.dbs_bootstrapper import initialize_dbs
from apis.validate_url_service import URLValidator

app = Flask(__name__, static_url_path='/', static_folder='static', template_folder='static')
dbFactory = initialize_dbs()
dbs = dbFactory.get_dbs()
urlValidator: URLValidator = URLValidator(dbs.values())

class URLStatusCode(IntEnum):
    SafeURL = 0
    Fishing = 1,
    UnsafeSite = 2

class WarningType(IntEnum):
    MaybeUnsafe = 2,
    UnsafeURL = 1

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

@app.get('/warn-user')
def warn_user():
    request_arguments = dict(request.args)
    if 'redirect_to' not in request_arguments.keys() or 'warning_type' not in request_arguments.keys():
        return render_template('error.html'), 400
    redirect_to = request_arguments['redirect_to']
    if not redirect_to.startswith('http'):
        redirect_to = 'http://' + redirect_to
    
    warning_type = request_arguments['warning_type']
    if WarningType.MaybeUnsafe == int(warning_type):
        return render_template('yellow_warning.html', url=redirect_to)

    if WarningType.UnsafeURL == int(warning_type):
        return render_template('red_warning.html', url=redirect_to)
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
