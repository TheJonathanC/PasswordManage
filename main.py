from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
import asyncio
from prisma import Prisma, register
db = Prisma()
db.connect()
register(db)

app = Flask(__name__)

class LoginSchema(Schema):
    site_name = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))


@app.route('/savecredentials', methods=['POST'])
def login():
  
    try:
        # Validate incoming JSON data against the LoginSchema
        login_data = LoginSchema().load(request.json)
        db.Password.create(
        {
            'sitename': login_data['site_name'],
            'password': login_data['password']
        }
    )
        print(login_data['site_name'], login_data['password'])
        # Here you can access login_data['site_name'] and login_data['password'] for further processing
        return jsonify({'success': True}), 200
    except ValidationError as e:
        # If validation fails, return error messages
        return jsonify({'success': False, 'errors': e.messages}), 400


if __name__ == '__main__':
    app.run(debug=True)
