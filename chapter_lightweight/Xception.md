Xception是Google提出的，arXiv 的V1 于2016年10月公开《Xception: Deep Learning with Depthwise Separable Convolutions 》，Xception是对Inception v3的另一种改进，主要是采用depthwise separable convolution来替换原来Inception v3中的卷积操作。

4.1设计思想
采用depthwise separable convolution来替换原来Inception v3中的卷积操作
与原版的Depth-wise convolution有两个不同之处：
第一个：原版Depth-wise convolution，先逐通道卷积，再11卷积; 而Xception是反过来，先1\1卷积，再逐通道卷积；
第二个：原版Depth-wise convolution的两个卷积之间是不带激活函数的，而Xception在经过1*1卷积之后会带上一个Relu的非线性激活函数；
4.2网络架构
feature map在空间和通道上具有一定的相关性，通过Inception模块和非线性激活函数实现通道之间的解耦。增多3*3的卷积的分支的数量，使它与1*1的卷积的输出通道数相等，此时每个3*3的卷积只作用与一个通道的特征图上，作者称之为“极致的Inception（Extream Inception）”模块，这就是Xception的基本模块。[1]


[1]: https://leesen998.github.io/2018/01/15/%E7%AC%AC%E5%8D%81%E4%B8%83%E7%AB%A0_%E6%A8%A1%E5%9E%8B%E5%8E%8B%E7%BC%A9%E3%80%81%E5%8A%A0%E9%80%9F%E5%8F%8A%E7%A7%BB%E5%8A%A8%E7%AB%AF%E9%83%A8%E7%BD%B2/
