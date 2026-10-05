import queue
import threading


# 自定义无缓存读视频类
class VideoCaptureQueue:
    """始终读取最新帧的视频捕获队列。"""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """创建视频捕获队列并启动后台读取线程。

        Args:
            *args: 透传给 `cv2.VideoCapture` 的位置参数，常见为摄像头编号（int）
                或设备名称/视频文件路径（str）。
            **kwargs: 透传给 `cv2.VideoCapture` 的关键字参数。
        """
        import cv2

        # camera_id 可以是摄像头编号（int），也可以是设备名称或视频文件路径（str）
        self.cap = cv2.VideoCapture(*args, **kwargs)
        self.q = queue.Queue(maxsize=3)
        self.stop_threads = False  # 用于优雅地结束后台读取线程
        th = threading.Thread(target=self._reader)
        th.daemon = True  # 设置工作线程为后台运行
        th.start()

    # 实时读帧，只保存最后一帧
    def _reader(self):
        while not self.stop_threads:
            ret, frame = self.cap.read()
            if not ret:
                self.q.put((ret, frame))
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put((ret, frame))

    def read(self) -> tuple[bool, object]:
        """读取队列中的最新帧。"""
        return self.q.get()

    def terminate(self) -> None:
        """停止后台读取线程并释放视频设备。"""
        self.stop_threads = True
        self.cap.release()
