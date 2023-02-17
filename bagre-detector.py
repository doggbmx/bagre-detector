import boto3
import cv2
from botocore.exceptions import ClientError
from gtts import gTTS
import os

captura = cv2.VideoCapture(0)
cliente = boto3.client('rekognition', region_name='us-east-1')

bagre_mayor = '/home/manu/Documents/bagre_mayor.jpg'

text = 'ALERT! THE KING OF CATFISH DETECTED, WELCOME HOME SIR'
tts = gTTS(text)
tts.save('bagre.mp3')


def obtener_bytes(ruta_imagen):
    with open(ruta_imagen, 'rb') as imagen:
        return imagen.read()


def comparar_rostros(ruta_imagen1, ruta_imagen2):
    # bytes_1 = obtener_bytes(ruta_imagen1)
    bytes_2 = obtener_bytes(ruta_imagen2)

    try:
        respuesta = cliente.compare_faces(
            SourceImage={'Bytes': ruta_imagen1.tobytes()}, TargetImage={'Bytes': bytes_2}, SimilarityThreshold=60, QualityFilter='AUTO')

        if respuesta and respuesta['ResponseMetadata']['HTTPStatusCode'] == 200:
            # print(respuesta.keys())
            for i in respuesta['UnmatchedFaces']:
                print('NOOOOO ERES UN BAGREEEEEE')
                # print(i)
                # print('/n')

            for i in respuesta['FaceMatches']:
                if i['Similarity'] > 60:
                    print('ERES UN BAGRE')
                    os.system('aplay bagre.wav')
                else:
                    print('NOOOOO ERES UN BAGREEEEEE')
                print('Similarity: ' + str(i['Similarity']))
    except ClientError as error:
        print('Error llamando a la api rekognition:' + str(error))


# if __name__ == '__main__':
#     ruta_imagen1 = '/home/manu/Documents/uno.jpg'
#     bagre_mayor = '/home/manu/Documents/bagre_mayor.jpg'
#     comparar_rostros(ruta_imagen1, bagre_mayor)
while True:
    ret, frame = captura.read()

    comparar_rostros(cv2.imencode('.jpg', frame)[1], bagre_mayor)

    cv2.imshow('BAGRE DETECTOR 420', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()
