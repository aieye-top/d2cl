
ShuffleNet
==========

网络是Megvii
Inc. (Face++)提出。，晚于MobileNet两个月在arXiv上公开ShuffleNet pursues
the best accuracy in very limited computational budgets at tens or
hundreds of MFLOPs

ShuffleNet基于MobileNet的group思想，将卷积操作限制到特定的输入通道。而与之不同的是，ShuffleNet将输入的group进行打散，从而保证每个卷积核的感受野能够分散到不同group的输入中，增加了模型的学习能力。[12]

In ARM device, ShuffleNet achieves 13× actual speedup over AlexNet
while maintaining comparable accuracy.[6] 2018 CVPR : 300 citations.

Experiments on ImageNet classification and MS COCO object detection
demonstrate the superior performance of ShuffleNet over other
structures, e.g. lower top-1 error (absolute 7.8%) than recent MobileNet
on ImageNet classification task, under the computation budget of 40
MFLOPs.[2]

CNN 分组卷积 ResNet

分组点卷积 通道重排 shufflenet v2 pytorch复现

动机
----

数百层和数千通道，Billions of FLOPs

方法
----

属于直接训练而不是压缩

分组点卷积Group convolutions\`
------------------------------

给点卷积也分组

分组点卷积某个通道的输出仅来及一部分输入通道，阻止了信息流动，特征表示。

Group convolutions are used in AlexNet and ResNeXt. (a): There is no
channel shuffle, each output channel only relates to the input channels
within the group. This property blocks information flow between channel
groups and weakens representation. (b): If we allow group convolution to
obtain input data from different groups, the input and output channels
will be fully related. (c): The operations in (b) can be efficiently and
elegantly implemented by a channel shuffle operation. Suppose a
convolutional layer with g groups whose output has g×n channels; we
first reshape the output channel dimension into (g, n), transposing and
then flattening it back as the input of next layer. And channel shuffle
is also differentiable, which means it can be embedded into network
structures for end-to-end training.[6]

Group conv与DW conv存在相同的“信息流通不畅”问题[13]

通道重排(channel shuffle)
-------------------------

如果我们允许组卷积从不同组中获取输入数据，则输入和输出通道讲完全相关。

对于从上一个组层生成的特征图，可以先将每一个组中的通道划分为几个子组，
然后在下一层中的每个组中使用不同的子组作为输入。

ShuffleNet中的Channel
Shuffle操作可以将组间的信息进行交换，并且可以实现端到端的训练。

Group
convolution。其中输入特征通道被为G组(图4)，并且对于每个分组的信道独立地执行卷积，则分组卷积计算量是HWNK²M/G，为标准卷积计算量的1/G。
Channel shuffle。Grouped
Convlution导致模型的信息流限制在各个group内，组与组之间没有信息交换，这会影响模型的表示能力。因此，需要引入group之间信息交换的机制，即Channel
Shuffle操作。

引入的问题：[5]

channel shuffle在工程实现占用大量内存和指针跳转，这部分很耗时。 channel
shuffle的规则是人工设计，分组之间信息交流存在随意性，没有理论指导。

The motivation of ShuffleNet is the fact that conv1x1 is the bottleneck
of separable conv as mentioned above. While conv1x1 is already efficient
and there seems to be no room for improvement, grouped conv1x1 can be
used for this purpose!

The above figure illustrates the module for ShuffleNet. The important
building block here is the channel shuffle layer which “shuffles” the
order of the channels among groups in grouped convolution. Without
channel shuffle, the outputs of grouped convolutions are never exploited
among groups, resulting in the degradation of accuracy.[7]

采用concat替换add操作
---------------------

avg pooling和DW conv(s=2)会减小feature
map的分辨率，采用concat增加通道数从而弥补分辨率减小而带来信息的损失

FLOPS
-----

|FLOPs| (img:raw-latex:`\Shuffle`\_Flops.jp)

.. |FLOPs| image:: #flops

.. code:: py

   import torch
   import torch.nn as nn
   import torch.nn.functional as F


   class ShuffleBlock(nn.Module):
       def __init__(self, groups):
           super(ShuffleBlock, self).__init__()
           self.groups = groups

       def forward(self, x):
           '''Channel shuffle: [N,C,H,W] -> [N,g,C/g,H,W] -> [N,C/g,g,H,w] -> [N,C,H,W]'''
           N,C,H,W = x.size()
           g = self.groups
           return x.view(N,g,C//g,H,W).permute(0,2,1,3,4).reshape(N,C,H,W)

   class Bottleneck(nn.Module):
       def __init__(self, in_planes, out_planes, stride, groups):
           super(Bottleneck, self).__init__()
           self.stride = stride

           mid_planes = out_planes/4
           g = 1 if in_planes==24 else groups
           self.conv1 = nn.Conv2d(in_planes, mid_planes, kernel_size=1, groups=g, bias=False)
           self.bn1 = nn.BatchNorm2d(mid_planes)
           self.shuffle1 = ShuffleBlock(groups=g)
           self.conv2 = nn.Conv2d(mid_planes, mid_planes, kernel_size=3, stride=stride, padding=1, groups=mid_planes, bias=False)
           self.bn2 = nn.BatchNorm2d(mid_planes)
           self.conv3 = nn.Conv2d(mid_planes, out_planes, kernel_size=1, groups=groups, bias=False)
           self.bn3 = nn.BatchNorm2d(out_planes)

           self.shortcut = nn.Sequential()
           if stride == 2:
               self.shortcut = nn.Sequential(nn.AvgPool2d(3, stride=2, padding=1))

       def forward(self, x):
           out = F.relu(self.bn1(self.conv1(x)))
           out = self.shuffle1(out)
           out = F.relu(self.bn2(self.conv2(out)))
           out = self.bn3(self.conv3(out))
           res = self.shortcut(x)
           out = F.relu(torch.cat([out,res], 1)) if self.stride==2 else F.relu(out+res)
           return out

   def ShuffleNetG2():
       cfg = {
           'out_planes': [200,400,800],
           'num_blocks': [4,8,4],
           'groups': 2
       }
       return ShuffleNet(cfg)

   def ShuffleNetG3():
       cfg = {
           'out_planes': [240,480,960],
           'num_blocks': [4,8,4],
           'groups': 3
       }
       return ShuffleNet(cfg)


   def test():
       net = ShuffleNetG2()
       x = torch.randn(1,3,32,32)
       y = net(x)
       print(y)

-  The proposed network is mainly composed of a stack of ShuffleNet
   units grouped into three stages.
-  The number of bottleneck channels is set to 1/4 of the output
   channels for each ShuffleNet unit.
-  A scale factor s is applied on the number of channels. The networks
   in the above table is denoted as “ShuffleNet 1×”, then ”ShuffleNet
   s×” means scaling the number of filters in ShuffleNet 1× by s times
   thus overall complexity will be roughly s² times of ShuffleNet 1×.

ShuffleNet和ResNet结构可知，ShuffleNet计算量降低主要是通过分组卷积实现。ShuffleNet虽然降低了计算量，但是引入两个新的问题：\ `4 <https://zhuanlan.zhihu.com/p/45496826>`__

