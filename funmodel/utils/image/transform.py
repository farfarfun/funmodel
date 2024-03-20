# coding:utf8

import base64
import urllib.request

import cv2
import numpy as np
import requests


def url_to_base64(url):
    return base64.b64encode(requests.get(url).content)


def url_to_cvimg(url):
    img = np.asarray(bytearray(urllib.request.urlopen(url).read()), dtype="uint8")
    return cv2.imdecode(img, cv2.IMREAD_COLOR)


def base64_to_cvimg(b64):
    return cv2.imdecode(
        np.frombuffer(base64.b64decode(b64), np.uint8), cv2.COLOR_RGB2BGR
    )


def cvimg_to_base64(img):
    return base64.b64encode(cv2.imencode(".jpg", img)[1])
