from . import backend


def create_foss(foss_data):
    """Create Foss.
    :param foss_data: Foss information
    :type foss_data: dict
    :returns: serialized Foss object
    :rtype: dict
    """
    foss = backend.create_foss(foss_data)

    return foss.to_dict()


def get_foss_by_id(foss_id):
    """Get Foss by id.
    :param foss_id: id of the foss to be retrived
    :type foss_id: integer
    :returns: serialized Foss object
    :rtype: dict
    """
    foss = backend.get_foss_by_id(foss_id)

    return foss.to_dict()


def get_all_fosses():
    """Get all Fosses.
    :returns: serialized Foss objects
    :rtype: list
    """
    fosses = backend.get_all_fosses()
    return [
        foss.to_dict() for foss in fosses
    ]


def update_foss(foss_data, foss_id):
    """Update Foss.
    :param foss_data: Foss information
    :type foss_data: dict
    :param foss_id: id of the Foss to be updated
    :type foss_id: integer
    :returns: serialized Foss object
    :rtype: dict
    """
    foss = backend.update_foss(foss_data, foss_id)

    return foss.to_dict()


def delete_foss(foss_id):
    """Delete Foss.
    :param foss_id: id of the Foss to be deleted
    :type foss_id: integer
    """
    backend.delete_foss(foss_id)
