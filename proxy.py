from flask import Flask, request, make_response
import requests
from filter import filter
from tinydb import TinyDB, Query

app = Flask(__name__)

@app.route('/<path:url>')
def index(url):
    # takes request args and data and forwards it
    method = request.method
    headers = request.headers
    data = request.get_data()
    cookies = request.cookies
    url = request.full_path[1:]
    try:
        r = requests.request(method, url, cookies=cookies, headers=headers, data=data)
    except:
        print('fail ')
    if filter(r):
        # build results dictionary
        res = {}
        for key in app.config['options']:
            if key == 'json':
                try:
                    res[key] = r.json()
                except:
                    res[key] = ''
            elif key == 'cookies':
                res[key] = r.cookies.get_dict()
            elif key =='headers':
                res[key] = dict(r.headers)
            else:
                res[key] = getattr(r, key)
        
        # insert results into database
        db = app.config['db']
        db.insert(res)

        # forward response status code
        response = make_response('', r.status_code)
        return response
    else:
        response = make_response('', 204)
        return response

