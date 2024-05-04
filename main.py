from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError, validate
import asyncio
from prisma import Prisma, register




app = Flask(__name__)
app.register_blueprint()
class LoginSchema(Schema):
    site = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=1))
    _id = fields.String(required=True, validate=validate.Length(min=1))    
class RegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=5))
    email = fields.String(required=True, validate=validate.Email())
    password = fields.String(required=True, validate=validate.Regexp(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', error='Password must contain at least one letter, one number, and be at least 8 characters long'))


@app.route('/savecredentials', methods=['POST'])
async def login():
    db = Prisma()
    await db.connect()
    try:
        # Validate incoming JSON data against the LoginSchema
        login_data = LoginSchema().load(request.json)
        await db.password.create(
        {
            'userId': login_data['_id'], # This should be the user ID of the user who is saving the password, for example 'user': user.id
            'site': login_data['site'], 
            'passwordHash': login_data['password'] # This detail should be encrypted, and not stored in plain text
        }
    )
        # Here you can access login_data['site_name'] and login_data['password'] for further processing
        return jsonify({'success': True}), 200
    except ValidationError as e:
        # If validation fails, return error messages
        return jsonify({'success': False, 'errors': e.messages}), 400

@app.route('/register', methods=['POST'])
async def register():
    db = Prisma()
    await db.connect()
    try:
        # Validate incoming JSON data against the LoginSchema
        register_data = RegisterSchema().load(request.json)
        await db.user.create(
        {
            'username': register_data['username'], 
            'email': register_data['email'],
            'password': register_data['password'] # This detail should be encrypted, and not stored in plain text
        }
    )
        user = await db.user.find_unique(where={"email": register_data["email"]})
        print(user.id)
        return jsonify({'success': True, 'userID' : user.id}), 200
    except ValidationError as e:
        # If validation fails, return error messages
        return jsonify({'success': False, 'errors': e.messages}), 400


if __name__ == '__main__':
    app.run(debug=True)
