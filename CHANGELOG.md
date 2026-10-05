# CHANGELOG

## [0.0.10] - 未发布

### 变更

- 源码迁移到 `src/funmodel/` 标准布局。
- 补齐 `opencv-python`/`numpy` 运行时依赖及版本下限。
- 为公开类和函数补充类型标注与中文 docstring。

### 新增

- README 补充简介、安装命令与最小可运行示例，并附组织统一介绍区块。
- `tests/` 补充覆盖 `PredictModel`/`ImagePredictModel` 公开 API 的用例。

### 修复

- 删除未被任何构建流程消费的残留版本文件 `script/__version__.md`（与 `pyproject.toml`
  长期不同步，版本唯一来源为 `pyproject.toml`）。
- `base64_to_cvimg` 误将 `cv2.COLOR_RGB2BGR`（颜色转换码，数值上恰好等于
  `cv2.IMREAD_ANYCOLOR`）当作 `cv2.imdecode` 的读取 flag 使用；灰度图输入会被解码为
  二维矩阵而非三通道矩阵，调用方按惯例访问 `shape[2]` 时抛 `IndexError`。已改为
  `cv2.IMREAD_COLOR`，与 `url_to_cvimg` 行为保持一致。
