from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Authentication import UserLogin, UserRegistration, SocialLogin

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/hello')

#Authentication
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserRegistration, '/auth/register')
api.add_resource(SocialLogin, '/auth/social-auth')
