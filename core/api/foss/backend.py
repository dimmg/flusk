from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ..common.exceptions import RecordAlreadyExists, RecordNotFound

from .models import Foss


def create_foss(foss_data):
    foss = Foss(**foss_data)
    try:
        foss.save()
    except IntegrityError:
        msg = 'Email `%s` already has been taken' % foss_data['email']
        raise RecordAlreadyExists(message=msg)

    return foss


def get_foss_by_id(foss_id):
    try:
        result = Foss.query.filter(Foss.id == foss_id).one()
    except NoResultFound:
        msg = 'There is no Foss with `id: %s`' % id
        raise RecordNotFound(message=msg)

    return result


def get_all_fosses():
    return Foss.query.all()


def update_foss(foss_data, foss_id):
    foss = get_foss_by_id(foss_id)
    foss.update(**foss_data)

    return foss


def delete_foss(foss_id):
    foss = get_foss_by_id(foss_id)
    foss.delete()
