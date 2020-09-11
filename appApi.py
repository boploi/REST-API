from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


@app.route('/')
def index_page():
    return 'Hello to who visited this page'


def check_posted_data(posted_data, function_name):
    if function_name == 'add' or function_name == 'subtract' or function_name == 'multiply':
        if "a" not in posted_data or "b" not in posted_data:
            return 301
        else:
            return 200
    elif function_name == 'divide':
        if 'a' not in posted_data or 'b' not in posted_data:
            return 301
        elif posted_data["b"] == 0:
            return 302
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
            'Status code': status_code
        }
        return jsonify(ret_json)


class Subtract(Resource):
    def post(self):
        data_dict = request.get_json()
        status_code = check_posted_data(data_dict, 'subtract')
        if status_code != 200:
            ret_json = {
                'Message': 'An Error happened',
                'Status code': status_code
            }
            return jsonify(ret_json)
        a = data_dict["a"]
        b = data_dict["b"]
        sub = a - b
        ret_sub = {
            'Message': sub,
            'Status code': status_code
        }
        return jsonify(ret_sub)


class Divide(Resource):
    def post(self):
        data_dict = request.get_json()
        status_code = check_posted_data(data_dict, 'divide')
        if status_code != 200:
            ret_json = {
                'Message': 'An Error happened',
                'Status code': status_code
            }
            return jsonify(ret_json)
        a = data_dict["a"]
        b = data_dict["b"]
        div = (a*1.0)/b
        ret_sub = {
            'Message': div,
            'Status code': status_code
        }
        return jsonify(ret_sub)


class Multiply(Resource):
    def post(self):
        data_dict = request.get_json()
        status_code = check_posted_data(data_dict, 'multiply')
        if status_code != 200:
            ret_json = {
                'Message': 'An Error happened',
                'Status code': status_code
            }
            return jsonify(ret_json)
        a = data_dict["a"]
        b = data_dict["b"]
        multi = a * b
        ret_mul = {
            'Result': multi,
            'Status code': 200
        }
        return jsonify(ret_mul)


api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')

if __name__ == '__main__':
    app.run(debug=True)
