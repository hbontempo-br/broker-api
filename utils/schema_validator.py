import logging

import jsonschema
from api.resources.base_resource import BaseResource
from cachetools.func import ttl_cache
from constants import SCHEMA_FILE
from falcon import Request, Response
from openapi_schema_to_json_schema import to_json_schema
from prance import ResolvingParser
from utils.errors import BadRequest

logging.getLogger("openapi_spec_validator").setLevel(level=logging.INFO)


def validate_schema(
    req: Request, resp: Response, resource: BaseResource, params: dict, schema_dict
):
    try:
        jsonschema.validate(
            req.media,
            schema_dict,
            format_checker=jsonschema.FormatChecker(),
        )
    except jsonschema.ValidationError as e:
        raise BadRequest(description=e.message).http()


@ttl_cache()
def get_specification(schema_name: str, filepath: str = SCHEMA_FILE) -> dict:
    specification = load_full_specification(filepath=filepath)
    open_api_dict = specification.get("components").get("schemas")[schema_name]
    options = {"supportPatternProperties": True}
    logging.debug(f"Converting OpenApi to jsonschema (schema: {schema_name})")
    converted_schema_dict = to_json_schema(schema=open_api_dict, options=options)
    return converted_schema_dict


@ttl_cache()
def load_full_specification(filepath: str):
    logging.debug(f"Loading OpenApi specification from {filepath}")
    parser = ResolvingParser(url=filepath, backend="openapi-spec-validator")
    logging.debug("OpenApi specification loaded")
    return parser.specification
