import sys
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask_restful import Resource, reqparse
from src2.model import User, TraditionalAuth, SocialAuth
from src2.util.errorsAndMessages import error, succefullAuthMessage

#Initializers and Global Constant
class UserLogin(Resource):
    def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('email', help = 'This field cannot be blank', required = True)
            self.parser.add_argument('password', help = 'This field cannot be blank', required = True)
    def post(self):
        data = self.parser.parse_args()
        input_email = data['email']
        input_password = data['password']
        
        autheticated = TraditionalAuth.find_by_email(input_email)
        if (not autheticated) or (not autheticated.password_is_valid(input_password)):
            return error(500, "Credential Invalid")
        access_token = create_access_token(identity = autheticated.id)
        refresh_token = create_refresh_token(identity = autheticated.id)
        return(succefullAuthMessage('User Logged In Sucesfully', access_token, refresh_token))

        
class UserRegistration(Resource):
    def __init__(self):
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('email', help = 'This field cannot be blank', required = True)
            self.parser.add_argument('name', help = 'This field cannot be blank', required = True)
            self.parser.add_argument('password', help = 'This field cannot be blank', required = True)
    def post(self):
        data = self.parser.parse_args()
        input_email = data['email']
        input_pass = data['password']
        input_name = data['name']

        if TraditionalAuth.find_by_email(data['email']):
            return error(500, "User with such an email already exists")
        authenticationSession = TraditionalAuth(
            email = input_email,
            password = input_pass
        )
        try:
            authenticationSession.save()
            user = User(str(authenticationSession.getId()), input_name)
            user.save()
            access_token = create_access_token(identity = user.id)
            refresh_token = create_refresh_token(identity = user.id)
            return(succefullAuthMessage('User Created Sucesfully', access_token, refresh_token))
        except:
            print(error(500, sys.exc_info()[0]))
            raise
