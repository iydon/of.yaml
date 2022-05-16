<!-- Template from https://github.com/othneildrew/Best-README-Template -->
#



<!-- PROJECT SHIELDS -->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GPL-3.0 License][license-shield]][license-url] -->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/iydon/of.yaml">
    🟢⬜🟩⬜🟩<br />
    ⬜⬜⬜⬜⬜<br />
    🟩⬜🟩⬜🟩<br />
    ⬜⬜⬜⬜⬜<br />
    🟩⬜🟩⬜🟩<br />
  </a>

  <h3 align="center">OpenFOAM.YAML</h3>

  <p align="center">
    OpenFOAM 的 Python 接口（采用 YAML 配置）
    <br />
    <a href="https://github.com/iydon/of.yaml"><strong>探索文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/iydon/of.yaml">查看演示</a>
    ·
    <a href="https://github.com/iydon/of.yaml/issues">报告错误</a>
    ·
    <a href="https://github.com/iydon/of.yaml/issues">寻求功能</a>
  </p>
</div>



<!-- ABOUT THE PROJECT -->
## 关于项目

本项目最初是为了解决 OpenFOAM 案例文件结构复杂的问题[^1]，我的解决方案是采用通用[^2]配置文件格式来重新描述案例。在比较了市面上现有的通用配置文件格式后，我最终选择了 YAML[^3]，同时 Python 是我最熟悉的编程语言之一，OpenFOAM、YAML 与 Python 的结合便有了本项目。

本项目目前不能自动识别 OpenFOAM 案例，必须首先手动或半手动[^4]将 OpenFOAM 案例转化为等价的 YAML 格式。为了弥补无法自动转化案例的遗憾，本项目已经预先手动转化了部分官方教程案例与优秀第三方教程到 YAML 格式。在转化完 YAML 格式后，便可借助本项目：

- 获取 OpenFOAM 与算例的各类信息；
- 方便地修改案例参数，批量运行案例；
- 直观地感受案例运行的进度信息[^5]；
- 对案例运行结果进行部分后处理[^6]。

而且，由于案例可以通过 YAML 格式反复生成，解决了之前部分文件需要加 `.orig` 后缀防止覆盖、部分 `Allclean` 脚本复杂等问题。

最后，希望通过本项目可以将 OpenFOAM 与 Python 生态相结合，激发 OpenFOAM 的生命力与创造力。



<!-- CONTRIBUTING -->
<!-- 不会翻译，暂且留白，说实话我也不熟悉 〈（_　_）〉 -->



<!-- LICENSE -->
## 许可证

在 GPL-3.0 许可下发布。许可证相关的更多信息请见 `LICENSE.txt`。



<!-- CONTACT -->
## 联系我

梁钰栋 - [@iydon](https://github.com/iydon) - liangiydon_AT_gmail.com



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/iydon/of.yaml.svg?style=for-the-badge
[contributors-url]: https://github.com/iydon/of.yaml/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/iydon/of.yaml.svg?style=for-the-badge
[forks-url]: https://github.com/iydon/of.yaml/network/members
[stars-shield]: https://img.shields.io/github/stars/iydon/of.yaml.svg?style=for-the-badge
[stars-url]: https://github.com/iydon/of.yaml/stargazers
[issues-shield]: https://img.shields.io/github/issues/iydon/of.yaml.svg?style=for-the-badge
[issues-url]: https://github.com/iydon/of.yaml/issues
[license-shield]: https://img.shields.io/github/license/iydon/of.yaml.svg?style=for-the-badge
[license-url]: https://github.com/iydon/of.yaml/blob/master/LICENSE.txt

[^1]: OpenFOAM 的 wmake 命令同样存在类似的问题，相关统计结果请见 `script/wmake.py` 脚本
[^2]: 通用是指与编程语言无关，最好是主流编程语言均有工具可以解析该配置文件格式
[^3]: YAML 手写起来较为简洁，但是理论上只要能转化为对应的数据结构，什么配置文件格式均可
[^4]: 半手动可以借助 `script/case2yaml.py` 脚本，目前暂无对该脚本的升级计划
[^5]: 按理来说进度监控会对性能产生影响，但是在一分钟以内简单串行案例的初步比较下，应用本项目运行案例的平均时间要低于应用 `Allrun` 脚本运行案例的平均时间，平均时间减少约 6.4%。期待后续添加更多具体、完善的基准测试到 `script/bench.py` 脚本中
[^6]: 后处理部分采用 [VTK](https://github.com/Kitware/VTK) 开源格式，可以轻松获取网格上的信息，可操作空间大但可能需要自己造轮子
