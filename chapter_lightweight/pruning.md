# Pruning

基于移动端的图像风格迁移，人像渲染等应用有着广泛的需求，在智能相机、移动社交、虚拟穿戴等领域有着巨大的应用前景。

生成式模型由于其本身输出结果和优化目标的特点，模型往往需要较大的内存，运行这些模型需要较大的计算开销，一般只能在GPU平台上运行，不能直接将这些模型迁移到移动端上。

Co-Evolutionary Compression for Unpaired Image Translation[3]被ICCV 2019录用，该论文首次提出针对GAN中生成网络的剪枝算法

在图像迁移任务中，可以在保持迁移效果的情况下，网络参数量和计算量压缩四倍以上，实测推理时间压缩三倍以上。

## 生成模型参数冗余建模

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



[1]: https://github.com/huawei-noah/Pruning
[2]: https://www.zhihu.com/people/YunheWang/posts
[3]: https://arxiv.org/abs/1907.10804
