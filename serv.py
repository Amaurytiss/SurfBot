# import flask dependencies
from flask import Flask, request, make_response, jsonify
from surfline_apiV2 import Forecast


# initialize the flask app
app = Flask(__name__)

# default route

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    param_ask = req.get('queryResult').get('parameters').get('conditions')

    spot = req.get('queryResult').get('outputContexts')[0].get('parameters').get('spot')
    


    prev = Forecast(spot)

    if param_ask == 'wind':
        sentence = prev.send_wind()

    if param_ask == 'wave':
        sentence = prev.send_wave()

    if param_ask == 'weather':
        sentence = prev.send_weather()

    if param_ask == 'score':
        sentence = prev.send_score()

    if param_ask == 'period':
        sentence = prev.send_period()

    if param_ask == 'tide':
        sentence = prev.send_tide()

    return {'fulfillmentText': sentence}

    

# create a route for webhook
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run(debug=True)