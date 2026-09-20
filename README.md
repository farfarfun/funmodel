# funmodel

`funmodel` 是 farfarfun 组织下多媒体/AI 模型系列包（`funmodel-dwpose`、`funmodel-mivolo`、`funmodel2` 等）的公共基础库，提供预测模型的统一基类（本地缓存目录管理、图像预测接口）以及图像编解码等工具函数，各扩展包通过 PEP 420 命名空间包机制挂载到 `funmodel` 下。

## 安装

```bash
uv pip install funmodel
```

## 最小可运行示例

```python
from funmodel.core.predict.image import ImagePredictModel

model = ImagePredictModel(model_name="demo")
print(model.cache_path)  # ~/.funmodel/demo

result, image = model.predict(image=None)
```

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
