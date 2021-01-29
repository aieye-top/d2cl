
.. raw:: html

   <!--
    * @version:
    * @Author:  StevenJokess https://github.com/StevenJokess
    * @Date: 2020-10-16 20:56:49
    * @LastEditors:  StevenJokess https://github.com/StevenJokess
    * @LastEditTime: 2020-12-30 20:41:26
    * @Description:
    * @TODO::
    * @Reference:https://ai.deepshare.net/detail/v_5ee644a796c35_tAwVkVvK/3?from=p_5ee641d2e8471_5z8XYfL6&type=6
    * https://ai.deepshare.net/detail/v_5ee644d9ed5d3_17ThW2c9/3?from=p_5ee641d2e8471_5z8XYfL6&type=6
    * https://ai.deepshare.net/detail/v_5ee645075753a_qSt7UuAU/3?from=p_5ee641d2e8471_5z8XYfL6&type=6
    * [5]: https://paddleclas.readthedocs.io/zh_CN/latest/models/Mobile.html
    * [6]: https://github.com/shicai/MobileNet-Caffe
    * [7]: https://www.zhihu.com/question/58941804
   -->

MobileNet
=========

MobileNet可谓是轻量级网络中的Inception，经历了一代又一代的更新。成为了学习轻量级网络的必经之路。MobileNetV1怎么和Xception的网络block结构一样，都大量用到了深度可分离。2016年6月，谷歌提出了MobileNetV1，由于各种原因当时没有挂上arxiv，一直到2017年4月才提交。好巧不巧，谷歌的另一团队，同时提出了Xception。

该网络将传统的卷积操作替换深度可分离卷积，即Depthwise卷积和Pointwise卷积的组合，相比传统的卷积操作，该组合可以大大节省参数量和计算量。与此同时，MobileNetV1也可以用于目标检测、图像分割等其他视觉任务中。[5]

只有一句话，MobileNetV1就是把VGG中的标准卷积层换成深度可分离卷积就可以了。

MobileNet is a stack of the separable convolution modules which are
composed of depthwise conv and conv1x1 (pointwise conv). Image for post
The separable conv independently performs convolution in spatial and
channel domains. This factorization of convolution significantly reduces
the computational cost from HWNK²M to HWNK² (depthwise) + HWNM
(conv1x1), HWN(K² + M) in total. In general, M>>K² (e.g. K=3 and M ≥
32), the reduction rate is roughly 1/8–1/9. The important point here is
that the bottleneck of the computational cost is now conv1x1[8]

ResNet
------

Activation
----------

轻量化网络的客观需求
--------------------

小、速度

不同于其他网络只关注小容量，MobileNet不仅关注低延迟，也关注小容量。

本文方法
--------

根据应用需求与资源限制（延迟，大小） 优化延迟 深度可分离卷积
设置两个超参数：balance准确率与延迟

深度可分离卷积 Depthwise Separable convolutions[11]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MobileNet使用了一种称之为 Depthwise Separable
convolutions来替代原有的传统3D卷积，减少了卷积核的冗余表达。在计算量和参数数量明显下降之后，卷积网络可以应用在更多的移动端平台。

采用DW卷积在减少参数数量的同时提升运算速度。但是由于每个feature
map只被一个卷积核卷积，因此经过DW输出的feature
map不能只包含输入特征图的全部信息，而且特征之间的信息不能进行交流，导致“信息流通不畅”。
采用PW卷积实现通道特征信息交流，解决DW卷积导致“信息流通不畅”的问题。

结构
----

通过步长来降采样 (n+2p-f)/s + 1\* (n+2p-f)/s + 1 尺度维度变化

用stride=2的卷积替换pooling
直接在卷积时利用stride=2完成了下采样，从而节省了需要再去用pooling再去进行一次下采样的时间，可以提升运算速度。同时，因为pooling之前需要一个stride=1的
conv，而与stride=2 conv的计算量想比要高近4倍(个人理解)。

