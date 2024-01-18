# Yet Another Proxy Server (yaps)

Throughout all my web ctfing, I've often used a proxy server to store and analyse requests, especially with tools such as [SQLMap](https://github.com/sqlmapproject/sqlmap) etc.
Thought it would be nice to write something and others can start up on the go if needed, rather than writing something completely

## What this does
Well, anything really, but I usually use this for parsing thru/looking at results from automated scanners/tools when they can't do the job alone. 
For instance, the [RawWater](https://quals.2023.nautilus.institute/challenges/1.html) defcon 2023 quals chall was solved in under 15min at 5am by simply chucking sqlmap at it, running a proxy server similar to this to print out the queries+result, and looking for an injectable parameter/keyword, which we quickly found. (skilless) Magic!

## This project is NOT meant to be scaled
A very crude implementation was taken here, with using a [Flask](https://github.com/pallets/flask/) server as the proxy server and the [requests](https://pypi.org/project/requests/) module to do most of the heavy lifting. 
I used [tinyDB](https://github.com/msiemens/tinydb) here as I have never done so before, and JSON is...good?
Therefore, this is definitely not meant to be scaled in any sense and is purely for one off ctf challenge type usecases.

## Usage
1. Clone the repo ```git clone https://github.com/fishjojo1/yaps```
2. Edit the config.json config file, and filter.py, and whatever else you may please
3. Start with ```py main.py --config <path to config file>```
4. Send any request to the proxy server with the url ```<proxy server url>/<actual request url>```
5. Profit

### Config.json
```
{   
    "proxy-port": 5000, //port that the server will run on
    "db-path": "collected/data.json", //relative(forgive me) path of the config file
    "log-info": { //config for what details to log, you could also add anything that a request object will store and return with getattr(request, 'attr')
        "url": true, //set to true to store, set to false to...not store?
        "text": true, 
        "json": true,
        "cookies": true,
        "headers": true,
        "status_code": true
    }
}
```

### Filter.py
EVERY request sent to the proxy server will be sent to the filter() function here in order to determine if the request should be saved
The function should take in a request parameter(feel free to change this lol), and return a boolean value, ```True``` if the result should be saved and ```False``` otherwise
<br>
Eg. to save requests with status code 200
```
def filter(r):
    if r.status_code == 200:
        return True
    return False
```

Eg. to reject requests with the keyword 'fail'
```
def filter(r):
    if 'fail' in r.text:
        return False
    return True
```

:D
