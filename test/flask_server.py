'''
Created on 2019年8月30日

@author: syp560
'''
import logging
import json
import time
from flask import Flask, request, jsonify
from test.demo_decrorator import runTime

app = Flask(__name__)

logger = logging.getLogger('zxai_flask_server')
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.DEBUG)

@app.route('/test_name')
@runTime
def getName():
    word = request.args.get('name')
    if not word:
        word = 'Allen'
    logger.debug('Now is {}'.format(time.strftime("%H:%M:%S", time.localtime())))
    logger.debug(json.dumps('Hello {}, time is {}'.format(word, time.strftime("%H:%M:%S", time.localtime()))))

    arr = [1,2,3]
    return jsonify(arr)
    
@app.route('/test_name222')
@runTime
def getName222():
    word = request.args.get('name')
    if not word:
        word = 'Allen'
    logger.debug('Now is {}'.format(time.strftime("%H:%M:%S", time.localtime())))
    logger.debug(json.dumps('Hello {}, time is {}'.format(word, time.strftime("%H:%M:%S", time.localtime()))))

    arr = [1,2,3]
    return jsonify(arr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)