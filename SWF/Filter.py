import numpy as np
class Filter:
    def meanFiltering(self, img, fs):
        res = {}
        for key,value in fs.items():
            res[key] = np.sum(img * value) // np.sum(value)

        return res

    def boxFilter(self, img, radius_w, radius_h):
        width, height = img.shape
        res = np.zeros_like(img)
        for i in range(height):
            for j in range(width):
                tmp_sum = 0
                start_h = max(0, i-radius_h[0])
                end_h = min(height, i+radius_h[1])
                start_w = max(0, j-radius_w[0])
                end_w = min(width, j+radius_w[1])
                for ji in range(start_h, end_h):
                    for jj in range(start_w, end_w):
                        tmp_sum += img[jj, ji]
                res[j,i] = tmp_sum
        return res

    def boxFilterModify(self, img, radius_w, radius_h):
        height, width = img.shape
        res = np.zeros_like(img, dtype=np.float)
        res_row = np.zeros_like(img, dtype=np.float)
        for i in range(height):
            for j in range(width):
                tmp_sum = 0
                start_w = max(0, j-radius_w[0])
                end_w = min(width-1, j+radius_w[1]) 
                if (end_w - start_w) < 1e-7:
                    res_row[i, j] = img[i, start_w]
                    continue
                for ww in range(start_w, end_w+1):
                    tmp_sum += img[i,ww]
                res_row[i, j] = tmp_sum//(end_w - start_w + 1)
        for i in range(height):
            for j in range(width):
                tmp_sum = 0
                start_h = max(0, i-radius_h[0])
                end_h = min(height, i+radius_h[1])
                for hh in range(start_h, end_h):
                    tmp_sum += res_row[hh,j]
                if (end_h - start_h) < 1e-7:
                    res[i, j] = tmp_sum
                    continue
                res[i, j] = tmp_sum // (end_h - start_h)
        return res

            
