from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/data/waste_types', methods=['GET'])
def get_waste_types():
    waste_types = {
        'bulky_goods': {
            'de': 'Sperrgut',
            'en': 'Bulky goods',
        },
        'cardboard': {
            'de': 'Karton',
            'en': 'Cardboard',
        },
        'cargotram': {
            'de': 'Cargotram',
            'en': 'Cargotram',
        },
        'chipping_service': {
            'de': 'Häkseldienst',
            'en': 'Chipping service',
        },
        'etram': {
            'de': 'eTram',
            'en': 'eTram',
        },
        'incombustibles': {
            'de': 'Unbrennbares',
            'en': 'Incombustibles',
        },
        'metal': {
            'de': 'Metall',
            'en': 'Metal',
        },
        'organic': {
            'de': 'Grüngut',
            'en': 'Organic waste',
        },
        'paper': {
            'de': 'Altpapier',
            'en': 'Paper',
        },
        'special': {
            'de': 'Sondermüll',
            'en': 'Special waste',
        },
        'textile': {
            'de': 'Textilien',
            'en': 'Textiles',
        },
        'waste': {
            'de': 'Abfall',
            'en': 'Waste',
        },
    }
    return jsonify(waste_types)


@app.route('/submit_calendar', methods=['POST'])
def submit_calendar():
    response = {"status": "success"}
    post_data = request.get_json()
    print(post_data)
    return jsonify(response)


if __name__ == '__main__':
    app.run()

