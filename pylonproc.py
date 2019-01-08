import imageio
import cv2
import numpy
import time
import os
import errno
import math
import logging
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from vispy import app, gloo

logger = logging.getLogger(__name__)


class QCamProcessor(QObject):

    img_processed = pyqtSignal(object)
    status = pyqtSignal(str)
    is_running = pyqtSignal()
    is_processing = pyqtSignal(numpy.ndarray)

    def __init__(self):
        super().__init__()

    #Only this method should be overridden
    @pyqtSlot(numpy.ndarray)
    def processImg(self, img=numpy.ndarray):
        return 0

    def startProcessing(self, img_received=pyqtSignal(numpy.ndarray)):
        #Handle QThread related stuff (i.e. signals and stuff here)
        #This runs in MainThread so don't put loops here.
        #processImg runs in separate thread.

        self.is_processing = img_received
        self.is_processing[numpy.ndarray].connect(self.processImg)


    #when cancel signal is received
    def cancelProcessing(self):
        try:
            self.is_processing[numpy.ndarray].disconnect(self.processImg)
        except Exception as e:
            logger.exception(str(e))

    #clean up processing, i.e. save file etc.
    def finishProcessing(self):
        self.img_processed.emit()


class QCamRecorder(QCamProcessor):

    img_processed = pyqtSignal()
    frame_written = pyqtSignal()  # just to let the progressBar know when to update
    fimjson_path = pyqtSignal(str)
    timelimit_reached = pyqtSignal()

    fpath = ''

    codec = 'XVID'

    def __init__(self):
        super().__init__()
        self.fourcc = None
        self.out = None  # imageio.get_writer(...)
        self.fps = 41.58177  # max. FPS
        self.maxframes = 100  # arbitrary so that we record at least something for testing purposes
        self.framecount = 0
        self.fimjson = ''
        self.iscancelled = False
        self.resolution = (1200, 1200)

    # @pyqtSlot(float)
    def changeFps(self, newfps):
        self.fps = newfps
        self.status.emit("Will record at " + str(self.fps) + " fps.")
        logger.debug("Will record at " + str(self.fps) + " fps.")

    def msecsToFrames(self, mseconds):
        self.maxframes = math.floor(self.fps * mseconds / 1000)  # Rounding down for consistency
        self.status.emit("Will record " + str(self.maxframes) + " frames.")
        logger.debug("Will record " + str(self.maxframes) + " frames.")

    def startProcessing(self, img_received=pyqtSignal(numpy.ndarray)):
        currenttime = time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime())
        subpath = os.path.join(self.fpath, currenttime)
        if not os.path.exists(subpath):
            try:
                os.makedirs(subpath)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        fimfile = 'FIM_' + currenttime + '.avi'
        self.fimjson = os.path.join(subpath, 'FIM_' + currenttime + '.json')
        self.fourcc = cv2.VideoWriter_fourcc(*self.codec)
        #self.out = imageio.get_writer(os.path.join(subpath, fimfile), 'ffmpeg', 'I', fps=self.fps, codec=self.codec)
        self.out = cv2.VideoWriter(os.path.join(subpath, fimfile), self.fourcc, self.fps, self.resolution, False)
        self.iscancelled = False
        super().startProcessing(img_received)

    def processImg(self, img=numpy.ndarray):
        try:
            if self.framecount < self.maxframes and not self.iscancelled:
                # imageio is very expensive and slows down grabbing and recording threads.
                #self.out.append_data(img)
                self.out.write(img)
                self.frame_written.emit()
                self.framecount += 1
            elif self.framecount >= self.maxframes:
                self.timelimit_reached.emit()
        except Exception as e:
            logger.exception(str(e))

    def cancelProcessing(self):
        self.iscancelled = True
        super().cancelProcessing()
        self.finishProcessing()

    def finishProcessing(self):
        #self.out.close()
        self.out.release()
        self.status.emit("Released file.")
        logger.debug("Released file.")
        self.fimjson_path.emit(self.fimjson)
        super().finishProcessing()


