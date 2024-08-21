import cv2
import numpy as np

from mecheye.shared import *
from mecheye.area_scan_3d_camera import *
from mecheye.area_scan_3d_camera_utils import *
from mecheye.area_scan_3d_camera_utils import find_and_connect, print_camera_info, print_camera_status, print_camera_intrinsics

from .lib import *


class ConnectCameraAPI(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        # self.width = width
        # self.height = height

        self.camera = Camera()
        self.camera_info = CameraInfo()
        self.camera_status = CameraStatus()
        self.camera_intrinsics = CameraIntrinsics()

    # Mech-Mind 카메라 정보 출력
    def get_camera_info(self):
        show_error(self.camera.get_camera_info(self.camera_info))
        print_camera_info(self.camera_info)
        show_error(self.camera.get_camera_status(self.camera_status))
        print_camera_status(self.camera_status)

    # 카메라 왜곡, matrix (3D 카메라에서 2D 카메라의 고유 파라미터 설명)
    def get_camera_intrinsics(self):
        show_error(self.camera.get_camera_intrinsics(self.camera_intrinsics))
        print_camera_intrinsics(self.camera_intrinsics)

    # 카메라 연결
    def connect_to_camera(self):
        print("Camera testing...")
        error_status = self.camera.connect(self.ip, self.port)

        if not error_status.is_ok():
            show_error(error_status)
            return False
        print("Connected to the camera successfully.")
        return True
    
    # 카메라 연결 끊기
    def disconnect_to_camera(self):
        self.camera.disconnect()
        print("Disconnected from the camera successfully.")   

    # 2D image 캡처
    def capture_2d_image(self):
        frame_2d = Frame2D()
        show_error(self.camera.capture_2d(frame_2d))
        if frame_2d.color_type() == ColorTypeOf2DCamera_Monochrome:
            image2d = frame_2d.get_gray_scale_image()
        elif frame_2d.color_type() == ColorTypeOf2DCamera_Color:
            image2d = frame_2d.get_color_image()

        file_name = "2DImage.png"
        cv2.imwrite(file_name, image2d.data())

        img_h, img_w, img_c = image2d.data().shape
        print("2D image size: {} x {}".format(img_w, img_h))
        print("2D image size: {}".format(frame_2d.image_size()))
        print("Capture and save the 2D image: {}".format(file_name))

    # Depth Map 캡처
    def capture_depth_map(self):
        frame3d = Frame3D()
        show_error(self.camera.capture_3d(frame3d))
        depth_map = frame3d.get_depth_map()
        
        img = depth_map.data().astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = np.ascontiguousarray(img)
        cv2.imshow('3d test', img)
        cv2.waitKey()

        # depth_file = "DepthMap.tiff"
        # cv2.imwrite(depth_file, depth_map.data())
        # print(depth_map)
        # print("Capture and save the depth map: {}".format(depth_file))
        
        

    # def capture_depth_map_normal(self):
    #     frame3d = Frame3D()
    #     show_error(self.camera.capture_3d_with_normal(frame3d))
    #     depth_map = frame3d.get_depth_map()

    #     depth_file = "DepthMap_normal.tiff"
    #     cv2.imwrite(depth_file, depth_map.data())
    #     print("Capture and save the depth map: {}".format(depth_file))


    def main(self):
        if self.connect_to_camera():
            # a.get_camera_info()
            # a.capture_2d_image()
            a.capture_depth_map()
            a.disconnect_to_camera()

    
if __name__ == '__main__':
    a = ConnectCameraAPI(IP, PORT)
    a.main()
    
