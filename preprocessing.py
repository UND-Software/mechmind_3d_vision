# import tifffile as tiff

# img_3d = tiff.imread('DepthMap.tiff')
# print(img_3d.shape)
# print(img_3d.dtype)


import cv2

# img_3d = cv2.imread('DepthMap.tiff', cv2.IMREAD_COLOR)
img_3d = cv2.imread('DepthMap.tiff', cv2.IMREAD_UNCHANGED)
# print(img_3d.shape)
cv2.imshow('3D camera', img_3d)
cv2.waitKey()