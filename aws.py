#객체감지
import boto3 #AWS와 데이터를 주고받기위한 라이브러리

def detect_labels_local_file(photo):

    client = boto3.client('rekognition')
    
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    
    result=[]
    for label in response["Labels"]:
        name = label["Name"]
        confidence = label["Confidence"]
        result.append(f"{name} :{confidence:.2f}")
        
    r= '<br/>'.join(map(str,result))
    return r


def compare_faces(sourceFile, targetFile):

    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=0,SourceImage={'Bytes': imageSource.read()},TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        # position = faceMatch['Face']['BoundingBox']
        # similarity = str(faceMatch['Similarity'])
        # print('The face at ' +str(position['Left']) + ' ' +str(position['Top']) + ' matches with ' + similarity + '% confidence')
        r=f"동일 인물일 확률은 {faceMatch['Similarity']}%입니다"
    imageSource.close()
    imageTarget.close()
    return r
