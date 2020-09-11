from flask_restful import Resource, reqparse
import sys

from src2.model import User
class Login(Resource):
    def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('email', help = 'This field cannot be blank', required = True)
            self.parser.add_argument('password', help = 'This field cannot be blank', required = True)
    def post(self):
        data = self.parser.parse_args()
        return {"message": "auth"}
    
class UserRegistration(Resource):
    def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('email', help = 'This field cannot be blank', required = True)
            self.parser.add_argument('name', help = 'This field cannot be blank', required = True)
            self.parser.add_argument('password', help = 'This field cannot be blank', required = True)
    def post(self):
        data = self.parser.parse_args()
        user = User(
            email = data['email'],
            name = data['name'],
            password = data['password']
        )

        try:
            user.save()
            return {
                'message': 'User created' .format(data['email'])
            }
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
