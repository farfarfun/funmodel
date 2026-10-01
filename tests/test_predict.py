import os
import shutil
from unittest.mock import MagicMock, patch

import pytest

from funmodel.core.predict.base import PredictModel
from funmodel.core.predict.image import ImagePredictModel


@pytest.fixture
def tmp_cache_dir(tmp_path):
    yield str(tmp_path)
    shutil.rmtree(tmp_path, ignore_errors=True)


def test_predict_model_creates_cache_path(tmp_cache_dir):
    model = PredictModel(model_name="demo", cache_dir=tmp_cache_dir)
    assert model.cache_path == f"{tmp_cache_dir}/demo"
    assert os.path.isdir(model.cache_path)


def test_predict_model_default_load_and_predict_are_noop(tmp_cache_dir):
    model = PredictModel(model_name="demo", cache_dir=tmp_cache_dir)
    assert model.load() is None
    assert model.predict() is None


def test_image_predict_model_predict_without_draw(tmp_cache_dir):
    model = ImagePredictModel(model_name="demo", cache_dir=tmp_cache_dir)
    result, image = model.predict(image="fake-image", draw=False)
    assert result == {}
    assert image == "fake-image"


def test_image_predict_model_predict_with_draw_calls_draw_image(tmp_cache_dir):
    model = ImagePredictModel(model_name="demo", cache_dir=tmp_cache_dir)
    result, image = model.predict(image="fake-image", draw=True)
    assert result == {}
    # 默认 draw_image 原样返回图像
    assert image == "fake-image"


def test_predict_capture_yields_frames_and_releases_source(tmp_cache_dir):
    capture = MagicMock()
    capture.read.side_effect = [(True, "frame"), (False, None)]
    model = ImagePredictModel(model_name="demo", cache_dir=tmp_cache_dir)

    with (
        patch("funmodel.core.predict.image.VideoCaptureQueue", return_value=capture),
        patch("cv2.waitKey", return_value=-1),
    ):
        assert list(model.predict_capture("video.mp4", draw=False)) == [
            ({}, "frame", "frame")
        ]

    capture.terminate.assert_called_once_with()


def test_predict_capture_releases_source_when_consumer_stops(tmp_cache_dir):
    capture = MagicMock()
    capture.read.return_value = (True, "frame")
    model = ImagePredictModel(model_name="demo", cache_dir=tmp_cache_dir)

    with (
        patch("funmodel.core.predict.image.VideoCaptureQueue", return_value=capture),
        patch("cv2.waitKey", return_value=-1),
    ):
        frames = model.predict_capture()
        next(frames)
        frames.close()

    capture.terminate.assert_called_once_with()
