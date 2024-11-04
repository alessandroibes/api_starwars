from flask_restx import Model, fields


class NullableString(fields.String):
    __schema_type__ = ["string", "null"]
    __schema_example__ = "nullable string"


generic_error_message_model = Model(
    "generic_error_message",
    {
        "message": fields.String(
            description="Error message"
        )
    }
)


films_request_model = Model(
    "films_request",
    {
        "title": fields.String(
            description="The title of this film",
            required=True,
            example="A New Hope",
        ),
        "director": NullableString(
            description="The name of the director of this film",
            example="George Lucas",
        ),
        "release_date": NullableString(
            description="The ISO 8601 date format of film release at original creator country",
            example="1977-05-25",
        ),
        "planets": fields.List(fields.String(
            description="An array of planet resource id",
            example="672762a0875fea2f97a2a9ce",
        ))
    }
)


films_response_model = Model(
    "films_response",
    {
        "id": fields.String(
            description="The identifier of this film",
            example="67281161d0af9e1cf7e4cd8f",
        ),
        "title": fields.String(
            description="The title of this film",
            example="A New Hope",
        ),
        "director": fields.String(
            description="The name of the director of this film",
            example="George Lucas",
        ),
        "release_date": fields.String(
            description="The ISO 8601 date format of film release at original creator country",
            example="1977-05-25",
        ),
        "planets": fields.List(fields.String(
            description="An array of planet resource id",
            example="672762a0875fea2f97a2a9ce",
        )),
        "created": fields.String(
            description="the ISO 8601 date format of the time that this resource was created",
            example="2014-12-10T14:23:31.880000Z",
        ),
        "edited": fields.String(
            description="the ISO 8601 date format of the time that this resource was edited",
            example="2014-12-12T11:24:39.858000Z",
        )
    }
)


planets_request_model = Model(
    "planets_request",
    {
        "name": fields.String(
            description="The name of this planet",
            required=True,
            example="Tatooine",
        ),
        "diameter": NullableString(
            description="The diameter of this planet in kilometers",
            example="10465",
        ),
        "climate": NullableString(
            description="The climate of this planet. Comma separated if diverse",
            example="arid",
        ),
        "population": NullableString(
            description="The average population of sentient beings inhabiting this planet",
            example="200000",
        ),
        "films": fields.List(fields.String(
            description="An array of Film Resources id that this planet has appeared in",
            example="67281579f96026b041ddecfb",
        ))
    }
)


planets_response_model = Model(
    "planets_response",
    {
        "id": fields.String(
            description="The identifier of this planet",
            example="6728162d5b59f05a5a28562b",
        ),
        "name": fields.String(
            description="The name of this planet",
            required=True,
            example="Tatooine",
        ),
        "diameter": NullableString(
            description="The diameter of this planet in kilometers",
            example="10465",
        ),
        "climate": NullableString(
            description="The climate of this planet. Comma separated if diverse",
            example="arid",
        ),
        "population": NullableString(
            description="The average population of sentient beings inhabiting this planet",
            example="200000",
        ),
        "films": fields.List(fields.String(
            description="An array of Film Resources id that this planet has appeared in",
            example="67281579f96026b041ddecfb",
        )),
        "created": fields.String(
            description="the ISO 8601 date format of the time that this resource was created",
            example="2014-12-10T14:23:31.880000Z",
        ),
        "edited": fields.String(
            description="the ISO 8601 date format of the time that this resource was edited",
            example="2014-12-12T11:24:39.858000Z",
        )
    }
)