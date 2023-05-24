from utils.query import query


def get_role(username):
    find_user = f''' SELECT * FROM MANAJER WHERE username = '{username}' '''
    response = query(find_user)
    if (len(response) != 0):
        return 'Manajer'

    find_user = f''' SELECT * FROM PENONTON WHERE username = '{username}' '''
    response = query(find_user)
    if (len(response) != 0):
        return 'Penonton'

    return 'Panitia'
