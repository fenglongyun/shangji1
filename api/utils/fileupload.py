from django.conf import settings
import random
import datetime
import os
def fileupload(file, path):
    ext=file.name.split('.')[-1]
    newfilename=datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(10000,99999))+'.'+ext
    savepath=os.path.join(os.path.join(settings.MEDIA_ROOT, path), newfilename)
    with open(savepath,'wb') as f:
        for content in file.chunks():
            f.write(content)
    return newfilename


