# 参数剪枝(Pruning)

参数剪枝是指在预训练好的大型模型基础上,设计对网络参数的评价准则,以此为根据删除“冗余”参数.根据剪枝粒度粗细,参数剪枝可分为非结构化剪枝和结构化剪枝.非结构化剪枝的粒度比较细,可以无限制去掉网络中期望比例的任何“冗余”参数,,但是会带来裁剪后网络结构不规整难以有效加速的问题.结构化剪枝的粒度比较粗,剪枝的最小单位是filter内参数的组合,通过对filter或者feature map设置评价因子,甚至可以删除整个filter或者某几个channel,使网络“变窄”,可以直接在现有软硬件上获得有效加速,但可能带来预测精度(accuracy)的下降,需要通过对模型微调(fine-tuning)恢复性能

## 非结构化剪枝

LeCun在上世纪80年代末提出的OBD (optimal brain damage) 算法[19]使用loss对参数求二阶导数判断参数重要程度.在此基础上,Hassibi等人不再限制于OBD算法[19]的对角假设,提出OBS(optimal brain surgeon)算法[20],除了将次重要权重值置0,还重新计算其他权重值来补偿激活值,压缩效果更好.与OBS算法[20]类似,Srinivas等人[21]提出删除全连接层稠密的连接,不依赖训练数据,大大减少计算复杂度.最近,Dong等人[22]020406080文献发表年份分布图文献[8]文献[9]文献[10]文献[11]文献[12]本文


## 权重剪枝[7]

神经网络的权重剪枝就是把网络趋近于0的权重直接裁剪成0，以达到稀疏性。权重剪枝，可以作为量化模型后进一步的优化，有了稀疏性，通过压缩后可以进一步减少参数存储量；有了稀疏性，运算时如果跳过权重为0的计算，又可以减少功耗。TensorFlow Lite框架对模型的移动端部署的核心优化就是量化和权重剪枝。

稀疏模型的优势在于易于可压缩，在推理过程中跳过权重为0的计算。剪枝通过压缩模型来实现。在牺牲微小精度的前提下，我们的模型有6倍的性能提升。剪枝这项技术，也在实际应用到语音应用中，如语音识别、文本转语音以及横跨各种视觉与翻译的模型中。
权重剪枝主要有两种方式

后剪枝：拿到一个模型直接对权重进行剪枝，不需要其他条件。

训练时剪枝：训练迭代时边剪枝，使网络在训练过程中权重逐渐趋于0，但是由于训练时权重动态调整，使得剪枝操作对网络精度的影响可以减少，所以训练时剪枝比后剪枝更加稳定。

TF官方提供了详尽的Keras剪枝教程和Python API文档，以及训练稀疏模型等高级用法的指导。此外，还有一个MNIST手写体图像识别的CNN模型剪枝代码，和IMDN情感分类的LSTM模型的剪枝代码也可以参考。










## 生成模型参数冗余建模

基于移动端的图像风格迁移，人像渲染等应用有着广泛的需求，在智能相机、移动社交、虚拟穿戴等领域有着巨大的应用前景。

生成式模型由于其本身输出结果和优化目标的特点，模型往往需要较大的内存，运行这些模型需要较大的计算开销，一般只能在GPU平台上运行，不能直接将这些模型迁移到移动端上。

Co-Evolutionary Compression for Unpaired Image Translation[3]被ICCV 2019录用，该论文首次提出针对GAN中生成网络的剪枝算法

在图像迁移任务中，可以在保持迁移效果的情况下，网络参数量和计算量压缩四倍以上，实测推理时间压缩三倍以上。

对生成模型来说，网络输出是高维的生成图像，很难直接从这些图像本身去量化评价压缩模型的好坏，借鉴传统的剪枝算法，可以直接最小化压缩生成模型前后的重建误差来获得压缩后的模型。可以定义为生成器感知误差，



对于两个图像域的互相转换，循环一致性误差的重要性也在多篇论文里得到证明，所以也是压缩生成器重要的优化方向。

$$
\mathcal{L}_{c y c}=\frac{1}{m} \sum_{i=1}^{m}\left\|G_{2}\left(\hat{G}_{1}\left(x_{i}\right)\right)-x_{i}\right\|_{2}^{2}
$$
所以总体来说, 压缩一个生成网络的目标函数如下：
$$
\hat{G}_{1}=\arg \min _{G_{1}} \mathcal{N}\left(G_{1}\right)+\gamma\left(\mathcal{L}_{\text {DisA}}+\lambda \mathcal{L}_{\text {cyc}}\right)
$$
其中 $\mathrm{N}(\cdot)_{\text {表示网络的参数量, }}, \gamma$ 用来平衡网络参数量和压缩模型的误差。


对于两个的图像域互相转换，两个生成器一般有相同的网络结构和参数量，如果只优化其中一个生成器会导致网络训练过程不稳定，所以提出同时优化两个生成器，这样也可以节省计算时间和资源。


$\begin{aligned} \hat{G}_{1}, \hat{G}_{2} &=\arg \min _{G_{1}, G_{2}} \mathcal{N}\left(G_{1}\right)+\mathcal{N}\left(G_{2}\right) \\ &+\gamma\left(\mathcal{L}_{\text {Dis } A}\left(G_{1}, D_{1}\right)+\lambda \mathcal{L}_{\text {cyc }}\left(G_{1}, G_{2}, X\right)\right) \\ \quad &+\gamma\left(\mathcal{L}_{\text {Dis } A}\left(G_{2}, D_{2}\right)+\lambda \mathcal{L}_{\text {cyc }}\left(G_{2}, G_{1}, Y\right)\right) \end{aligned}$

## 其他方法

Molchanov等人[53]将剪枝问题当作一个优化问题,从权重参数中选择一个最优组合使得loss的损失最小,认为剪枝后预测精度衰减小的参数是不重要的.Lin等人[54]工作的独特之处是能全局评估各个filter的重要度,动态地和迭代地剪枝,并且能重新调用之前迭代中错误剪枝的filter.Zhang等人[55]将剪枝问题视为具有组合约束条件的非凸优化问题,利用交替方向乘法器(ADMM)分解为两个子问题,可分别用SGD和解析法求解.Yang等人[16]相比[55]加入能耗作为约束条件,通过双线性回归函数进行建模

[1]: https://github.com/huawei-noah/Pruning
[2]: https://www.zhihu.com/people/YunheWang/posts
[3]: https://arxiv.org/abs/1907.10804
https://mp.weixin.qq.com/s/lc7IoOV6S2Uz5xi7cPQUqg
[5]: http://www.jos.org.cn/ch/reader/download_pdf_file.aspx?journal_id=jos&file_name=88D0BB702E5C1707DA216DE97314F1CF19E0198366EB5D137A9BF999F723A888FEB366E50279546F&open_type=self&file_no=6096
[6]: https://zhuanlan.zhihu.com/p/101544149
[7]: https://cloud.tencent.com/developer/article/1635983
