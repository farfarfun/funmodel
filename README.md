# funmodel

`funmodel` 是 farfarfun 组织下多媒体/AI 模型系列包（`funmodel-dwpose`、`funmodel-mivolo`、`funmodel2` 等）的公共基础库，提供预测模型的统一基类（本地缓存目录管理、图像预测接口）以及图像编解码等工具函数，各扩展包通过 PEP 420 命名空间包机制挂载到 `funmodel` 下。

## 安装

需要 Python 3.12 或更高版本。安装命令会同时安装 `numpy`、`opencv-python` 和
`funget` 等运行时依赖：

```bash
uv pip install funmodel
```

在 Linux 的精简或无桌面环境中，如 OpenCV 导入时提示缺少共享库，请安装发行版提供的
OpenGL/GLib 运行时库（例如 Debian/Ubuntu 的 `libgl1` 和 `libglib2.0-0`）。

## 最小可运行示例

```python
import numpy as np

from funmodel.core.predict.image import ImagePredictModel

model = ImagePredictModel(model_name="demo")
print(model.cache_path)  # ~/.funmodel/demo

image = np.zeros((480, 640, 3), dtype=np.uint8)
result, image = model.predict(image=image)
```

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
