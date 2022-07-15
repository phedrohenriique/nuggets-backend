from sanic import json

## response error messages

invalid_fields = {
    "error": {
        "message": "Invalid/Missing Fields on Request",
        "type": "BadRequestException",
        "code": 400
    }
}

not_authorized = {
    "error": {
        "message": "Not Authorized",
        "type": "NotAuthorizedException",
        "code": 401
    }
}

database_error = {
    "error": {
        "message": "Could Not Execute Request",
        "type": "DatabaseError",
        "code": 500
    }
}

def error_response(data):
    return json(data, data["error"]["code"])

## response success messages

def success_response(data):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
    }

    return json(data, 200, headers=headers)
