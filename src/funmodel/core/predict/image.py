from typing import Any, Generator

import numpy as np

from funmodel.utils.capture import VideoCaptureQueue

from .base import PredictModel


class ImagePredictModel(PredictModel):
    """基于图像输入的预测模型基类。"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """初始化图像预测模型，参数透传给 `PredictModel`。"""
        super(ImagePredictModel, self).__init__(*args, **kwargs)

    def draw_image(self, image: np.ndarray, result: dict, *args: Any, **kwargs: Any) -> np.ndarray:
        """在图像上绘制预测结果，子类可覆盖实现。

        Args:
            image: 原始图像。
            result: 预测结果。

        Returns:
            绘制后的图像，默认原样返回。
        """
        return image

    def predict(
        self, image: np.ndarray, draw: bool = False, *args: Any, **kwargs: Any
    ) -> tuple[dict, np.ndarray]:
        """对单帧图像执行预测。

        Args:
            image: 输入图像。
            draw: 是否在图像上绘制预测结果。

        Returns:
            预测结果字典与（可能被绘制过的）图像。
        """
        result: dict = {}
        if draw:
            image = self.draw_image(image, result)
        return result, image

    def predict_capture(
        self, source: int | str = 0, draw: bool = True, *args: Any, **kwargs: Any
    ) -> Generator[tuple[dict, np.ndarray, np.ndarray], None, None]:
        """从视频源逐帧读取并预测。

        Args:
            source: 视频源，摄像头编号或视频文件路径。
            draw: 是否在图像上绘制预测结果。

        Yields:
            (预测结果, 原始帧, 处理后图像) 三元组。
        """
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
