from . import backend


def create_foss(foss_data):
    foss = backend.create_foss(foss_data)

    return foss.to_dict()


def get_foss_by_id(foss_id):
    foss = backend.get_foss_by_id(foss_id)

    return foss.to_dict()


def get_all_fosses():
    fosses = backend.get_all_fosses()
    return [
        foss.to_dict() for foss in fosses
    ]


def update_foss(foss_data, foss_id):
    foss = backend.update_foss(foss_data, foss_id)

    return foss.to_dict()


def delete_foss(foss_id):
    backend.delete_foss(foss_id)
