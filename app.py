from flask import Flask, render_template, Response, request, send_from_directory
import cv2
from PIL import Image, ImageDraw, ExifTags, ImageColor
from numpy import asarray
import io
import DetectText
import time
import boto3
import os

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

class DataStore():
    dataKiosks = 0

data = DataStore()


def upload_picture(bucket):
    # connect to aws acc
    client = boto3.client('s3', region_name='us-east-1', aws_access_key_id=os.getenv('AWSAccessKeyId'), aws_secret_access_key=os.getenv('AWSSecretKey'))
    success, frame = camera.read()
    
    ret, buffer = cv2.imencode('.jpg', frame)
    # print(ret)
    # print(buffer)
    frame = buffer.tobytes()
    client.put_object(Body=frame, Bucket=bucket, Key="Test.jpg", ContentType=request.mimetype)
    return {'message': 'image uploaded'}

def gen_frames():  # generate frame by frame from camera
    start_time = time.perf_counter()
    bucket="image.processing.rekognition"

    # photo = "Kiosk Labeled Updated.jpg"
    photo="Test.jpg"
    # numberKiosks = kiosks
    # numberKiosks = 5
    numberKiosks = data.dataKiosks
    coordinates = DetectText.detect_text(photo, bucket, numberKiosks)
    # print(coordinates)
#     coordinates = [
#     {'left': 179.00000274181366, 'top': 315.9999918937683, 'width': 82.01371729373932, 'height': 110.0020158290863, 'status': 'Functional', 'color': 'Green', 'colorCode': '#00FF00', 'Reasons': {}},
#     {'left': 498.99998903274536, 'top': 320.0000023841858, 'width': 75.99999815225601, 'height': 92.99999713897705, 'status': 'Possibly Functional', 'color': 'Yellow', 'colorCode': '#FFFF00', 'Reasons': {'1': "User hasn't interacted in 24 hours"}},
#     {'left': 825.0000071525574, 'top': 322.99999952316284, 'width': 71.01584494113922, 'height': 97.00915932655334, 'status': 'Non-Functional', 'color': 'Red', 'colorCode': '#FF0000', 'Reasons': {'1': 'UI Broken'}}
# ]


    # send input to InformationBoxes.js


    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Re-capture an image of the kiosks every 10 seconds
            if int(time.perf_counter()) - int(start_time) == 10000:
                # Inputs -> DetectText(-NumberOfKiosks, -)
                # Outputs -> Return Adjusted Points (Take size of number, and multiply up to size of Kiosk)
                # DetectText(5)
                # Coordinate Array -> {1: {Coordinates}, 2: {}...}
                coordinates = DetectText.detect_text(photo, bucket, numberKiosks)
                # print(coordinates)
                start_time = time.perf_counter()

            else:
                imgWidth  = camera.get(3)  # float `width`
                imgHeight = camera.get(4)
                # print(imgWidth)
                # print(imgHeight)
                # print(imgWidth, imgHeight)
                # 1280 x 720 (basically how good the camera is)
                # turning numpy array into an actual image
                # data = Image.fromarray(frame)

                # create images on the picture for X amount of kiosks (NumberOfKiosks)
                for i in range(1, numberKiosks + 1):
                    left = int(coordinates[i]['left'])
                    top = int(coordinates[i]['top'])
                    width = int(coordinates[i]['width'])
                    height = int(coordinates[i]['height'])
                    
                    # adding 200 to account for video being shown in 1280 * 720
                    # and picture being taken in 1080 * 720
                    # left = int(coordinates[i-1]['left'])
                    # top = int(coordinates[i-1]['top'])
                    # width = int(coordinates[i-1]['width'])
                    # height = int(coordinates[i-1]['height'])
                    # color code based on received information (cv2 uses BGR, not RGB, so switch colors accordingly)
                    colorCode = {
                        "Red": (0, 0, 255),
                        "Yellow": (0, 255, 255),
                        "Green": (0,255,0)
                    }

                    # () -> Start coordinate: left corner
                    # () -> Ending coordinate: bottom right corner
                    # 'left': 179.00000274181366, 'top': 315.9999918937683, 'width': 82.01371729373932, 'height': 110.0020158290863

                    image = cv2.rectangle(frame, (left, top), (left + width, top + height), colorCode[coordinates[i]['color']], 2)

                    # image = cv2.rectangle(frame, (left, top), (left + width, top + height), colorCode[coordinates[i-1]['color']], 2)
                    # RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                

                # turning image back into numpy array
                numpydata = asarray(image)

                ret, buffer = cv2.imencode('.jpg', numpydata)
                frame = buffer.tobytes()

                
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/more_info/<id>')
def more_info(id):
    # print(id)
    workingdir = os.path.abspath(os.getcwd())
    filepath = workingdir + '/static/files/'
    file = "KioskData-part-" + id + ".pdf"
    return send_from_directory(filepath, file)


@app.route('/<int:kiosks>')
def index(kiosks):
    """Video streaming home page."""
    bucket="image.processing.rekognition"
    resp = upload_picture(bucket)
    # print(resp)
    bucket="image.processing.rekognition"
    photo="Test.jpg"
    # numberKiosks = 3
    # numberKiosks = 5
    # print(kiosks)
    data.dataKiosks = kiosks
    # print(kiosks)
    coordinates = DetectText.detect_text(photo, bucket, kiosks)
    # print(coordinates)
    # print("HELLO")
    # if(len(coordinates) == kiosks):
    return render_template('index.html', coordinates=coordinates, kiosks=kiosks)
    # else:
        # print("INSIDE")
        # just return the live video feed
        # return render_template('failedFind.html')

@app.route('/', methods=['POST'])
def my_form_post():
    numKiosks = request.form['text']
    # processed_text = text.upper()
    print(numKiosks)
    return numKiosks

# @app.route('/handle_data', methods=['GET'])
# def handle_data():
#     print("TEST")
#     dic = {}

#     dic["numKiosks"] = request.args.get('numKiosks')
#     # dic["newOrNot"] = request.form['newOrNot']
#     # dic["nameOfExisting"] = request.form['nameOfExisting']
#     # return dic
#     return

if __name__ == '__main__':
    app.run(debug=True)