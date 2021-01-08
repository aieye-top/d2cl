
# compression

## 针对生成模型的协同进化压缩算法(ICCV2019)

在CycleGAN中的两个生成器网络将会被同时压缩：
$$
\begin{aligned}
\hat{G}_{1}, \hat{G}_{2} &=\arg \min _{G_{1}, G_{2}} \mathcal{N}\left(G_{1}\right)+\mathcal{N}\left(G_{2}\right) \\
&+\gamma\left(\mathcal{L}_{\text {DisA}}\left(G_{1}, D_{1}\right)+\lambda \mathcal{L}_{\text {cyc }}\left(G_{1}, G_{2}, X\right)\right) \\
\quad+& \gamma\left(\mathcal{L}_{\text {DisA }}\left(G_{2}, D_{2}\right)+\lambda \mathcal{L}_{\text {cyc }}\left(G_{2}, G_{1}, Y\right)\right)
\end{aligned}
$$


