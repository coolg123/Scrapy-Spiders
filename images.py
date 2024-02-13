import scrapy
import json
from scrapy.http import Request
import re
import random

def create_image_url(data):
    base_url = data["media"]["baseUri"]
    pretty_name = data["media"]["prettyName"]
    tokens = data["media"]["token"]
    full_view = data["media"]["types"][-3]
    height = full_view["h"]
    width = full_view["w"]
    _150 = data["media"]["types"][0]['c']

    _150 = re.sub(r'w_\d+', f'w_{width}', _150)
    _150 = re.sub(r'h_\d+', f'h_{height}', _150)
    token = random.choice(tokens)
    image_url = base_url + _150.replace('<prettyName>', pretty_name) + "?token=" + token

    return image_url

header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.deviantart.com/hypnoman/gallery',
            'Sec-Ch-Ua': '" Not A;Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Ch-Viewport-Height': '1080',
            'Sec-Ch-Viewport-Width': '1920',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

class ImagesSpider(scrapy.Spider):
    name = "images"
    allowed_domains = ["deviantart.com"]

    def start_requests(self):
        
        cookies = {
            '_pxvid': '9948a61b-4c6b-11ee-a51f-ac1607864526',
            '_px': 'o64jFhRR5LdFlp4HgZSQgOLAU2OoIgToY4FnlBlvQjn6FpAqhd8mxfZ+HpwbikSA4vcE+QNxaeKVekkDKsyl2Q==:1000:sqQwSF2hBcWiRl8Yb7gM0c3s4s0i5TkBvBkgoNDV6JfSoSHUcqiNHJQWchBr85kymsnmZCibXqAIi1qrjLimpdHCzZvKJD/3rlUAS0Fh8Hvmxu21f1eaIusSSGEfpre4yW5Nh7nHNRn0rYLXeD17kGDSGrarfEF97DSOdiyXg4oh/UPWff7lRUs+LyMiIANoUPY17zue01kY0vJQdr/28AJOU+msg/OgeIVkuWWF4JOr9pkQ4jsXF+l1bbzCNnJmOOQdsr1iW6ou9I4I2eq9Rw==',
            'auth_secure': '__b90f3ac403a6c8b3b1af%3B%22f4c67a62c519c41cc31dca98a69ad540%22',
            'userinfo': '__8e081dc172b85a10196a%3B%7B%22username%22%3A%22randomcoolgenius%22%2C%22uniqueid%22%3A%22bdafe0d623e4caeb3337648c9f6486e4%22%2C%22dvs9-1%22%3A1%2C%22ab%22%3A%22tao-0cb-1-b-7%7Ctao-dh1-1-b-7%7Ctao-me1-1-a-3%22%2C%22pv%22%3A%22c%3D1%2C1%2C1%2C1%22%7D',
            'auth': '__5dc81fa2956dcb9af94d%3B%229279140d02058cf5c13348d726e53acf%22',
            'td': '0:2054%3B3:445%3B10:445%3B12:2174.15380859375x1277.5384521484375',
        }


        url = "https://www.deviantart.com/_puppy/dashared/gallection/contents?username=dollmistress&type=gallery&offset=24&limit=24&all_folder=true&csrf_token=coqpp0Qy8ZBqUOWm.s8jlmm.0HhmNcG2KruMNYdSOxrUMRgewlTeemYivtHMEpGK6tM&da_minor_version=20230710"


        yield Request(url, headers=header, cookies=cookies, callback=self.parse)

    def parse(self, response):
        response = json.loads(response.body)

        for image in response['results']:
            try:
                image_url = create_image_url(image)
                yield {
                    'image_name': image['media']["prettyName"],
                    'image_url': image_url,
                }
            except Exception as e:
                print(e)
                continue

        next_offset = response["nextOffset"]
        
        if next_offset != None:
            next_url = f"https://www.deviantart.com/_puppy/dashared/gallection/contents?username=dollmistress&type=gallery&offset={next_offset}&limit=24&all_folder=true&csrf_token=coqpp0Qy8ZBqUOWm.s8jlmm.0HhmNcG2KruMNYdSOxrUMRgewlTeemYivtHMEpGK6tM&da_minor_version=20230710"
            yield Request(next_url, headers=header, callback=self.parse)

