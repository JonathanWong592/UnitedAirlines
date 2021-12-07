import boto3
import io
import json
from PIL import Image, ImageDraw, ExifTags, ImageColor


def detect_text(photo, bucket, inputNumKioskFromManager):
    print(inputNumKioskFromManager)
    f = open('TestKioskData.json')
    data = json.load(f)
    client=boto3.client('rekognition')

    # # Load image from S3 bucket
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket,photo)
    s3_response = s3_object.get()
    stream = io.BytesIO(s3_response['Body'].read())
    # print(stream)
    image=Image.open(stream)

    imgWidth, imgHeight = image.size  
    draw = ImageDraw.Draw(image)

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    # print(response)
    textDetections=response['TextDetections']

    # print(textDetections)
    # print ('Detected text\n----------')
    # print(textDetections)
    numArray = []
    id = 0
    # inputNumKioskFromManager = 5
    # inputNumKioskFromManager = 3
    confirmedNumArray = [i + 1 for i in range(inputNumKioskFromManager)]

    coordinates = {}
    for text in textDetections:
        # print(text)
        # print(text['DetectedText'], "TESTY")
        if(not (text['DetectedText'].isdigit())):
            # print(text['DetectedText'])
            continue
        else:
        # if text['DetectedText']
            # print ('Detected text:' + text['DetectedText'])
            # print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            # print ('Id: {}'.format(text['Id']))
            # if 'ParentId' in text:
            #     print ('Parent Id: {}'.format(text['ParentId']))
            # print ('Type:' + text['Type'])
            # print()

            # print(text)
            box = text['Geometry']['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']

            temp_coords = {
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height
            }

            # Call function to retrieve information from kiosk data.
            # In our case, we will just use dummy data stored in json file
            # Inputs -> CollectKioskData(Hub, Area (General, VIP))
            # Outputs -> Returns array 
            # CollectKioskData(Newark, General)
            # {(Kiosk) 1:JSON Data, 2:JSON Data, 3:JSON Data, 4:JSON Data, 5:JSON Data}
            temp_kiosk_data = data[str(text['DetectedText'])]
            
            # merge both json objects
            merged = {**temp_coords, **temp_kiosk_data}

            # print(merged)
            coordinates[int(text['DetectedText'])] = merged
            # print(coordinates)
            # points = (
            #     (left,top),
            #     (left + width, top),
            #     (left + width, top + height),
            #     (left , top + height),
            #     (left, top)
            # )

            # first find the kiosk line, and get all numbers into an array
            # print("Length of text: " , len(text['DetectedText'].replace(" ", "")))
            # print(len(text['DetectedText'].replace(" ", "")))
            # print(inputNumKioskFromManager)
            # if len(text['DetectedText'].replace(" ", "")) == inputNumKioskFromManager:
            #     split = text['DetectedText'].split(' ')
            #     # print(split)
            #     for i in range(inputNumKioskFromManager):
            #         if str(i + 1) in split:
            #             numArray.append(i+1)

            #     if numArray == confirmedNumArray:
            #         id = text['Id']
                
            #     print(numArray)

            # if (text['DetectedText'].isdigit()) and int(text['DetectedText']) in numArray and text['ParentId'] == id:
                
            #     temp_coords = {
            #         "left": left,
            #         "top": top,
            #         "width": width,
            #         "height": height
            #     }

            #     # Call function to retrieve information from kiosk data.
            #     # In our case, we will just use dummy data stored in json file
            #     # Inputs -> CollectKioskData(Hub, Area (General, VIP))
            #     # Outputs -> Returns array 
            #     # CollectKioskData(Newark, General)
            #     # {(Kiosk) 1:JSON Data, 2:JSON Data, 3:JSON Data, 4:JSON Data, 5:JSON Data}
            #     temp_kiosk_data = data[str(text['DetectedText'])]
                
            #     # merge both json objects
            #     merged = {**temp_coords, **temp_kiosk_data}

            #     print(merged)
            #     coordinates[int(text['DetectedText'])] = merged
            #     print(coordinates)

    # print(coordinates)
    return coordinates

# def main():

#     bucket="image.processing.rekognition"
#     # photo="Kiosk Labeled Updated.jpg"
#     photo="Straight Labels.jpg"
#     text_count=detect_text(photo,bucket)
#     print("Text detected: " + str(text_count))


# if __name__ == "__main__":
#     main()