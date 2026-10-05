import base64
from unittest.mock import patch

import cv2
import numpy as np
import pytest

from funmodel.utils.image.transform import (
    base64_to_cvimg,
    cvimg_to_base64,
    url_to_base64,
    url_to_cvimg,
)


def _download_with(data: bytes, success: bool = True):
    def fake_download(url, path, overwrite):
        if success:
            path.write_bytes(data)
        return success

    return fake_download


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


def test_base64_to_cvimg_forces_three_channels_for_grayscale_source():
    # 回归用例：此前误用 cv2.COLOR_RGB2BGR（数值上等价于 cv2.IMREAD_ANYCOLOR）
    # 作为 imdecode 的 flag 参数，灰度图会被原样解码成二维矩阵，
    # 导致调用方按惯例访问 shape[2] 时抛 IndexError。
    gray = np.zeros((4, 4), dtype=np.uint8)
    encoded = base64.b64encode(cv2.imencode(".png", gray)[1].tobytes())

    decoded = base64_to_cvimg(encoded)

    assert decoded.shape == (4, 4, 3)


def test_url_to_base64_downloads_with_funget():
    data = b"image data"
    with patch(
        "funmodel.utils.image.transform.download", side_effect=_download_with(data)
    ) as download:
        assert url_to_base64("https://example.com/image.jpg") == base64.b64encode(data)

    download.assert_called_once()


def test_url_to_cvimg_decodes_downloaded_image():
    image = np.zeros((2, 3, 3), dtype=np.uint8)
    encoded = cv2.imencode(".png", image)[1].tobytes()
    with patch(
        "funmodel.utils.image.transform.download", side_effect=_download_with(encoded)
    ):
        decoded = url_to_cvimg("https://example.com/image.png")

    assert decoded.shape == image.shape


def test_url_conversion_raises_when_download_fails():
    with (
        patch(
            "funmodel.utils.image.transform.download",
            side_effect=_download_with(b"", success=False),
        ),
        pytest.raises(OSError, match="图片下载失败"),
    ):
        url_to_base64("https://example.com/missing.jpg")


def test_url_to_cvimg_returns_none_for_invalid_image_data():
    with patch(
        "funmodel.utils.image.transform.download",
        side_effect=_download_with(b"not an image"),
    ):
        assert url_to_cvimg("https://example.com/invalid.jpg") is None
