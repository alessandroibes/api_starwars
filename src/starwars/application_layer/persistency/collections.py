from typing import NamedTuple, Sequence, Union


class Collection(NamedTuple):
    name: str
    validator: dict
    index: Union[
        str, Sequence[tuple]
    ]  # A sequence will be interpreted as one compound index
    unique_index: bool


collections_definitions = [
    Collection(
        "planets",
        validator= {
            "bsonType": "object",
            "required": ["name"],
            "properties": {
                "name": { "bsonType": "string" },
                "climate": { "bsonType": "string" },
                "diameter": { "bsonType": "string" },
                "population": { "bsonType": "string" },
                "films": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId"  # Garante que cada filme é um ObjectId válido
                    },
                    "description": "List of related film IDs, optional"
                }
            }
        },
        index="name",
        unique_index=True,
    ),
    Collection(
        "films",
        validator= {
            "bsonType": "object",
            "required": ["title"],
            "properties": {
                "title": { "bsonType": "string" },
                "release_date": { "bsonType": "string" },
                "director": { "bsonType": "string" },
                "planets": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId"  # Garante que cada planeta é um ObjectId válido
                    },
                    "description": "List of related planet IDs, optional"
                }
            }
        },
        index="title",
        unique_index=True,
    )
]