# SWF-Reproducing
Side Window Filtering Reproducing of Python Version

## Results

* 入参
  * 滑窗半径：3
  * 滑窗类型：8类（'L','R','U','D','SE','SW','NE','NW'）
  * 迭代次数：10次
* filter类型：box filter
* samples
* 输入原始图像进行滤波结果

![original](/Users/leo/Desktop/SWF/results/original.jpg)

![filtering](/Users/leo/Desktop/SWF/results/filter.jpg)

* 输入椒盐噪声的滤波结果

![origial](/Users/leo/Desktop/SWF/results/noise.jpg)

![filteringNoise](/Users/leo/Desktop/SWF/results/filterNoise.jpg)

## Implement Details

* 读入bgr的图像，每个通道分开处理
  * 在对一个固定大小的滑窗进行加权求和时，有两种方式，一种是通过padding，pad像素与边缘像素值一致，类似于神经网络中的卷积方式进行；第二种是直接在每个像素上进行遍历计算，不需要padding。实现中利用的是后种方式。
* 对于每个像素点，只会属于相邻窗口间的其中一个窗口，比如对于L和R窗口来说，像素如果包含在L窗口中计算，在R窗口中，就不进行计算。
* 此处针对不同的滑窗类型，直接按照偏移量来确定，避免了为每一种滑窗类型都写一种方法的重复操作。

## Tips

* 如果将矩阵的type设置为uint8，在后面计算最小cost函数时，会出现错误结果，因为对于负数或超过255的值会溢出。
* plt和cv的排列不一致，cv读取出来时bgr，而plt时bgr展示。

## References

1. [Side Window Filtering C++实现](https://github.com/Ldpe2G/ArmNeonOptimization/tree/master/sideWindowBoxFilter)
2. [优化盒子滤波](https://zhuanlan.zhihu.com/p/64522357)
3. Yin, H., Gong, Y., & Qiu, G. (2019). Side window filtering. *Proceedings of the IEEE Computer Society Conference on Computer Vision and Pattern Recognition*, *2019*-*June*, 8750–8758. https://doi.org/10.1109/CVPR.2019.00896