1、channel shuffle在工程实现占用大量内存和指针跳转，这部分很耗时。
2、channel
shuffle的规则是人工设计，分组之间信息交流存在随意性，没有理论指导。

ShuffleNet-V2\ `8 <https://github.com/megvii-model/ShuffleNet-Series>`__
------------------------------------------------------------------------

《ShuffleNet V2: Practical Guidelines for Ecient CNN Architecture
Design》

影响神经网络速度的4个因素：

1. FLOPs(FLOPs就是网络执行了多少multiply-adds操作)
2. 影响速度的不仅仅是FLOPs，还有内存访问成本（Memory Access cost, MAC）
   ;
3. 模型的并行（并行度高的模型速度相对更快。）
4. 计算平台(GPU，ARM)

因此作者结合理论与实践得到了四条实用的设计原则。

1. 输入输出的channel相同时，最小化内存访问成本（MAC）一一使用1
   :math:`\times 1` 卷积平衡输入和输出的通道大小
2. 过量使用分组卷积会增加MAC一一分组卷积要谨慎实用, 注意分组数
3. 网络碎片化会降低并行度, 一些网络如inception等倾向于采用“多路”结构,
   既存在一个block中有很多不同 的小卷积或pooling，这容易造成网络碎片化,
   降低并行度。一文避免网络碎片化
4. 不能忽略元素级别的操作，例如ReLU和Add等操作，这些操作虽然FLOPs较小，但是MAC较大。——减少元素级运算

(a): the basic ShuffleNet-V1 unit; (b) the ShuffleNet-V1 unit for
spatial down sampling :math:`(2 \times) ;` (c) ShuffleNet-V2 basic unit;
(d) ShuffleNet-V2 unit for spatial down sampling ( :math:`2 \times` )

