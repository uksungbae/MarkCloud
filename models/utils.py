from bson import ObjectId
from pydantic import BaseModel
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from pydantic import GetJsonSchemaHandler
from typing import Any


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: Any
    ) -> core_schema.CoreSchema:
        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError(f"Invalid ObjectId string: {value}")
            return ObjectId(value)

        python_schema = core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema(
                    [
                        core_schema.str_schema(),
                        core_schema.no_info_plain_validator_function(validate_from_str),
                    ]
                ),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

        json_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ],
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

        return core_schema.json_or_python_schema(
            python_schema=python_schema,
            json_schema=json_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(str)
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema_obj: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema.str_schema(pattern=r'^[0-9a-fA-F]{24}$'))
        return json_schema
