import os
import numpy as np
import io
import base64
import signal
import cv2
from io import BytesIO 
from PIL import Image
from pathlib import Path
import tornado.ioloop
import tornado.web
from tornado.options import options
import pyfakewebcam
import time

WIDTH, HEIGHT = None, None
fakecam = None
fake_webcam_path = '/dev/video42'

accect_ctlc = False


## 偽装カメラの初期化
def init_fakecam(w, h):
    global fakecam, WIDTH, HEIGHT
    WIDTH, HEIGHT = w, h

    ## カメラ偽装の初期化
    fakecam = pyfakewebcam.FakeWebcam(fake_webcam_path, w, h)
    print("[init] fake_cam, [w, h] %d, %d"%(w,h))


## カメラ偽装の更新
def update_fakecam(frame):
    global fakecam
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    fakecam.schedule_frame(rgb_frame)


def signal_handler(signum, frame):
    global accect_ctlc
    accect_ctlc = True

def try_exit(): 
    global accect_ctlc
    if accect_ctlc:
        tornado.ioloop.IOLoop.instance().stop()


class VCamHandler(tornado.web.RequestHandler):
    def post(self, *arg, **kwargs):
        try:
            base64_png = self.get_argument("image")

            ## ヘッダー削除
            code = base64.b64decode(base64_png.split(',')[1])
            
            ## PILイメージ <- バイナリーストリーム
            image_pil = Image.open(BytesIO(code))

            ## numpy配列(RGBA) <- PILイメージ
            img_numpy = np.asarray(image_pil)

            ## numpy配列(BGR) <- numpy配列(RGBA)
            frame = cv2.cvtColor(img_numpy, cv2.COLOR_RGBA2BGR)

            h, w = frame.shape[:2]

            if fakecam == None:
                ## 偽装カメラの初期化
                init_fakecam(w, h)

            ## 偽装カメラの更新
            update_fakecam(frame)

        except:
            pass


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


def get_root_path():
    return Path(__file__).resolve().parents[0]


def make_app():
    BASE_DIR=get_root_path()
    return tornado.web.Application([
            (r"/", MainHandler),
            (r"/fakewebcam", VCamHandler),
        ],
        static_path=os.path.join(BASE_DIR, "static"),   
        template_path=os.path.join(BASE_DIR, "templates"),
    )


if __name__ == "__main__":
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    app = make_app()
    app.listen(8888)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start() 
    tornado.ioloop.IOLoop.instance().start()
