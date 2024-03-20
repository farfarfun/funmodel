from typing import Generator

from funmodel.utils.capture import VideoCaptureQueue

from .base import PredictModel


class ImagePredictModel(PredictModel):
    def __init__(self, *args, **kwargs):
        super(ImagePredictModel, self).__init__(*args, **kwargs)

    def draw_image(self, image, result, *args, **kwargs):
        return image

    def predict(self, image, draw=False, *args, **kwargs):
        result = {}
        if draw:
            image = self.draw_image(image, result)
        return result, image

    def predict_capture(self, source=0, draw=True, *args, **kwargs) -> Generator:
        import cv2

        video_capture = VideoCaptureQueue(source)
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            response, image = self.predict(frame, draw=draw, *args, **kwargs)
            yield response, frame, image
