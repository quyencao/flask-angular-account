from flask import jsonify

class Response:
    @staticmethod
    def make_response(data, status_code):
        resp = jsonify(data)
        resp.status_code = status_code
        return resp
