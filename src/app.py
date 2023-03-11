from flask import Flask, request
import logging
from models.plate_reader import PlateReader
from PIL import UnidentifiedImageError
import io
from plate_client import PlateClient
from plate_client import url_to_number
import requests

app = Flask(__name__)

plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')
client = PlateClient('http://127.0.0.1:8080')
base_image_url = 'http://51.250.83.169:7878/images/'


@app.route('/')
def hello():
    return f'<h1><center>Hello!</center></h1>'


@app.route('/getimage/<ID>', methods=['GET'])
def readNumberFromUrl(ID):
    '''
    Прием одной картинки по шаблону
    /getimage/10022'
    '''
    try:
        # функция url_to_number из plate.client - принимает ID картинки и возвращает распознанный номер
        number = url_to_number(client, base_image_url, ID)
    except UnidentifiedImageError: 
        return {'error': 'invalid image'}, 400
    return {"name" : number}



@app.route('/getimages/<IDs>', methods=['GET'])
def multireadNumberFromUrl(IDs):
    '''
    Прием нескольких картинок происходит через нижнее подчеркивание.
    Пример запроса:
    /getimages/10022_9965'
    '''    
    list_IDs = IDs.split('_')
    numbers = []

    try:
        for ID in list_s:
            number = url_to_number(client, base_image_url, ID)
            numbers.append(number)
    except UnidentifiedImageError: 
        return {'error': f'invalid image {ID}' }, 400

    return {"name" : numbers}


@app.route('/readNumber', methods=['POST'])
def readNumber():
    body = request.get_data()
    im = io.BytesIO(body)    

    try:
        res = plate_reader.read_text(im)
    except UnidentifiedImageError:
        return {'error': 'invalid image'}, 400

    return {"name" : res}


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
