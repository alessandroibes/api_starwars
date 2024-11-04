import logging

from flask import Blueprint, request
from flask_restx import Api, Resource

from starwars.application_layer.use_cases.planets import PlanetAlreadyRegistered, PlanetsUseCase
from starwars.presentation_layer.mappings import PlanetMapping
from starwars.presentation_layer.views.schemas import (
    generic_error_message_model,
    planets_request_model,
    planets_response_model
)

logger = logging.getLogger("api-starwars." + __name__)

VERSION = "1.0"
DOC = "API Star Wars Planets"

bp_planets = Blueprint("planets", __name__, url_prefix="/api/planets")

api = Api(
    bp_planets,
    version=VERSION,
    title=DOC,
    description=DOC,
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)

ns.add_model(generic_error_message_model.name, generic_error_message_model)
ns.add_model(planets_request_model.name, planets_request_model)
ns.add_model(planets_response_model.name, planets_response_model)


@ns.route("")
class PlanetResource(Resource):
    @ns.expect(planets_request_model)
    @ns.response(201, "CREATED", planets_response_model)
    @ns.response(400, "BAD REQUEST", generic_error_message_model)
    @ns.response(409, "CONFLICT", generic_error_message_model)
    def post(self):
        mapping = PlanetMapping(payload=request.json)

        try:
            result = PlanetsUseCase.create_planet(data=mapping)
        except PlanetAlreadyRegistered as e:
            logger.exception(
                "Failed to create planet - name already in use",
                extra={
                    "props": {
                        "request": f"/api/planets",
                        "method": "POST",
                        "name": mapping.name,
                        "error_message": str(e),
                    }
                }
            )

            return {"message": str(e)}, 409
        except Exception as e:
            logger.exception(
                "Failed to create planet",
                extra={
                    "props": {
                        "request": f"/api/planets",
                        "method": "POST",
                        "name": mapping.name,
                        "error_message": str(e),
                    }
                },
            )

            return {"message": str(e)}, 400

        return result, 201


@ns.route("/<string:id>")
class PlanetResourceItem(Resource):
    @ns.response(200, "OK", planets_response_model)
    @ns.response(400, "BAD REQUEST", generic_error_message_model)
    @ns.response(404, "NOT FOUND", generic_error_message_model)
    def get(self, id: str):
        try:
            planet = PlanetsUseCase().get_planet_by_id(id=id)

        except Exception as e:
            logger.exception(
                "Failed to get planet by id",
                extra={
                    "props": {
                        "request": f"/api/planets/{id}",
                        "method": "GET",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            return {"message": str(e)}, 400
        
        if not planet:
            logger.warning(
                f"Planet with id {id} was not found",
                extra={
                    "props": {
                        "request": f"/api/planets/{id}",
                        "method": "GET",
                        "id": id,
                    }
                },
            )

            return {"message": f"Planet with id {id} was not found"}, 404
        
        return planet, 200

    @ns.expect(planets_request_model)
    @ns.response(200, "OK", planets_response_model)
    @ns.response(400, "BAD REQUEST", generic_error_message_model)
    @ns.response(404, "NOT FOUND", generic_error_message_model)
    def put(self, id: str):
        mapping = PlanetMapping(payload=request.json)

        try:
            result = PlanetsUseCase.update_planet(
                id=id,
                data=mapping,
            )

        except PlanetAlreadyRegistered as e:
            logger.exception(
                "Failed to update planet - name already in use",
                extra={
                    "props": {
                        "request": f"/api/planets/{id}",
                        "method": "PUT",
                        "name": mapping.name,
                        "error_message": str(e),
                    }
                }
            )

            return {"message": str(e)}, 409

        except Exception as e:
            logger.exception(
                "Failed to update planet",
                extra={
                    "props": {
                        "request": f"/api/planets/{id}",
                        "method": "PUT",
                        "id": id,
                        "name": mapping.name,
                        "error_message": str(e),
                    }
                },
            )

            return {"message": str(e)}, 400

        return result, 200

    @ns.response(204, "NO CONTENT")
    @ns.response(400, "BAD REQUEST", generic_error_message_model)
    def delete(self, id: str):
        try:
            PlanetsUseCase.remove_planet(id=id)

        except Exception as e:
            logger.exception(
                "Failed to remove planet",
                extra={
                    "props": {
                        "request": f"/api/planets/{id}",
                        "method": "DELETE",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            return {"message": str(e)}, 400

        return None, 204
