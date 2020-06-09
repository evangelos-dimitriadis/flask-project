import colander
from api.errors import InvalidUsage
from flask import current_app


class ExtendedStatusInfo(colander.MappingSchema):
    connection_uri = colander.SchemaNode(colander.String())
    database_name = colander.SchemaNode(colander.String())
    locked = colander.SchemaNode(colander.String())
    scenarios = colander.SchemaNode(colander.String())
    start_count = colander.SchemaNode(colander.Int())
    stop_count = colander.SchemaNode(colander.Int())
    crash_count = colander.SchemaNode(colander.Int())
    average_uptime = colander.SchemaNode(colander.String())
    maximum_uptime = colander.SchemaNode(colander.String())
    minimum_uptime = colander.SchemaNode(colander.String())
    last_start_with_crash = colander.SchemaNode(colander.String())
    last_start = colander.SchemaNode(colander.String())
    last_stop = colander.SchemaNode(colander.String())
    average_of_crashes_in_the_last_start_attempt = colander.SchemaNode(colander.Float())
    average_of_crashes_in_the_last_10_start_attempts = colander.SchemaNode(colander.Float())
    average_of_crashes_in_the_last_30_start_attempts = colander.SchemaNode(colander.Float())


class ExtentedStatusList(colander.SequenceSchema):
    stat = ExtendedStatusInfo()


class ExtendedStatus(colander.MappingSchema):
    status = ExtentedStatusList()


class StatusInfo(colander.MappingSchema):
    database_name = colander.SchemaNode(colander.String())
    state = colander.SchemaNode(colander.String(), validator=colander.Length(min=1, max=4))
    state_time = colander.SchemaNode(colander.String())
    health = colander.SchemaNode(colander.String())
    health_time = colander.SchemaNode(colander.String())
    remarks = colander.SchemaNode(colander.String())


class StatusList(colander.SequenceSchema):
    stat = StatusInfo()


class Status(colander.MappingSchema):
    status = StatusList()


def serialize_status_long(appstruct):
    key_value = appstruct.split("\n")
    dict = {}
    list_of_dict = []
    for v in key_value:
        entry = v.split(": ")
        if len(entry) > 1:
            key = entry[0].replace('  ', '').replace(' ', '_')
            dict[key] = entry[1]
        else:
            list_of_dict.append(dict)
            dict = {}

    # Remove empty
    while {} in list_of_dict:
        list_of_dict.remove({})

    s = {'status': list_of_dict}

    try:
        serialized = ExtendedStatus().serialize(s)
    except colander.Invalid as e:
        errors = e.asdict()
        raise InvalidUsage(errors, status_code=400)

    return serialized


def serialize_status(appstruct):
    status = appstruct.split("\n")
    list_of_dict = []
    for i in range(1, len(status) - 1):
        line_status = status[i].split()
        dict = {}
        # Normal case
        if len(line_status) >= 6:
            dict['database_name'] = line_status[0]
            dict['state'] = line_status[1]
            dict['state_time'] = line_status[2]
            dict['health'] = line_status[3]
            dict['health_time'] = line_status[4]
            dict['remarks'] = line_status[5]
        # No time case
        else:
            dict['database_name'] = line_status[0]
            dict['state'] = line_status[1]
            dict['state_time'] = ''
            dict['health'] = ''
            dict['health_time'] = ''
            dict['remarks'] = ''

        list_of_dict.append(dict)

    s = {'status': list_of_dict}
    try:
        serialized = Status().serialize(s)
    except colander.Invalid as e:
        errors = e.asdict()
        raise InvalidUsage(errors, status_code=400)

    return serialized
