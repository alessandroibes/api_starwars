from flask import Blueprint
from flask_restx import Api, Resource

VERSION = "1.0"
DOC = "API Star Wars Index"

bp_index = Blueprint("index", __name__, url_prefix="/")

api = Api(
    bp_index,
    version=VERSION,
    title=DOC,
    description=DOC,
    doc=False,
)

ns = api.namespace("", description=DOC)


@ns.route("/health-status", doc=False)
class Index(Resource):
    def get(self):
        return dict(service="API Star Wars HealthCheck", version=VERSION)
