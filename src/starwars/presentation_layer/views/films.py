import logging

from flask import Blueprint, request
from flask_restx import Api, Resource

from starwars.application_layer.use_cases.films import FilmAlreadyRegistered, FilmsUseCase
from starwars.presentation_layer.mappings import FilmMapping
from starwars.presentation_layer.views.schemas import (
    generic_error_message_model,
    films_request_model,
    films_response_model
)

logger = logging.getLogger("api-starwars." + __name__)

VERSION = "1.0"
DOC = "API Star Wars Films"

bp_films = Blueprint("films", __name__, url_prefix="/api/films")

api = Api(
    bp_films,
    version=VERSION,
    title=DOC,
    description=DOC,
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)

ns.add_model(generic_error_message_model.name, generic_error_message_model)
ns.add_model(films_request_model.name, films_request_model)
ns.add_model(films_response_model.name, films_response_model)


@ns.route("")
class FilmResource(Resource):
    @ns.expect(films_request_model)
    @ns.response(201, "CREATED", films_response_model)
    @ns.response(400, "BAD REQUEST", generic_error_message_model)
    @ns.response(409, "CONFLICT", generic_error_message_model)
    def post(self):
        mapping = FilmMapping(payload=request.json)

        try:
            result = FilmsUseCase.create_film(data=mapping)

        except FilmAlreadyRegistered as e:
            logger.exception(
                "Failed to create film - title already in use",
                extra={
                    "props": {
                        "request": "/api/films",
                        "method": "POST",
                        "name": mapping.title,
                        "error_message": str(e),
                    }
                }
            )

            return {"message": str(e)}, 409
        
        except Exception as e:
            logger.exception(
                "Failed to create film",
                extra={
                    "props": {
                        "request": "/api/films",
                        "method": "POST",
                        "name": mapping.title,
                        "error_message": str(e),
                    }
                },
            )

            return {"message": str(e)}, 400

        return result, 201


@ns.route("/<string:id>")
class FilmByIdResourceItem(Resource):
    @ns.response(200, "OK", films_response_model)
    @ns.response(400, "BAD REQUEST", generic_error_message_model)
    @ns.response(404, "NOT FOUND", generic_error_message_model)
    def get(self, id: str):
        try:
            planet = FilmsUseCase().get_film_by_id(id=id)

        except Exception as e:
            logger.exception(
                "Failed to get film by id",
                extra={
                    "props": {
                        "request": f"/api/films/{id}",
                        "method": "GET",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            return {"message": str(e)}, 400
        
        if not planet:
            logger.warning(
                f"Film with id {id} was not found",
                extra={
                    "props": {
                        "request": f"/api/films/{id}",
                        "method": "GET",
                        "id": id,
                    }
                },
            )

            return {"message": f"Film with id {id} was not found"}, 404
        
        return planet, 200

    @ns.expect(films_request_model)
    @ns.response(200, "OK", films_response_model)
    @ns.response(400, "BAD REQUEST", generic_error_message_model)
    @ns.response(404, "NOT FOUND", generic_error_message_model)
    def put(self, id: str):
        mapping = FilmMapping(payload=request.json)

        try:
            result = FilmsUseCase.update_film(
                id=id,
                data=mapping,
            )

        except FilmAlreadyRegistered as e:
            logger.exception(
                "Failed to update film - title already in use",
                extra={
                    "props": {
                        "request": f"/api/films/{id}",
                        "method": "PUT",
                        "title": mapping.title,
                        "error_message": str(e),
                    }
                }
            )

            return {"message": str(e)}, 409

        except Exception as e:
            logger.exception(
                "Failed to update film",
                extra={
                    "props": {
                        "request": f"/api/films/{id}",
                        "method": "PUT",
                        "id": id,
                        "title": mapping.title,
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
            FilmsUseCase.remove_film(id=id)

        except Exception as e:
            logger.exception(
                "Failed to remove film",
                extra={
                    "props": {
                        "request": f"/api/films/{id}",
                        "method": "DELETE",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            return {"message": str(e)}, 400

        return None, 204
