import colander


class Arguments(colander.MappingSchema):
    all = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    long = colander.SchemaNode(colander.Boolean(), missing=colander.drop)
    password = colander.SchemaNode(colander.String(), name="pass", missing=colander.drop)
