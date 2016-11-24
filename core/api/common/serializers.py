import datetime
import uuid
from functools import singledispatch


@singledispatch
def serialize(rv):
    return rv


@serialize.register(datetime.datetime)
def serialize_dt(rv):
    return datetime.datetime.strftime(rv, '%Y-%m-%dT%H:%M:%S.%fZ')


@serialize.register(uuid.UUID)
def serialize_uuid(rv):
    return str(rv)


class ModelSerializerMixin(object):
    def to_dict(self, exclude=None, only=None):
        if exclude and only:
            msg = 'ModelSerializer can receive either `exclude` or `only`, not both.'
            raise ValueError(msg)

        if exclude is None:
            exclude = []
        if only is None:
            only = []

        return self._to_dict(exclude, only)

    def _to_dict(self, exclude, only):
        serialized_model = {}
        _mapper = self.__mapper__.c.keys()

        if exclude:
            for attr in _mapper:
                if attr not in exclude:
                    serialized_model[attr] = self._serialize_attr(attr)
        elif only:
            for attr in only:
                if attr in _mapper:
                    serialized_model[attr] = self._serialize_attr(attr)
                else:
                    raise ValueError(
                        'The `only` attribute contains an invalid key: `%s`' % attr)
        else:
            for attr in _mapper:
                serialized_model[attr] = self._serialize_attr(attr)

        return serialized_model

    def _serialize_attr(self, attr):
        _val = getattr(self, attr)
        return serialize(_val)
