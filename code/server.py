from multiprocessing import Pool
from flask import Flask, request, abort, jsonify
from prediction import *

app = Flask(__name__)
_pool = None

TEMP = 0.005
primetext = u'Du kommst des Weges '
#
def expensive_function(primetext):
        # import packages that is used in this function
        # do your expensive time consuming process
        return predict(primetext, TEMP)

@app.route('/', methods=['POST'])
def create_task():
    print "getting poem.."
    if not request.json:
        abort(400)
    f = _pool.apply_async(expensive_function,[request.json['primetext']])
    poem = f.get(timeout=20)
    return jsonify({'poem': poem}), 201

if __name__=='__main__':
        _pool = Pool(processes=30)
        try:
                # insert production server deployment code
                # app.run()
                app.run(debug=True)
        except KeyboardInterrupt:
                _pool.close()
                _pool.join()