class Canvas(app.Canvas):
    vertex = """
                attribute vec2 position;
                attribute vec2 texcoord;
                varying vec2 v_texcoord;
                void main()
                {
                    gl_Position = vec4(position, 0.0, 1.0);
                    v_texcoord = texcoord;
                }
            """
    fragment = """
                uniform sampler2D texture;
                uniform vec2 mousecoord;
                uniform float mousezoom;
                varying vec2 v_texcoord;
                void main()
                {
                    gl_FragColor = texture2D(texture, v_texcoord);
                    
                    float mouse_dist = distance(v_texcoord, mousecoord);
                    
                    //Draw the outline of the glass
                    if (mouse_dist < 0.205)
                        gl_FragColor = vec4(0.1, 0.1, 0.1, 1.0);
                    //Draw a zoomed-in version of the texture
                    if (mouse_dist < 0.2)
                        gl_FragColor = texture2D(texture, (v_texcoord + mousecoord) / 2.0);
                }
            """
    currentframe = None

    def __init__(self):
        app.Canvas.__init__(self)
        #self.currentframe = numpy.zeros((framedimx, framedimy, 3)).astype(numpy.uint8)
        self.image = gloo.Program(self.vertex, self.fragment, 4)
        self.image['position'] = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
        # bottom left, top left, bottom right, top right
        # This works on Windows. But why are the textures smaller?
        #self.image['texcoord'] = [(0, 1/3), (0, 0), (1/3, 1/3), (1/3, 0)]
        # This works on linux:
        # (where DPI can't be determined automatically
        self.image['texcoord'] = [(0, 1), (0, 0), (1, 1), (1, 0)]
        # How Can I stretch textures and why is that necessary?
        #self.image['texture'] = self.currentframe

        width, height = self.physical_size
        gloo.set_viewport(0, 0, height, height)
        gloo.set_clear_color('black')

    def on_resize(self, event):
        width, height = event.physical_size
        if width < height:
            gloo.set_viewport(0,
                              abs((height - width) / 2),
                              width,
                              width)
        else:
            gloo.set_viewport(abs((width - height) / 2),
                              0,
                              height,
                              height)

    def on_draw(self, event):
        gloo.clear('black')
        #self.image['texture'][...] = self.currentframe
        self.image['texture'] = self.currentframe
        self.image.draw('triangle_strip')
        self.update()

    def updateFrame(self, newframe=numpy.ndarray):
        self.currentframe = newframe

    def on_mouse_move(self, event):
        x, y = event.pos
        self.image['mousecoord'] = (x/self.size[0], y/self.size[1])
        self.on_draw(event)

    # def on_mouse_wheel(self, event):
    #    _, delta = event.delta
    #    self.image['mousezoom'] = delta


class QCamGLPreview(QCamProcessor):

    def __init__(self):
        super().__init__()
        self.canvas = Canvas()

    def processImg(self, img=numpy.ndarray):
        self.canvas.updateFrame(img)
        self.status.emit("Updating framebuffer.")

    def startProcessing(self, img_received=pyqtSignal(numpy.ndarray)):
        super().startProcessing(img_received)
        app.use_app(backend_name="PyQt5", call_reuse=True)


class QCamSnapshot(QCamProcessor):
    img_processed = pyqtSignal()
    fpath = ''

    def processImg(self, img=numpy.ndarray):
        currenttime = time.strftime('%d-%m-%Y_%H-%M-%S', time.localtime())
        fimfile ='FIMsnapshot_' + currenttime + '.png'
        fpath = os.path.join(self.fpath, fimfile)
        # we just want to save one frame, so when we receive one,
        # we immediately stop by checking if there is already a file saved.
        if not os.path.isfile(fpath):
            try:
                imageio.imwrite(fpath, img)
                self.status.emit(fimfile)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        self.cancelProcessing()  # we just want to save one frame, so when we receive one, we immediately stop.
        self.finishProcessing()
