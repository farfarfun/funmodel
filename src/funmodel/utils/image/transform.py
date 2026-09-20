# coding:utf8

import base64
import urllib.request

import cv2
import numpy as np
import requests


def url_to_base64(url: str) -> bytes:
    """下载 URL 指向的图片并转换为 base64 编码字节串。"""
    return base64.b64encode(requests.get(url).content)


def url_to_cvimg(url: str) -> np.ndarray:
    """下载 URL 指向的图片并解码为 OpenCV 图像矩阵（BGR）。"""
    img = np.asarray(bytearray(urllib.request.urlopen(url).read()), dtype="uint8")
    return cv2.imdecode(img, cv2.IMREAD_COLOR)


def base64_to_cvimg(b64: str | bytes) -> np.ndarray:
    """将 base64 编码的图片数据解码为 OpenCV 图像矩阵。"""
    return cv2.imdecode(
        np.frombuffer(base64.b64decode(b64), np.uint8), cv2.COLOR_RGB2BGR
    )


def cvimg_to_base64(img: np.ndarray) -> bytes:
    """将 OpenCV 图像矩阵编码为 JPEG 后转换为 base64 编码字节串。"""
    return base64.b64encode(cv2.imencode(".jpg", img)[1])
