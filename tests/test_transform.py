import base64

import numpy as np

from funmodel.utils.image.transform import base64_to_cvimg, cvimg_to_base64


def test_cvimg_base64_roundtrip_shape_preserved():
    img = np.zeros((4, 4, 3), dtype=np.uint8)
    img[:, :, 0] = 255

    encoded = cvimg_to_base64(img)
    decoded = base64_to_cvimg(encoded)

    assert isinstance(encoded, bytes)
    assert decoded.shape[2] == 3


def test_base64_to_cvimg_accepts_str_and_bytes():
    img = np.zeros((2, 2, 3), dtype=np.uint8)
    encoded_bytes = cvimg_to_base64(img)
    encoded_str = encoded_bytes.decode("ascii")

    assert base64_to_cvimg(encoded_bytes).shape[2] == 3
    assert base64_to_cvimg(encoded_str).shape[2] == 3
    assert base64.b64decode(encoded_str) == base64.b64decode(encoded_bytes)
