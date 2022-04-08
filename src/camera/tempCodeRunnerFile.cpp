void main()
{

    VideoCapture cap(0);
    Mat img;

    while (true)
    {

        cap.read(img);
        imshow("Image", img);
        waitKey(1);
    }
}