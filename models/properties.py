import colander
from flask import current_app
from models.strict_schema import StrictMappingSchema


class Properties(StrictMappingSchema):
    all = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    name = colander.SchemaNode(colander.String(), missing=colander.drop)
    type = colander.SchemaNode(colander.String(), missing=colander.drop)
    shared = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    nthread = colander.SchemaNode(colander.String(), missing=colander.drop)
    optpipe = colander.SchemaNode(colander.String(), missing=colander.drop)
    readonly = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    embedr = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    embedpy = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    embedpy3 = colander.SchemaNode(colander.String(), missing=colander.drop)
    embedc = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    ipv6 = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    listenaddr = colander.SchemaNode(colander.String(), missing=colander.drop)
    nclients = colander.SchemaNode(colander.String(), missing=colander.drop)
    dbextra = colander.SchemaNode(colander.String(), missing=colander.drop)
    memmaxsize = colander.SchemaNode(colander.String(), missing=colander.drop)
    vmmaxsize = colander.SchemaNode(colander.String(), missing=colander.drop)


def serialize_monetdb_get(appstruct):
    properties = appstruct.split("\n")
    list_of_dict = []
    dict = {}
    name = None
    for i in range(1, len(properties) - 1):
        line_properties = properties[i].split()

        if name and name != line_properties[0]:
            list_of_dict.append(dict)
            dict = {}

        name = line_properties[0]
        dict[line_properties[1]] = line_properties[-1]

    list_of_dict.append(dict)

    return list_of_dict