深度可分离卷积
--------------

深度卷积负责各个通道 点卷积1\ *1*\ M，每个卷积一个像素

深度可分离卷积 分为 深度卷积和 点卷积

MoblieNets瘦身[10]
------------------

宽度参数
~~~~~~~~

有时，嵌入式端需要更小、更快的网络模型,
而原先的MobileNet架构不能满足要求。MobileNet
中通过引入一个控制网络均匀变薄的宽度乘数器 :math:`\alpha`,
使得输入通道数从m变成 :math:`\alpha m`, 输出通道数 从n变换成
:math:`\alpha n` 。引入宽度乘数器后, Depthwise separable
convolution的计算成本为
:math:`D_{k} \cdot D_{k} \cdot \alpha M \cdot \beta D_{F} \cdot D_{F} \cdot D_{F}+\alpha M \cdot \alpha N \cdot D_{F} \cdot D_{F}, \alpha \in(0,1]_{\circ}`
当 :math:`\alpha=1` 时, 为基本的 MobileNet; :math:`\alpha<1`
为通道数缩减的MobileNet。由计算成本公式可以看出，宽度乘法器使参数
数量大约降低了 :math:`\alpha^{2}`, 降低了计算成本。

分辨率参数
~~~~~~~~~~

在引入宽度乘数器 :math:`\alpha` 的基础上,
MobileNet又引入了一个可以控制改变相应输入图像大小和相应
神经网络内部每一层大小的参数分辨率乘法器 :math:`\beta`,
使得输入图像和神经网络内部每一层分辨率变为 :math:`\beta \cdot D_{F}`
。引入宽度乘法器 :math:`\alpha` 和分辨率乘法器 :math:`\beta` 后,
Depthwise separable convolutions的计算 成本：
:math:`D_{k} \cdot D_{k} \cdot \alpha M \cdot \beta D_{F} \cdot \beta D_{F}+\alpha M \cdot \alpha N \cdot \beta D_{F} \cdot \beta D_{F}, \alpha \in(0,1], \beta \in(0,1]_{\circ}`
:math:`\alpha=1, \beta=1` 时, 为基本MobileNet; :math:`\beta<1` 时,
为缩减MobileNet。

分析
~~~~

引入宽度乘法器 :math:`\alpha` 和分辨率乘法器 :math:`\beta`
可以让MobileNet 参数量减少，但同时也会让准确率相对
于基准MobileNet在实时性上与精确度上有了下降。所以为了达到想要的效果,
选择一个合适大小 的宽度乘法器 :math:`\alpha` 和分辨率乘法器
:math:`\beta`, 寻求精度与参数大小之间的一个平衡。

TODO:https://ai.deepshare.net/detail/v_5ee645312d94a_eMNJ5Jws/3?from=p_5ee641d2e8471_5z8XYfL6&type=6

训练
~~~~

MobileNet中采用同步梯度与RMSprop共同作用来更新网络的梯度大小。MobilNet参数量较少，整个模型不是很复杂，不容易出现过拟合，所以在训练的时候不使用正则化与数据增强策略。其余训练策略与普通网络方式相同。

MobileNet通过使用depthwise separable
convolutions大幅降低了网络的参数量和乘加次数，适于部署于嵌入式端。当我们需要进行目标检测、人脸识别等任务时，需要用到卷积神经网络提取特征，可以将MobileNet替代原有网络中的特征提取网络，来降低网络参数量，提高实时性。

