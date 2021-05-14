import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import random
class ImageUtils:
    def imgRead(self, path):
        img = cv.imread(path)
        print(img.shape)
        return img

    def imgResize(self, img):
        width, height, channels = img.shape
        size = (int(width * 0.3), int(height * 0.5))
        imgOut = cv.resize(img, size, interpolation=cv.INTER_AREA)
        return imgOut

    def imgShow(self, img):
        # plt.imshow(img)
        # img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        cv.imshow('gakki', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def imgSave(self, imgNoise, imgFilter):
        cv.imwrite('./results/noise.jpg', imgNoise)
        cv.imwrite('./results/filterNoise.jpg', imgFilter)

    def addNoise(self, img, num):
        # sault noise
        for i in range(num):
            x = int(random.randrange(0,img.shape[0]))
            y = int(random.randrange(0,img.shape[1]))
            img[x,y,0] = 255
            img[x,y,1] = 255
            img[x,y,2] = 255
        return img


if __name__ == '__main__':
    imageUtils = ImageUtils()
    img = imageUtils.imgRead('./results/gakki.jpg')
    img = imageUtils.imgResize(img)
    print(img.shape)
    img2 = np.zeros_like(img)
    img2[:,:,0] = img[:,:,0]
    img2[:,:,1] = img[:,:,1]
    img2[:,:,2] = img[:,:,2]
    img2 = np.pad(img2, ((3,3), (3,3), (0,0)))
    img3 = imageUtils.addNoise(img, 3000)
    imageUtils.imgSave(img3, img2)
