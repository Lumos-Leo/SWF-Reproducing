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

    def boxFilterV2(self, img, radius_w, radius_h, radius):
        height, width = img.shape
        buffer = np.zeros(width)
        sumCol = np.zeros(width)
        A = np.zeros(img.shape)
        tmpH = 0

        for h in range(height):
            # 初始边界处理
            if (h < radius):
                for w in range(width):
                    buffer[w] = np.sum(img[0:h+radius,w])
                tmpH = h+radius
            # 末尾边界处理
            elif (h >=height-radius+1):
                buffer = buffer - img[h-1,:]
                tmpH = height - h
            else:
            # 更新buffer
                endH = np.min((height-radius+1, h+radius-1))
                buffer = buffer - img[h-radius,:] + img[endH,:]
                tmpH = endH - h  + radius

            # 小于滑窗半径都是buffer相加
            for w in range(radius):
                if (w == 0):
                    sumCol[w] = np.sum(buffer[w:radius])
                    A[h][w] = sumCol[w]/((radius-w)*tmpH)
                else:
                    sumCol[w] = sumCol[w-1] + buffer[radius+w-1]
                    A[h][w] = sumCol[w]/((radius+w)*tmpH)
            # 中间部分有加有减
            for w in range(radius, width-radius+1):
                sumCol[w] = sumCol[w-1] + buffer[w+radius-1] - buffer[w-radius]
                A[h][w] = sumCol[w]/ ((radius*2-1)*(tmpH)) 

            # 后面边界部分全是buffer相减
            for w in range(width-radius+1, width):
                sumCol[w] = sumCol[w-1] - buffer[w-1]
                A[h][w] = sumCol[w]/((width - w)*tmpH)
        return A.astype("uint8")

    def boxFilterV2_sideWindow(self, img, radius_w, radius_h):
        height, width = img.shape
        buffer = np.zeros(width)
        sumCol = np.zeros(width)
        A = np.zeros(img.shape)
        tmpH = 0

        for h in range(height):
            # 计算radius "L"
            radiusH = abs(radius_h[0] + radius_h[1] + 1)
            radiusW = abs(radius_w[0] + radius_w[1] + 1)
            startH = max(0, h-radius_h[0])
            endH = min(height, h+radius_h[1])
            tmpH = endH - startH + 1
            # 初始边界处理
            if (h == 0):
                if (abs(startH - endH) < 1e-7):
                    buffer[:] = img[startH, :]
                    tmpH = 1
                else:
                    buffer[:] = np.sum(img[startH:endH+1, :], axis=0)
                    
            # 末尾边界处理
            elif (h >= height - radius_h[1]):
                buffer = buffer - img[startH-1, :]
            # 中间过程处理
            else:
                if (startH == 0):
                    buffer = buffer + img[endH, :]
                else:
                    buffer = buffer + img[endH, :] - img[startH-1, :]
 
            for w in range(width):
                startW = max(0, w-radius_w[0])
                if (radius_w[1] == 0):
                    endW = min(width, w+radius_w[1])
                else:
                    endW = min(width, w+radius_w[1])
                # 小于滑窗半径都是buffer相加
                if (w == 0):
                    if (abs(startW - endW) < 1e-7):
                        sumCol[w] = np.sum(buffer[startW])
                        A[h][w] = sumCol[w]/(tmpH)
                    else:
                        sumCol[w] = np.sum(buffer[startW:endW+1])
                        A[h][w] = sumCol[w]/(tmpH*(endW-startW+1))
                # 后面边界部分全是buffer相减
                elif (w >= width - radius_w[1]):
                    sumCol[w] = sumCol[w-1] - buffer[startW-1]
                    A[h][w] = sumCol[w]/(tmpH*(endW-startW+1))
                # 中间部分有加有减
                else:
                    if (startW == 0):
                        sumCol[w] = sumCol[w-1] + buffer[endW]
                        A[h][w] = sumCol[w]/(tmpH*(endW-startW+1))
                    else:
                        sumCol[w] = sumCol[w-1] + buffer[endW] - buffer[startW-1]
                        A[h][w] = sumCol[w]/(tmpH*(endW-startW+1))
        return A.astype("uint8")

            




            