.. code:: py

   # [3]
   import torch.nn as nn
   import math


   def conv_bn(inp, oup, stride):
       return nn.Sequential(
           nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
           nn.BatchNorm2d(oup),
           nn.ReLU(inplace=True)
       )


   def conv_dw(inp, oup, stride):
       return nn.Sequential(
           nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
           nn.BatchNorm2d(inp),
           nn.ReLU(inplace=True),

           nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
           nn.BatchNorm2d(oup),
           nn.ReLU(inplace=True),
       )


   class MobileNet(nn.Module):
       def __init__(self, n_class,  profile='normal'):
           super(MobileNet, self).__init__()

           # original
           if profile == 'normal':
               in_planes = 32
               cfg = [64, (128, 2), 128, (256, 2), 256, (512, 2), 512, 512, 512, 512, 512, (1024, 2), 1024]
           # 0.5 AMC
           elif profile == '0.5flops':
               in_planes = 24
               cfg = [48, (96, 2), 80, (192, 2), 200, (328, 2), 352, 368, 360, 328, 400, (736, 2), 752]
           else:
               raise NotImplementedError

           self.conv1 = conv_bn(3, in_planes, stride=2)

           self.features = self._make_layers(in_planes, cfg, conv_dw)

           self.classifier = nn.Sequential(
               nn.Linear(cfg[-1], n_class),
           )

           self._initialize_weights()

       def forward(self, x):
           x = self.conv1(x)
           x = self.features(x)
           x = x.mean(3).mean(2)  # global average pooling

           x = self.classifier(x)
           return x

       def _make_layers(self, in_planes, cfg, layer):
           layers = []
           for x in cfg:
               out_planes = x if isinstance(x, int) else x[0]
               stride = 1 if isinstance(x, int) else x[1]
               layers.append(layer(in_planes, out_planes, stride))
               in_planes = out_planes
           return nn.Sequential(*layers)

       def _initialize_weights(self):
           for m in self.modules():
               if isinstance(m, nn.Conv2d):
                   n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                   m.weight.data.normal_(0, math.sqrt(2. / n))
                   if m.bias is not None:
                       m.bias.data.zero_()
               elif isinstance(m, nn.BatchNorm2d):
                   m.weight.data.fill_(1)
                   m.bias.data.zero_()
               elif isinstance(m, nn.Linear):
                   n = m.weight.size(1)
                   m.weight.data.normal_(0, 0.01)
                   m.bias.data.zero_()

