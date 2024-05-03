from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login/<site_name>/<password>', methods=['POST'])
def login(site_name, password):

    return jsonify({'site_name': site_name, 'password': password})

if __name__ == '__main__':
    app.run(debug=True)