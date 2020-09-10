from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index_page():
    return 'Hello to who visited this page'


def check_posted_data(posted_data, function_name):
    if function_name == 'add':
        if "a" not in posted_data or "b" not in posted_data:
            return 301
        else:
            return 200
    if function_name == 'subtract':
        if 'a' not in posted_data or b not in posted_data:
            return 303
        else:
            return 200


class Add(Resource):
    # Get POSTED data
    def post(self):
        data_dict = request.get_json()

        # check posted data
        status_code = check_posted_data(data_dict, 'add')
        if status_code != 200:
            status = {
                'Message': 'An Error happened',
                'Status Code': status_code
            }
            return jsonify(status)

        # Add POSTED DATA
        a = data_dict["a"]
        b = data_dict["b"]
        add = a + b
        ret_json = {
            'Message': add,
            'Status code': 200
        }
        return jsonify(ret_json)


class Subtract(Resource):
    def post(self):
        data_dict = request.get_json()
        status_code = check_posted_data(data_dict, 'subtract')

class Divide(Resource):
    pass


class Multiply(Resource):
    pass


api.add_resource(Add, '/add')

if __name__ == '__main__':
    app.run(debug=True)
