from colander import MappingSchema, Mapping


# This will result in raising error for unknown extra keys
class StrictMappingSchema(MappingSchema):
    def schema_type(self, **kw):
        return Mapping(unknown='raise')
