#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <signal.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <arpa/inet.h>

#include <opencv2/imgcodecs.hpp>
#include "opencv2/core/core.hpp"
#include <opencv2/core/types_c.h>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/objdetect.hpp>
#include <opencv2/videoio/videoio_c.h>

#define SOCKETNAME "/tmp/video"

using namespace cv;
using namespace std;

typedef struct
{
    Mat data;
    bool ready;
    bool send_mail;
} tparams;

bool capture = false;
int frames_detected = 0;
int mail_timer = 0;

void timer(int signum)
{
    capture = true;
    if (0 < mail_timer)
    {
        mail_timer++;
        if (mail_timer > 6000)
        {
            mail_timer = 0;
        }
    }
}

void end(int signum)
{
    printf("\nFechando o programa.\n");
    exit(signum);
}

void *capture_thread(void *pparams)
{
    tparams *params;
    params = (tparams *)pparams;

    // A imagem captada pela webcam -> adaptar para receber a imagem da câmera rpi.
    VideoCapture cap(0);
    // Iniciando a imagem.
    Mat img, gray;

    // Carregando modelo de detecção corporal/rosto.
    cv::HOGDescriptor hog;
    hog.setSVMDetector(cv::HOGDescriptor::getDefaultPeopleDetector());

    // CascadeClassifier detectorCascade;
    // detectorCascade.load("../models/haarcascade_fullbody.xml");

    // Mensagem de erro caso haja erro na abertura do modelo de detecção.
    // if (detectorCascade.empty())
    //{
    //    cout << "Arquivo XML não carregado" << endl;
    //    exit(-1);
    //}

    while (1)
    {
        while (!capture)
            ;
        capture = false;

        // Capturar imagem da webcam -> adaptar para receber a imagem da câmera rpi.
        cap.read(img);
        // Convertendo a escala de cor.
        cvtColor(img, gray, cv::COLOR_BGR2GRAY);
        // Criando um vetor para armazenar a pessoa detectada em um retângulo.
        // std::vector<cv::Rect> pessoa;
        vector<Rect> pessoa;
        //  Parâmetros de detecção.
        hog.detectMultiScale(gray, pessoa, 0, cv::Size(8, 8), cv::Size(32, 32), 1.2, 2);
        // hog.detectMultiScale(gray, pessoa, 1.1, 5, cv::CASCADE_SCALE_IMAGE, Size(30, 30));

        // Criando o retângulo na pessoa.
        // for (int i = 0; i < pessoa.size(); i++)
        //{
        //    rectangle(img, pessoa[i].tl(), pessoa[i].br(), Scalar(255, 0, 255), 2);
        //}
        for (int i = 0; i < pessoa.size(); i++)
        {
            rectangle(img, pessoa[i].tl(), pessoa[i].br(), Scalar(255, 0, 255), 2);
        }

        if (mail_timer == 0)
        {
            if (pessoa.size() > 0)
            {
                frames_detected++;
                if (frames_detected > 10)
                {
                    params->send_mail = true;
                }
            }
            else
            {
                frames_detected = 0;
            }
        } else {
            frames_detected = 0;
        }

        params->data = img.clone();
        params->ready = true;
    }
}

void *send_thread(void *pparams)
{
    tparams *params;
    params = (tparams *)pparams;

    struct sockaddr name;
    int socket_id = socket(PF_LOCAL, SOCK_STREAM, 0);
    name.sa_family = AF_LOCAL;
    strcpy(name.sa_data, SOCKETNAME);

    connect(socket_id, &name, sizeof(name));
    while (1)
    {
        while (!params->ready);
        params->ready = false;

        imwrite("./image.jpeg", params->data);
        if(params->send_mail) {
            params->send_mail = false;
            write(socket_id, "mail", 4);
            mail_timer++;
        } else {
            write(socket_id, "pic", 3);
        }
    }
    close(socket_id);
    end(0);
}

int main()
{
    signal(SIGINT, end);
    signal(SIGALRM, timer);
    ualarm(1000, 50e3);

    tparams params;
    params.ready = false;
    params.send_mail = false;

    pthread_t camera;
    pthread_create(&camera, NULL, &capture_thread, &params);

    pthread_t send;
    pthread_create(&send, NULL, &send_thread, &params);

    pthread_join(camera, NULL);
    pthread_join(send, NULL);

    return 0;
}
