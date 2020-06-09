import colander
from models.strict_schema import StrictMappingSchema


class Options(StrictMappingSchema):
    host = colander.SchemaNode(colander.String(), missing=colander.drop)
    port = colander.SchemaNode(colander.Int(), missing=colander.drop)
    password = colander.SchemaNode(colander.String(), missing=colander.drop)
