def error(errorNum, message):
    return {
        'msg': message,
        'err': errorNum
    }, errorNum

def succesfulMessage(message):
    return {
        'msg': message
    }
def succefullAuthMessage(message, token1, token2):
    return {
        'msg': message,
        'access_token': token1,
        'refreshtoken': token2
    }