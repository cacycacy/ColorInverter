from os.path import splitext
from pathlib import Path
from numpy import round, uint8
from cv2 import imread, resize, imwrite, INTER_CUBIC, IMREAD_GRAYSCALE
# from pprint import pprint

# import matplotlib.pyplot as plt



file_type = ('png', 'jpg', 'jpeg')
try:
    print('導入資料', end="....")
    file_type = tuple(map(lambda x:'*.'+x if x[0] != '.' else '*'+x, file_type)) # 檢查副檔名"."號
    paths = []
    for _suff in file_type:
        for p in Path('.').glob(_suff):
            if not splitext(p)[0].endswith('_inverted'):
                paths.append(str(p))
    print(f"找到檔案,共{len(paths)}筆")
    print(paths, end="\n\n")
    need_resize = input('是否要放大圖片(y/n)? :')
    for path in paths:
        gray = imread(path, IMREAD_GRAYSCALE)
    #     imshow('img', img)
        img_shape = gray.shape  # 图像大小(h, w, 3)
        
        h = img_shape[0]
        w = img_shape[1]
        if need_resize.lower() == 'y':
            if h>w:
                fx = 2048/h
                gray = resize(gray, None, fx=fx, fy=fx, interpolation=INTER_CUBIC)
            else:
                fy = 2048/w
                gray = resize(gray, None, fx=fy, fy=fy, interpolation=INTER_CUBIC)
            print(f"處理圖片:{path}\t原始大小:{img_shape} 輸出大小:{gray.shape}")
        else:
            print(f"處理圖片:{path}")
        dst = gray.copy()
        
        # 線性轉換
        a = 2
        dst = dst * float(a)
        dst[dst > 255] = 255
        dst = round(dst)
        dst = dst.astype(uint8)
        dst = 255 - dst # 最大图像灰度值减去原图像，即可得到反转的图像
        (filename,extension) = splitext(path)
    #     plt.figure(figsize = (200,20))
    #     plt.imshow(np.hstack((gray, dst)), cmap='gray')
        imwrite(filename+'_inverted'+extension, dst)

    print('\ndone!')
    print("按任意鍵確認~~", end="")
    input()
except Exception as e:
    print(e)
    print('\n發生錯誤，請截圖並聯繫開發人員!')
    print("按任意鍵確認~~", end="")
    input()