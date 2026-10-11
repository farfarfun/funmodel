# funmodel

`funmodel` 是 farfarfun 组织下多媒体/AI 模型扩展包（`funmodel-dwpose`、`funmodel-mivolo` 等）的公共基础库，提供预测模型的统一基类（本地缓存目录管理、图像预测接口）以及图像编解码等工具函数，各扩展包通过 PEP 420 命名空间包机制挂载到 `funmodel` 下。

## 环境要求

- **Python `>=3.12`**。运行时依赖 `funget` 要求 `>=3.12`，因此本包的下限随之抬到
  3.12（组织统一下限为 3.10，见规范第 3 章对直接依赖 `funget` 仓库的说明）。
- 运行时依赖由 pip/uv 自动安装，无需手动处理：`tqdm>=4.60`、`opencv-python>=4.5`、
  `numpy>=1.23`、`funget>=1.1.63`。
- **`opencv-python` 需要系统提供原生图形库**。它的扩展模块链接了
  `libGL.so.1`、`libglib-2.0.so.0`、`libX11.so.6` 等，在精简容器或无图形界面的
  服务器上缺少这些库时，`import cv2` 会直接报
  `ImportError: libGL.so.1: cannot open shared object file`：

  ```bash
  # Debian / Ubuntu
  apt-get install -y libgl1 libglib2.0-0
  ```

  纯服务端场景也可以改装无 GUI 变体 `opencv-python-headless`（API 相同，不依赖上述原生库）。

- `VideoCaptureQueue` 与 `ImagePredictModel.predict_capture` 需要可访问的摄像头或视频文件；
  没有视频源的环境只能使用 `predict`。

## 安装

```bash
uv pip install funmodel
```

## 最小可运行示例

```python
import numpy as np

from funmodel.core.predict.image import ImagePredictModel

model = ImagePredictModel(model_name="demo")
print(model.cache_path)  # ~/.funmodel/demo

image = np.zeros((480, 640, 3), dtype=np.uint8)
result, image = model.predict(image=image)
```

## 包结构：PEP 420 命名空间包

`funmodel` 是**隐式命名空间包**，仓库里**刻意不放** `src/funmodel/__init__.py`。

原因：`funmodel`、`funmodel-dwpose`、`funmodel-mivolo` 是三个互不声明依赖关系的独立
发行版，却都要把文件装进同一个 `site-packages/funmodel/` 目录。如果它们各自再打包
一份真实的 `__init__.py`，磁盘上只会保留**最后安装**的那一份，而卸载其中任意一个包
都会按它自己的 RECORD 把这个共享文件删掉，导致其余包的 import 悬空。省掉
`__init__.py`、交给 PEP 420 处理是这个场景的标准做法（实测结论见
[farfarfun/todo-list#394](https://github.com/farfarfun/todo-list/issues/394)）。

扩展包挂载约定：

- PyPI 名为 `funmodel-<能力>`，源码目录为 `funmodel/<能力>/`，并在 `dependencies` 里声明 `funmodel`
- 扩展包**不要**创建 `funmodel/__init__.py`，只放自己的 `funmodel/<能力>/__init__.py`
- 共享命名空间根目录 `funmodel/` 下的文件（含 `py.typed`）只由 `funmodel` 本体提供，
  扩展包的 `py.typed` 应放在自己的子包目录里
- `funmodel2` 是独立的顶层包 `funmodel2`，既不依赖 `funmodel` 也不挂载到本命名空间下

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
