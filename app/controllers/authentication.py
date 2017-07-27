"""Authentication."""
from flask_restful import request, Resource


class Authentication(Resource):
    """Authentication class."""

    def get(self):
        """get endtpoint."""
        return {"Authenticate": "Please try again"}
