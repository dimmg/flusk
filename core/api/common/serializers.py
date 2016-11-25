import datetime
import uuid
from functools import singledispatch


@singledispatch
def serialize(rv):
    """
    Define a generic serializable function.
    """
    return rv


@serialize.register(datetime.datetime)
def serialize_dt(rv):
    """Register the `datetime.datetime` type
    for the generic serializable function.

    Serialize a `datetime` object to `string`
    according to strict-rfc3339.
    :param rv: object to be serialized
    :type rv: datetetime.datetime
    :returns: string
    """
    return datetime.datetime.strftime(rv, '%Y-%m-%dT%H:%M:%S.%fZ')


@serialize.register(uuid.UUID)
def serialize_uuid(rv):
    """Register the `uuid.UUID` type
    for the generic serializable function.
    :param rv: object to be serialized
    :type rv: uuid.UUID
    :returns: string
    """
    return str(rv)


class ModelSerializerMixin(object):
    """
    Serializable Mixin for the SQLAlchemy objects.
    """
    def to_dict(self, exclude=None, only=None):
        """Convert SQLAlchemy object to `dict`.

        :param exclude: attrs to be excluded, defaults to None
        :type exclude: list, optional
        :param only: attrs to be serialized, defaults to None
        :type only: list, optional
        :returns: serialized SQLAlchemy object
        :rtype: dict

        The method cannot receive both `exclude` and `only` arguments
        at the same time. If this use case is reproduced, appropriate
        ValueError is raised.

        e.g. of usage

        ...
        return sql_alchemy_obj.to_dict(exclude=['name', 'email'])
        ...

        """
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
