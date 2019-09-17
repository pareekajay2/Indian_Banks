from flask import Flask, request, jsonify
from database_utilities.utils import get_data_banks, get_branch_details
from resources import create_access_token
import jwt
import json
from functools import wraps

app = Flask(__name__)
app.debug = True


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'secret', algorithms=['HS256'])
            with open('tokens.json', 'r') as infile:
                file = json.load(infile)
            if data['exp'] == file['exp']:
                pass
            else:
                return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', "error": e.args}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/bank_details/<ifsc>', methods=['GET'])
@token_required
def bank_details(ifsc):
    try:
        data = get_data_banks(ifsc=ifsc)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Something went wrong", "error": e.args}), 400


@app.route('/branch_details/<city>/<bank_name>', methods=['GET'])
@token_required
def branch_details(city, bank_name):
    try:
        if 'offset' in request.args:
            offset = request.args['offset']
        else:
            offset = 0
        if 'limit' in request.args:
            limit = request.args['limit']
        else:
            limit = None
        data = get_branch_details(city, bank_name, offset, limit)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Something went wrong", "errors": e.args}), 400


@app.route('/create-api-token', methods=['POST'])
def create_api_token():
    try:
        body = request.get_json(force=True)
        old_token = body['old_token']
        token = create_access_token(old_token)
        return jsonify({'token': str(token)}), 200
    except Exception as e:
        return jsonify({"success": False, "message": "Something went wrong", "errors": e.args}), 400


if __name__ == "__main__":
    app.run(debug=True)




