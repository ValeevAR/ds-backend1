import requests
from PIL import UnidentifiedImageError

class PlateClient:
    def __init__(self, url: str):
        self.url = url

    def readNumber(self, im) -> str:
        try:
            res = requests.post(
                f'{self.url}/readNumber',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                data = im
            )
            return res.json()['name']

        except UnidentifiedImageError: 
            return {'error': 'invalid image' }, 400

        except KeyError: 
            return {'error': 'image is not found'}, 501


def url_to_number(client, base_image_url, ID):
    '''
    Функция принимает ID картинки и возвращает распознанный номер
    '''
    image_number = int(ID)
    image_url = base_image_url + str(image_number)
    res = requests.get(image_url)   
    number = client.readNumber(res)
    return number


if __name__ == '__main__':
    client = PlateClient('http://127.0.0.1:8080')

    with open('images/10022.jpg', 'rb') as im:
        res = client.readNumber(im)

    print(res)

