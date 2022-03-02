import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np

# classe instanciada para realizar a interface com a câmera.
class VideoCamera(object):
    def __init__(self, flip = False):
        # iniciar a gravação da imagem em tempo real.
        self.vs = PiVideoStream().start() 
        # inverte a ordem dos elementos da matriz ao longo do eixo especificado, 
        # preservando a forma da matriz.
        self.flip = flip 
        # iniciar a execução após 2 segundos.
        time.sleep(2.0)

    # deleta o self como atributo da classe instanciada ao parar a gravação
    def __del__(self):
        self.vs.stop()

    # retorna um frame da câmera 
    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    # conecta ao stream do vídeo e obtém o frame da câmera
    def get_frame(self):
        # lê o frame
        frame = self.flip_if_needed(self.vs.read())
        # Comprime a imagem em uma extensão jpeg e codifica em um buffer de memória.
        ret, jpeg = cv2.imencode('.jpg', frame)
        # retorna os dados da imagem como uma string contendo os bytes do frame.
        return jpeg.tobytes()

    # Encontra a pessoa na imagem utilizando um classificador de imagem
    def get_object(self, classifier):
        found_objects = False
        frame = self.flip_if_needed(self.vs.read()).copy() 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # parâmetros do classificador como tamanho, cor.
        objects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Condição para que uma pessoa seja detectada
        if len(objects) > 0:
            found_objects = True

        # Desenhar um retângulo ao redor da pessoa identificada
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return (jpeg.tobytes(), found_objects)