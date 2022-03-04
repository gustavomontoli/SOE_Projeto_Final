# Biblioteca Flask para implementar a aplicação web e receber as imagens da câmera
# Biblioteca OpenCV para implementar a detecção da pessoa através da imagem
import cv2
from flask import Flask, render_template, Response

# O objeto Flask inicializará parâmetros necessários para construir a aplicação web
app = Flask(__name__)

# Definir a saída como a imagem captada pela webcam.
video_camera = cv2.VideoCapture(0)
# Este objeto irá inicializar um modelo de detecção corporal.
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml")


# Template do aplicativo
@app.route('/')
def index():
    return render_template('index.html')


# função para receber a imagem da webcam e detectar o corpo da pessoa e
# definir um retângulo delimitador
def gen(video_camera):
    while True:
        # Ler frame a frame
        success, frame = video_camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Parâmetros do classificador de objeto
        objects = object_classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Desenhar um retângulo ao redor da pessoa identificada
        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if not success:
            break
        else:
            # a função gera uma imagem com o formato .jpeg e a converte em bytes.
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Identificador de acesso ao link da web que recebem a imagem da webcam
@app.route('/video_feed')
def video_feed():
    global video_camera  # diferenciar de outras variáveis
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Inicializa o app.run para executar o aplicativo flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)
