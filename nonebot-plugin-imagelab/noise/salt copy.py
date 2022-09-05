import cv2
import numpy as np
import matplotlib.pyplot as plt
def gasuss_noise(image, mean=0, var=0.001):

    image = np.array(image/255, dtype=float)#将原始图像的像素值进行归一化，除以255使得像素值在0-1之间
    noise = np.random.normal(mean, var ** 0.5, image.shape)#创建一个均值为mean，方差为var呈高斯分布的图像矩阵
    out = image + noise#将噪声和原始图像进行相加得到加噪后的图像
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)#clip函数将元素的大小限制在了low_clip和1之间了，小于的用low_clip代替，大于1的用1代替
    out = np.uint8(out*255)#解除归一化，乘以255将加噪后的图像的像素值恢复
    return out
def sp_noise(image,prob):
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = np.random.random()#随机生成0-1之间的数字
            if rdn < prob:#如果生成的随机数小于噪声比例则将该像素点添加黑点，即椒噪声
                output[i][j] = 0
            elif rdn > thres:#如果生成的随机数大于（1-噪声比例）则将该像素点添加白点，即盐噪声
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]#其他情况像素点不变
    return output
raw=cv2.imread("raw.jpg",0)
out = sp_noise(raw,0.03)
out = gasuss_noise(out)
cv2.imwrite('Salt+Gas.jpg',out)
cv2.imshow('out',out)
cv2.waitKey(0)