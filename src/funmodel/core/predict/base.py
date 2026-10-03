import os
from pathlib import Path
from typing import Any


class PredictModel:
    """预测模型基类，负责管理模型的本地缓存目录。"""

    def __init__(
        self,
        model_name: str = "tmp",
        cache_dir: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """初始化预测模型。

        Args:
            model_name: 模型名称，用于生成缓存子目录。
            cache_dir: 模型缓存根目录，默认使用 `~/.funmodel/`。
        """
        self.model_name = model_name
        self.cache_dir = cache_dir or str(Path.home() / ".funmodel")
        os.makedirs(self.cache_path, exist_ok=True)

    @property
    def cache_path(self) -> str:
        """当前模型的缓存目录完整路径。"""
        return f"{self.cache_dir}/{self.model_name}"

    def load(self, *args: Any, **kwargs: Any) -> None:
        """加载模型权重，子类需覆盖实现。"""
        pass

    def predict(self, *args: Any, **kwargs: Any) -> Any:
        """执行预测，子类需覆盖实现。"""
        pass
