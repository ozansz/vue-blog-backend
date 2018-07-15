import uuid
import hashlib

def mdV(s):
    def _md5(s):
        m = hashlib.md5()
        m.update(s.encode('utf8'))
        return m.hexdigest()

    ret = s

    for _ in range(5):
        ret = _md5(ret)

    return ret

def auto_rename_img(instance, filename):
    return "static/post_images/{0}/{1}.{2}".format(mdV(str(instance.id)), uuid.uuid4().hex, filename.split('.')[-1])
