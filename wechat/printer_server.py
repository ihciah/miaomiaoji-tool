#!/usr/bin/python
# __author__="ihciah"
# Need twisted and pyopenssl

from twisted.web import resource
from twisted.web import server as webserver
from twisted.internet import reactor
from OpenSSL.SSL import Context, TLSv1_METHOD
import time, requests, cv2, threading, logging
import numpy as np
from message_process import BtManager
from image_process import ImageConverter

KEY = "AABBCCDD"
HTTP_PORT = 20000
mutex = threading.Lock()


def print_image(url):
    global mutex
    img_file = requests.get(url)
    image = np.asarray(bytearray(img_file.content), dtype='uint8')
    im = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
    pixels = ImageConverter.im2bmp(im)
    mutex.acquire()
    try:
        mmj = BtManager("69:68:63:69:61:68")
        if mmj.connected:
            stop = int(time.time()) + len(pixels) / 384 / 5
            mmj.sendImageToBt(pixels)
            mmj.disconnect()
            time_to_sleep = stop - int(time.time())
            time.sleep(time_to_sleep if time_to_sleep > 0 else 0)
    finally:
        mutex.release()

class HTTPServer(resource.Resource):
    isLeaf = True

    def getarg(self, req, arg):
        args = req.args
        if arg not in args or len(args[arg]) == 0:
            return None
        return args[arg][0]

    def validate(self, authcode):
        return authcode == KEY

    def render_POST(self, request):
        try:
            if request.uri == '/print':
                auth = self.getarg(request, 'Auth')
                if auth and self.validate(auth):
                    url = self.getarg(request, 'IMG_URL')
                    user = self.getarg(request, 'USER') or "NO_USER"
                    t = threading.Thread(target=print_image, args=(url,))
                    t.start()
                    ret = "Image submitted by wechat user:%s" % user
                    logging.info(ret)
                    return ret
            request.setResponseCode(403)
            return "403 Forbidden"
        except:
            pass


class ContextFactory:
    def __init__(self, context):
        self.context = context

    def getContext(self):
        return self.context


def main():
    cert = "/etc/ssl/ihc/crt"
    key = "/etc/ssl/ihc/key"

    httpserver = webserver.Site(HTTPServer())
    context = Context(TLSv1_METHOD)
    context.use_certificate_chain_file(cert)
    context.use_privatekey_file(key)

    reactor.listenSSL(HTTP_PORT, httpserver, ContextFactory(context), interface='192.168.102.130')

    reactor.run()


if __name__ == '__main__':
    try:
        logging.getLogger().setLevel(logging.INFO)
        main()
    except:
        pass

