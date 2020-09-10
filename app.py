from flask import Flask, request

app = Flask(__name__)


@app.route('/jsonpage')
def hoa_info():
    hoa = {
        'name': 'HoaPM',
        'address': 'chuong lon',
        'phone': [
            {
                'phone name': 'home',
                'phone number': '0123546'
            },
            {
                'phone name': 'work',
                'phone number': '092132184'
            }
        ]
    }
    return hoa


@app.route('/dividenum', methods=['POST'])
def divide_three_num():
    # get a,b,c from posted data
    dataDict = request.get_json()
    a = dataDict["a"]
    b = dataDict["b"]
    c = dataDict["c"]
    # divide three num
    div = a / b / c
    # add to json
    retJson = {
        'divided': 'div'
    }
    # jsonify
    return retJson

if __name__ == '__main__':
    app.run(debug=True)