ShuffleNet-V2 相对与V1，引入了一种新的运算: channel
split。具体来说，在开始时先将输入特征图在通道
维度分成两个分支：通道数分别为 :math:`C^{\prime}` 和
:math:`C-C^{\prime},` 实际实现时 :math:`C^{\prime}=C / 2`
。左边分支做同等映射, 右边的 分支包含3个连续的卷积,
并且输入和输出通道相同，这符合准则1。而且两个1x1卷积不再是组卷积, 这符合
准则2，另外两个分支相当于已经分成两组。两个分支的输出不再是Add元素，而是concat在一起,
紧接着是 对两个分支concat结果进行channle shuffle,
以保证两个分支信息交流。其实concat和channel shuffle可以和
下一个模块单元的channel
split合成一个元素级运算，这符合准则4。整体网络结果如下表:

depthwise convolution 和 瓶颈结构增加了 MAC，用了太多的
group，跨层连接中的 element-wise Add 操作也是可以优化的点。所以在
shuffleNet V2 中增加了几种新特性。 所谓的 channel split
其实就是将通道数一分为2，化成两分支来代替原先的分组卷积结构（G2），并且每个分支中的卷积层都是保持输入输出通道数相同（G1），其中一个分支不采取任何操作减少基本单元数（G3），最后使用了
concat 代替原来的 elementy-wise add，并且后面不加 ReLU
直接（G4），再加入channle shuffle 来增加通道之间的信息交流。
对于下采样层，在这一层中对通道数进行翻倍。
在网络结构的最后，即平均值池化层前加入一层 1x1
的卷积层来进一步的混合特征。\ `11 <https://leesen998.github.io/2018/01/15/%E7%AC%AC%E5%8D%81%E4%B8%83%E7%AB%A0_%E6%A8%A1%E5%9E%8B%E5%8E%8B%E7%BC%A9%E3%80%81%E5%8A%A0%E9%80%9F%E5%8F%8A%E7%A7%BB%E5%8A%A8%E7%AB%AF%E9%83%A8%E7%BD%B2/>`__

Comparison with MobileNetV1\ `6 <https://towardsdatascience.com/review-shufflenet-v1-light-weight-model-image-classification-5b253dfe982f>`__
---------------------------------------------------------------------------------------------------------------------------------------------

-  ShuffleNet models are superior to MobileNetV1 for all the
   complexities.
-  Though ShuffleNet network is specially designed for small models (<
   150 MFLOPs), it is still better than MobileNetV1 for higher
   computation cost, e.g. 3.1% more accurate than MobileNetV1 at the
   cost of 500 MFLOPs.
-  The simple architecture design also makes it easy to equip ShuffeNets
   with the latest advances such as Squeeze-and-Excitation (SE) blocks.
   (Hope I can review SENet in the future.)
-  ShuffleNets with SE modules boosting the top-1 error of ShuffleNet 2×
   to 24.7%, but are usually 25 to 40% slower than the “raw” ShuffleNets
   on mobile devices, which implies that actual speedup evaluation is
   critical on low-cost architecture design.

ShuffleNet-v2具有高精度的原因
-----------------------------

-  由于高效，可以增加更多的channel，增加网络容量
-  采用split使得一部分特征直接与下面的block相连，特征复用(DenseNet)

它在移动端低功耗设备提出了一种更为高效的卷积模型结构，在大幅降低模型计算复杂度的同时仍然保持了较高的识别精度，并在多个性能指标上均显著超过了同类方法。\ `9 <http://os.aiiaorg.cn/open/article/1201782277957726210>`__
　　ShuffleNet Series涵盖以下6个模型： 　　（1） ShuffleNetV1:
ShuffleNet: An Extremely Efficient Convolutional Neural Network for
Mobile Devices 　　论文链接：https://arxiv.org/abs/1707.01083
　　解读链接：为移动 AI 而生——旷视最新成果 ShuffleNet 全面解读 　　（2）
ShuffleNetV2: ShuffleNet V2: Practical Guidelines for Efficient CNN
Architecture Design 　　论文链接：https://arxiv.org/abs/1807.11164
　　解读链接：ECCV 2018 \| 旷视提出新型轻量架构ShuffleNet
V2：从理论复杂度到实用设计准则 　　（3） ShuffleNetV2+: ShuffleNetV2
的增强版 　　（4） ShuffleNetV2.Large: ShuffleNetV2 的深化版 　　（5）
OneShot: Single Path One-Shot Neural Architecture Search with Uniform
Sampling 　　论文链接：https://arxiv.org/abs/1904.00420
　　解读链接：AutoML \| 旷视研究院提出One-Shot模型搜索框架的新变体
　　（6） DetNAS: DetNAS: Backbone Search for Object Detection
　　论文链接：https://arxiv.org/abs/1903.10979
