from flask import Flask

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


if __name__ == '__main__':
    app.run(debug=True)