.. code:: py

   [4]
   import torch.nn as nn
   import math


   def conv_bn(inp, oup, stride):
       return nn.Sequential(
           nn.Conv2d(inp, oup, 3, stride, 1, bias=False),
           nn.BatchNorm2d(oup),
           nn.ReLU6(inplace=True)
       )


   def conv_1x1_bn(inp, oup):
       return nn.Sequential(
           nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
           nn.BatchNorm2d(oup),
           nn.ReLU6(inplace=True)
       )


   class InvertedResidual(nn.Module):
       def __init__(self, inp, oup, stride, expand_ratio):
           super(InvertedResidual, self).__init__()
           self.stride = stride
           assert stride in [1, 2]

           hidden_dim = round(inp * expand_ratio)
           self.use_res_connect = self.stride == 1 and inp == oup

           if expand_ratio == 1:
               self.conv = nn.Sequential(
                   # dw
                   nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
                   nn.BatchNorm2d(hidden_dim),
                   nn.ReLU6(inplace=True),
                   # pw-linear
                   nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False),
                   nn.BatchNorm2d(oup),
               )
           else:
               self.conv = nn.Sequential(
                   # pw
                   nn.Conv2d(inp, hidden_dim, 1, 1, 0, bias=False),
                   nn.BatchNorm2d(hidden_dim),
                   nn.ReLU6(inplace=True),
                   # dw
                   nn.Conv2d(hidden_dim, hidden_dim, 3, stride, 1, groups=hidden_dim, bias=False),
                   nn.BatchNorm2d(hidden_dim),
                   nn.ReLU6(inplace=True),
                   # pw-linear
                   nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False),
                   nn.BatchNorm2d(oup),
               )

       def forward(self, x):
           if self.use_res_connect:
               return x + self.conv(x)
           else:
               return self.conv(x)


   class MobileNetV2(nn.Module):
       def __init__(self, n_class=1000, input_size=224, width_mult=1.):
           super(MobileNetV2, self).__init__()
           block = InvertedResidual
           input_channel = 32
           last_channel = 1280
           interverted_residual_setting = [
               # t, c, n, s
               [1, 16, 1, 1],
               [6, 24, 2, 2],
               [6, 32, 3, 2],
               [6, 64, 4, 2],
               [6, 96, 3, 1],
               [6, 160, 3, 2],
               [6, 320, 1, 1],
           ]

           # building first layer
           assert input_size % 32 == 0
           input_channel = int(input_channel * width_mult)
           self.last_channel = int(last_channel * width_mult) if width_mult > 1.0 else last_channel
           self.features = [conv_bn(3, input_channel, 2)]
           # building inverted residual blocks
           for t, c, n, s in interverted_residual_setting:
               output_channel = int(c * width_mult)
               for i in range(n):
                   if i == 0:
                       self.features.append(block(input_channel, output_channel, s, expand_ratio=t))
                   else:
                       self.features.append(block(input_channel, output_channel, 1, expand_ratio=t))
                   input_channel = output_channel
           # building last several layers
           self.features.append(conv_1x1_bn(input_channel, self.last_channel))
           # make it nn.Sequential
           self.features = nn.Sequential(*self.features)

           # building classifier
           self.classifier = nn.Sequential(
               nn.Dropout(0.2),
               nn.Linear(self.last_channel, n_class),
           )

           self._initialize_weights()

       def forward(self, x):
           x = self.features(x)
           x = x.mean(3).mean(2)
           x = self.classifier(x)
           return x

       def _initialize_weights(self):
           for m in self.modules():
               if isinstance(m, nn.Conv2d):
                   n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                   m.weight.data.normal_(0, math.sqrt(2. / n))
                   if m.bias is not None:
                       m.bias.data.zero_()
               elif isinstance(m, nn.BatchNorm2d):
                   m.weight.data.fill_(1)
                   m.bias.data.zero_()
               elif isinstance(m, nn.Linear):
                   n = m.weight.size(1)
                   m.weight.data.normal_(0, 0.01)
                   m.bias.data.zero_()

.. code:: py

   #[5]
   import torch
   model = torch.hub.load('pytorch/vision:v0.6.0', 'mobilenet_v2', pretrained=True)
   model.eval()

TODO: (PROTOTYPE) CONVERT MOBILENETV2 TO NNAPI
https://pytorch.org/tutorials/prototype/nnapi_mobilenetv2.html

這邊把各個Block多用一層Sequential包起來是因為Network
Pruning的時候抓Layer比較方便。

import torchvision.models.quantization.mobilenet

MobileNetV1\ `6 <https://engineering.fb.com/2018/10/29/ml-applications/qnnpack/>`__
The first version of the MobileNet architecture pioneered the use of
depthwise convolutions to make a model more suitable for mobile devices.
MobileNetV1 consists almost entirely of 1×1 convolutions and depthwise
3×3 convolutions. We converted the quantized MobileNetV1 model from
TensorFlow Lite and benchmarked it on 32-bit ARM builds of TensorFlow
Lite and QNNPACK. With both runtimes using 4 threads, we observed 1.8x
geomean speedup of QNNPACK over the TensorFlow Lite runtime.

深度可分离卷积（Depthwise separable
convolution）代替标准的卷积，并使用宽度因子(width
multiply)减少参数量。深度可分离卷积把标准的卷积因式分解成一个深度卷积(depthwise
convolution)和一个逐点卷积(pointwise
convolution)。\ `7 <https://cygao.xyz/2019/07/12/lightweight/>`__

https://github.com/0809zheng/Hung-yi-Lee-ML2020-homework/blob/master/
hw7_Network_Compression/hw7_Architecture_Design.ipynb
