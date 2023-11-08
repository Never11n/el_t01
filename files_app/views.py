import datetime
import os
from random import randint
from rexec import FileWrapper
from django.http import HttpResponse, Http404
from files_app.models import AttachmentFile
from stroybook.env import FILE_HOSTING_STORE_PATH
from django.core.files import File
from stroybook.settings import FILE_HOSTING_STORE_PATH_N, FILE_HOSTING_STORE_PATH_N_TENDER

def store_one_attachment_file(file_to_upload, type_templ='ads'):
    try:
        new_file_system_name = str(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())) + "_" \
                               + str(randint(1, 10000))
        f = File(file_to_upload)
        print ("f = ", f)
        user_file = AttachmentFile()
        user_file.content_type = file_to_upload.content_type
        user_file.size = file_to_upload.size
        user_file.name = file_to_upload.name
        try:
            user_file.extension = file_to_upload.name.split('.')[-1]
        except Exception as ex:
            user_file.extension = ''
        if user_file.extension != '':
            new_file_system_name += '.' + user_file.extension
        print ("new_file_system_name =", new_file_system_name )
        user_file.system_name = new_file_system_name

        user_file.save()
        print ("user_file = ", user_file)
        #new_file = FILE_HOSTING_STORE_PATH + new_file_system_name
        if type_templ == "tender":
            new_file = FILE_HOSTING_STORE_PATH_N_TENDER + '/' + new_file_system_name
        else:
            new_file = FILE_HOSTING_STORE_PATH_N + '/' + new_file_system_name

        print ("new_file = ", new_file)
        with open(new_file, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        print ("user_file.id =", user_file.id)
        return user_file.id
    except Exception as ex:
        return 0


def download_attachment(request, file_id):
    # this code just for local usage, consider use nginx in production
    try:
        user_file = AttachmentFile.objects.get(id=int(file_id))
        #file_path = FILE_HOSTING_STORE_PATH + user_file.system_name
        file_path = FILE_HOSTING_STORE_PATH_N + user_file.system_name
        print ("file_path = ", file_path)
        response = HttpResponse(FileWrapper(file(file_path)))
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Type'] = user_file.content_type
        response['Content-Disposition'] = 'attachment; filename=' + '"' + user_file.name + '"'
        response['Expires'] = datetime.datetime.now() + datetime.timedelta(days=360)
        response['Last-Modified'] = user_file.created
        return response
    except Exception as ex:
        raise Http404

