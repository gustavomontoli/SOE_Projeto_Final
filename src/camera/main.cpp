#include <opencv2/imgcodecs.hpp>
#include "opencv2/core/core.hpp"
#include <opencv2/core/types_c.h>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/objdetect.hpp>
#include <opencv2/videoio/videoio_c.h>
#include <iostream>
#include <unistd.h>

using namespace cv;
using namespace std;

int main()
{
    // A imagem captada pela webcam -> adaptar para receber a imagem da câmera rpi.
    VideoCapture cap(0);
    // Iniciando a imagem.
    Mat img, gray;

    // Carregando modelo de detecção corporal/rosto.
    CascadeClassifier detectorCascade;
    detectorCascade.load("../models/facial_recognition_model.xml");

    // Mensagem de erro caso haja erro na abertura do modelo de detecção.
    if (detectorCascade.empty())
    {
        cout << "Arquivo XML não carregado" << endl;
        return -1;
    }

    while(1){
        // Capturar imagem da webcam -> adaptar para receber a imagem da câmera rpi.
        cap.read(img);
        // Convertendo a escala de cor.
        cvtColor(img, gray, cv::COLOR_BGR2GRAY);
        // Criando um vetor para armazenar a pessoa detectada em um retângulo.
        vector<Rect> pessoa;
        // Parâmetros de detecção.
        detectorCascade.detectMultiScale(gray, pessoa, 1.1, 5, cv::CASCADE_SCALE_IMAGE, Size(30, 30));

        // Criando o retângulo na pessoa.
        for (int i = 0; i < pessoa.size(); i++)
        {
            rectangle(img, pessoa[i].tl(), pessoa[i].br(), Scalar(255, 0, 255), 2);
        }

        imwrite("../image.jpeg", img);
        usleep(40e3);
    }

    return 0;
}