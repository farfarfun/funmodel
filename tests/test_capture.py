import threading
from unittest.mock import MagicMock, patch

from funmodel.utils.capture import VideoCaptureQueue


def test_video_capture_queue_reads_latest_frame_and_terminates():
    capture = MagicMock()
    finished = threading.Event()
    responses = iter([(True, "first"), (True, "latest"), (False, None)])

    def read():
        response = next(responses)
        if not response[0]:
            finished.set()
        return response

    capture.read.side_effect = read

    with patch("cv2.VideoCapture", return_value=capture):
        queue = VideoCaptureQueue("video.mp4")
        assert finished.wait(timeout=1)
        assert queue.read() == (True, "latest")
        assert queue.read() == (False, None)
        queue.terminate()

    capture.release.assert_called_once_with()
