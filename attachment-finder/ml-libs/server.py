from __future__ import print_function

from flask import Flask
from flask import request

import logic
import utils.nl_api as nl

app = Flask(__name__)


@app.route("/")
def hello():
    ret = 'Hit the endpoint like this http://127.0.0.1:5000?q=TEXT'
    try:
        sentence = str(request.args['a'])
        print('Received text = {}'.format(sentence))
        nl_api_element = nl.call_nl_api(sentence)
        print('[NL API] element = {}'.format(nl_api_element))
        predicted_query = logic.build_query(nl_api_element)
        print('[Logic] predicted query = {}'.format(predicted_query))
        return predicted_query
    except Exception, e:
        print(str(e)), e
    return ret


if __name__ == "__main__":
    app.run()
