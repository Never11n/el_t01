import datetime
from random import randint
from django.http import Http404, HttpResponse
from images_app.models import Image
from images_app.thumb import generate_thumb
from stroybook.env import DOMAIN, IMAGE_HOSTING_STORE_PATH, TYPE_STORE_DIR
from django.core.files import File
from stroybook_app.const import IMAGE_THUMB_SIZE
from stroybook.settings import IMAGE_HOSTING_STORE_PATH_N, IMAGE_HOSTING_STORE_PATH_N_SHORT


def store_one_file(file_to_upload, file_name):
    f = File(file_to_upload)
    user_file = Image()
    user_file.content_type = file_to_upload.content_type
    user_file.size = file_to_upload.size
    user_file.name = file_name
    user_file.save()

    #new_file = IMAGE_HOSTING_STORE_PATH + file_name
    new_file = IMAGE_HOSTING_STORE_PATH_N + '/' + file_name
    print ( "new_file = ", new_file )
    with open(new_file, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if TYPE_STORE_DIR == 'local':
        m_return = '/' + IMAGE_HOSTING_STORE_PATH_N_SHORT + '/' + user_file.name
    else:
        m_return = DOMAIN + '/media/' + user_file.name
    return m_return


def save_thumb(file_for_thumb, file_name, dim):
    ext = file_name.split('.')[-1]
    #thumb_name = IMAGE_HOSTING_STORE_PATH + str(dim) + '_' + file_name
    thumb_name = IMAGE_HOSTING_STORE_PATH_N + '/' + str(dim) + '_' + file_name
    with open(thumb_name, 'wb+') as destination:
        f = generate_thumb(file_for_thumb, (dim, dim), ext)
        for chunk in f.chunks():
            destination.write(chunk)
    if TYPE_STORE_DIR == 'local':
        m_return = '/' + IMAGE_HOSTING_STORE_PATH_N_SHORT + '/' + str(dim) + '_' + file_name
    else:
        m_return = DOMAIN + '/media/' + str(dim) + '_' + file_name
    return m_return

def upload_image(_file):
    if 'image/' in str(_file.content_type):
        file_to_upload = _file
        file_name = str(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())) + "_" \
                    + str(randint(1, 10000)) + '.' + file_to_upload.name.split('.')[-1]
        user_image = Image()

        user_image.origin = store_one_file(file_to_upload, file_name)
        user_image.thumb = save_thumb(file_to_upload, file_name, IMAGE_THUMB_SIZE)
        user_image.save()
        return user_image.id
    else:
        return 0


def save_file_from_base64(request):
    return HttpResponse('ok')
