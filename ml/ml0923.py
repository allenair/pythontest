'''
Created on 2019年9月23日

@author: syp560
'''
import numpy as np
from ml.mnist import load_mnist
from PIL import Image


if __name__ == '__main__':
    (x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)
    img = x_train[0]
    label = t_train[0]
    print(label)  # 5
    
    print(img.shape)  # (784,)
    img = img.reshape(28, 28)  # 把图像的形状变为原来的尺寸
    print(img.shape)  # (28, 28)
    
    pil_img = Image.fromarray(np.uint8(img))
    pil_img.show()