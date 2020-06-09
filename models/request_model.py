import colander
from api.errors import InvalidUsage
from models.options import Options
from models.arguments import Arguments
from models.properties import Properties


class Rmodel(colander.MappingSchema):
    arguments = Arguments(missing=colander.drop)
    options = Options()
    properties = Properties(missing=colander.drop)
    databases = colander.SchemaNode(colander.List(), missing=colander.drop)
    dbfarm = colander.SchemaNode(colander.String(), missing=colander.drop)


class Gmodel(colander.MappingSchema):
    arguments = Arguments(missing=colander.drop)
    options = Options()
    properties = colander.SchemaNode(colander.List(), missing=colander.drop)
    databases = colander.SchemaNode(colander.List(), missing=colander.drop)
    dbfarm = colander.SchemaNode(colander.String(), missing=colander.drop)


def validate_model(dict_object):
    try:
        model = Rmodel().deserialize(dict_object)
    except colander.Invalid as e:
        errors = e.asdict()
        raise InvalidUsage(errors, status_code=400)

    return model


def validate_get_model(dict_object):
    try:
        model = Gmodel().deserialize(dict_object)
    except colander.Invalid as e:
        errors = e.asdict()
        raise InvalidUsage(errors, status_code=400)

    return model
