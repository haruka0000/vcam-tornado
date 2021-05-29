import os
import tornado.ioloop
import tornado.web
from tornado.escape import json_decode, json_encode
import signal
from tornado.options import options
from pathlib import Path
import numpy as np
import io
from PIL import Image
import base64
from io import BytesIO 
from tornado.httpclient import AsyncHTTPClient

accect_ctlc = False

def signal_handler(signum, frame):
    global accect_ctlc
    accect_ctlc = True

def try_exit(): 
    global accect_ctlc
    if accect_ctlc:
        tornado.ioloop.IOLoop.instance().stop()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world")


class VCamHandler(tornado.web.RequestHandler):
    def post(self, *arg, **kwargs):
        # request_json = json_decode(self.request.body)
        try:
            base64_png = self.get_argument("data")
            code = base64.b64decode(base64_png.split(',')[1])  # remove header
            image_decoded = Image.open(BytesIO(code))

            print(image_decoded.size)
        except:
            pass
        # #バイナリーストリーム <- バリナリデータ
        # img_binarystream = io.BytesIO(request_json['data'].encode())

        # #PILイメージ <- バイナリーストリーム
        # img_pil = Image.open(img_binarystream)
        # # print(img_pil.mode) #この段階だとRGBA

        # #numpy配列(RGBA) <- PILイメージ
        # img_numpy = np.asarray(img_pil)

        # print(img_numpy.shape)
        # #numpy配列(BGR) <- numpy配列(RGBA)
        # img_numpy_bgr = cv2.cvtColor(img_numpy, cv2.COLOR_RGBA2BGR)
        self.render("camera.html", username=" static")
        
class CameraHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("camera.html", username=" static")

def get_root_path():
    return Path(__file__).resolve().parents[0]

def make_app():
    BASE_DIR=get_root_path()
    return tornado.web.Application([
            (r"/", MainHandler),
            (r"/static", CameraHandler),
            (r"/vcam", VCamHandler),
        ],
        static_path=os.path.join(BASE_DIR, "static"),        #※1
        template_path=os.path.join(BASE_DIR, "templates"),   #※2
    )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start() 
    tornado.ioloop.IOLoop.instance().start()
