import numpy as np
from imageUtils import ImageUtils
from Filter import Filter
import copy
class SideWindowFiltering:
    def __init__(self, radius):
        self.radius = radius

    def genSideWindows(self, radius, start, end):
        arr_tmp = np.zeros((radius, radius))
        arr_tmp[start[0]:end[0],start[1]:end[1]] = 1
        # print(arr_tmp)
        return arr_tmp

    def process(self, img, iterator):
        result = copy.deepcopy(img)
        for i in range(iterator):
            print('process {}...'.format(i+1))
            for i in range(img.shape[2]):
                fs = np.zeros((8,img.shape[0], img.shape[1]), dtype=np.float)
                '''L,R,U,D,SW,SE,NW,NE'''
                fs[0,:,:] = filter_.boxFilterV2_sideWindow(img[:,:,i], (self.radius, 0), (self.radius, self.radius))
                fs[1,:,:] = filter_.boxFilterV2_sideWindow(img[:,:,i], (0, self.radius), (self.radius, self.radius))
                fs[2,:,:] = filter_.boxFilterV2_sideWindow(img[:,:,i], (self.radius, self.radius), (self.radius, 0))
                fs[3,:,:] = filter_.boxFilterV2_sideWindow(img[:,:,i], (self.radius, self.radius), (0, self.radius))
                fs[4,:,:] = filter_.boxFilterV2_sideWindow(img[:,:,i], (self.radius, 0), (0, self.radius))
                fs[5,:,:] = filter_.boxFilterV2_sideWindow(img[:,:,i], (0, self.radius), (0, self.radius))
                fs[6,:,:] = filter_.boxFilterV2_sideWindow(img[:,:,i], (self.radius, 0), (self.radius, 0))
                fs[7,:,:] = filter_.boxFilterV2_sideWindow(img[:,:,i], (0, self.radius), (self.radius, 0))
                # fs[0,:,:] = filter_.boxFilterV2(img[:,:,i], (self.radius, self.radius), (self.radius, self.radius), self.radius)
                result[:,:,i] = self.getMinCostRes(img[:,:,i], fs)

        return result

    def getMinCostRes(self, img, fs_ori):
        img_flattened = img.flatten()
        flattened = fs_ori.flatten()
        step = len(fs_ori[0].flatten())
        result_idx = []
        for i in range(step):
            result_idx.append(np.argmin(np.abs(flattened[i::step] - img_flattened[i])))
        min_idx = np.reshape(result_idx, fs_ori[0].shape)
        height, width = min_idx.shape
        for w in range(width):
            for h in range(height):
                choice = min_idx[h, w]
                img[h,w] = fs_ori[choice, h, w]

        return img






if __name__ == "__main__":
    swf = SideWindowFiltering(3)
    imgUtils = ImageUtils()
    filter_ = Filter()
    img = imgUtils.imgRead('/Users/leo/Desktop/SWF/results/noise.jpg')
    # img = imgUtils.imgResize(img)
    # imgNoise = imgUtils.addNoise(img, 3000)
    processImg = copy.deepcopy(img)
    fnl_img = swf.process(processImg, 10)
    # print(np.sum(np.abs(fnl_img - imgNoise)))
    print(fnl_img.shape)
    imgUtils.imgSave(img, fnl_img)
            

