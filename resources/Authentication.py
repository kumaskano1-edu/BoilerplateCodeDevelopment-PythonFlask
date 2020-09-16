import sys, requests
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

class SocialLogin(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('token', help = 'This field cannot be blank', required = True)

    def post(self):
        data = self.parser.parse_args()
        input_token = data['token']
        if not input_token:
            return error(500, 'Token is Empty')

        request_url = 'https://graph.facebook.com/me?access_token=' + input_token
        social_vendor_verify = requests.get(request_url).json()

        if SocialAuth.find_by_social_id(social_vendor_verify['id']):
            access_token = create_access_token(identity = social_vendor_verify['id'])
            refresh_token = create_refresh_token(identity = social_vendor_verify['id'])
            return succefullAuthMessage("User Logged In Sucesfully", access_token, refresh_token)
        
        authed_user = SocialAuth(social_vendor_verify['id'], 1, 'Facebook')

        #checking the length of the name, and assigning the result to the var input_name
        if len(social_vendor_verify["name"]) > 1: input_name = social_vendor_verify["name"].split()[0]
        else: input_name = social_vendor_verify["name"]

        try:
            authed_user.save()
            user = User(str(authed_user.getId()), input_name)
            user.save()
            access_token = create_access_token(identity = user.id)
            refresh_token = create_refresh_token(identity = user.id)
            return(succefullAuthMessage('User Created Sucesfully', access_token, refresh_token))
        except:
            print(error(500, sys.exc_info()[0]))
            raise

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
