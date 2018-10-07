import uuid


def make_upload_image(filename, path):
    """
    Function which creates path for user's file in media folder using uuid.

    :param filename: name of the user's file, ex. 'image.png'
    :param path: where to save file in media folder, ex. 'model/attr'
    :return: path to file or None if filename is empty
    """
    if filename:
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return f'{path}/{filename[0]}/{filename[2]}/{filename}'
    return None
