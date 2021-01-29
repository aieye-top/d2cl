
# Pretrain

## 标准模型算法资源库[3]

各大主流 AI 训练平台为了能吸引更多的开发者，不断推出和完善主流模型的直接调用能力，通常被称为 Model Zoo。

https://modelzoo.co/

https://github.com/PaddlePaddle/PaddleHub
https://github.com/PaddlePaddle/models

TensorFlow社区推出了一系列围绕 model 的项目，
https://tfhub.dev/
https://github.com/onnx/models

[TensorFlow hub](http://www.tensorflow.org/hub)为迁移学习(增量学习)提供前端模型支持、TensorFlow models 提供几十种常用模型 的官方支持和社区研究模型关注度非常高、TensorFlow Tensor2Tensor 提供从数据集到训练模型的全流程案例。PyTorch、MXNet、Keras、 Gluon、TensorLayer 各层次的平台也都从不同程度的提供主流模型算 法的直接支持，使得开发者可以快速的使用。


import torch
torch.hub.list('pytorch/vision')


https://github.com/chsasank/pytorch-hub-model-zoo


import torch
from torchvision.models import mobilenet_v2

model = mobilenet_v2(pretrained=True)

model.eval()
input_tensor = torch.rand(1,3,224,224)

script_model = torch.jit.trace(model,input_tensor)
script_model.save("mobilenet-v2.pt")


AI Hub 就更进一步：它允许你共享整个机器学习的管道，而不仅仅是模型！不过，它仍然处于 alpha 测试状态，但它已经比三年前修改最新文件的随机存储库更好了，如果你能够明白我意思的话。[4]
https://aihub.cloud.google.com/



---



https://github.com/topics/pretrained-language-model
https://github.com/Separius/awesome-sentence-embedding
https://gitee.com/mindspore/mindspore/tree/master/model_zoo/research/cv/tinynet

https://nlp.gluon.ai/model_zoo/index.html

[2]: https://github.com/johnolafenwa/PytorchMobile/blob/master/convert.py
[3]: http://www.caict.ac.cn/kxyj/qwfb/bps/201810/P020181017317431141487.pdf
[4]: https://www.infoq.cn/article/iQl1Qjir3Kb*9cowQcKW?utm_source=related_read&utm_medium=article
