# Docker

容器作为一种新兴的虚拟化技术，跟传统的虚拟化方式相比具有众多的优势。其核心价值在于三点：[1]

- 敏捷性: 据业界统计，使用容器技术可以实现 3~10 倍的交付效率提升，大大加速新产品迭代的效率，并降低试错成本。
- 弹性: 通过容器技术可以充分发挥云的弹性，优化计算成本。一般情况下，通过容器技术可以降低 50% 的计算成本。
- 可移植性: 容器已经成为了应用分发和交付的标准，可以应用于底层运行环境的结构。实现一次构建处处部署。

用法：https://blog.csdn.net/weixin_40641725/article/details/105512106

全网最细 | 教你如何在 docker 容器下使用 mmdetection 训练自己的数据集 - 红色石头的文章 - 知乎
https://zhuanlan.zhihu.com/p/101263456

```bash
sudo nvidia-docker run -it -p [host_port]:[container_port](do not use 8888) --name:[container_name] [image_name] -v [container_path]:[host_path] /bin/bash
```
[2]

[1]: https://www.infoq.cn/article/lbF5cEOYhodd2roGPIT3
[2]: PyCharm+Docker：打造最舒适的深度学习炼丹炉 - 刘震的文章 - 知乎 https://zhuanlan.zhihu.com/p/52827335
