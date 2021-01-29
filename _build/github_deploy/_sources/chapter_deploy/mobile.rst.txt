
mobile
======

https://mp.weixin.qq.com/s/bndECrtEcNCkCF5EG0wO-A

移动端机器学习资源合集

Embedded and mobile frameworks are less fully featured than full
PyTorch/Tensorflow Have to be careful with architecture Interchange
format Embedded and mobile devices have little memory and
slow/expensivecompute Have to reduce network size /quantize weights
/distill knowledge

Embedded and mobile devices have low-processor with little memory, which
makes the process slow and expensive to compute. Often, we can try some
tricks such as reducing network size, quantizing the weights, and
distilling knowledge. Both pruning and quantization are model
compression techniques that make the model physically smaller to save
disk space and make the model require less memory during computation to
run faster. Knowledge distillation is a compression technique in which a
small “student” model is trained to reproduce the behavior of a large
“teacher” model. Embedded and mobile PyTorch/TensorFlow frameworks are
less fully featured than the full PyTorch/TensorFlow frameworks.
Therefore, we have to be careful with the model architecture. An
alternative option is using the interchange format. Mobile machine
learning frameworks are regularly in flux: Tensorflow Lite, PyTorch
Mobile, CoreML, MLKit, FritzAI. The best solution in the industry for
embedded devices is NVIDIA. The Open Neural Network Exchange (ONNX for
short) is designed to allow framework interoperability.[2]

Deploy

Take the compressed flite file and load itinto a mobile or embedded
device

云端AI迁移到端侧A的四大理由:[3]

1. 隐私和安全:当用户的数据禁止传出获取的地方时,如欧美隐私保护严格
2. 时延:当用户需要实时反馈时,比如机器人或自动驾驶车
3. 可靠性:与云端互联的网络可能不稳定、甚至断线
4. 能耗:频繁发送数据到云端耗费昂贵,占用频段资源

online
方式：移动端做初步预处理，把数据传到服务器执行深度学习模型，优点是这个方式部署相对简单，将现成的框架(Caffe，Theano，MXNet，Torch)
做下封装就可以直接拿来用，服务器性能大,
能够处理比较大的模型，缺点是必须联网。

offline 方式：在服务器上进行训练的过程，在手机上进行预测的过程。

当前移动端的三大框架（Caffe2、TensorFlow Lite、Core ML）均使用 offline
方式，该方式可在无需网络连接的情况下确保用户数据的私密性。

14.9 现有的移动端开源框架及其特点 440[5] NCNN 440 QNNPACK 441
Prestissimo 443 MDL 445 Paddle-Mobile 446 MACE 446 FeatherCNN 448
TensorFlow Lite 449 PocketFlow 450 MDL、NCNN和TFLite对比 452
移动端开源框架部署 453

在手机上部署深度学习模型也可以归在此列，只不过硬件没得选，用户用什么手机你就得部署在什么手机上23333。为老旧手机部署才是最为头疼的[6]

[1]: [2]:
https://course.fullstackdeeplearning.com/course-content/testing-and-deployment/hardware-mobile
[3]:
https://www.bilibili.com/video/BV1Yt4y197Sd?from=search&seid=16685409903707063286
[4]:
https://furui@phei.com.cn/module/goods/wssd_content.jsp?bookid=57454
[5]:
https://www.jiqizhixin.com/graph/technologies/d484e2f3-bfd1-47c8-a430-db148416b574
[6]: https://zhuanlan.zhihu.com/p/292816755
