#!/usr/bin/env python3

__author__ = 'Adam Marciniak'
__version__ = '0.1.0'
__license__ = 'MIT'

import gphoto2 as gp
import logging

class captureImage():
    def __init__(self):
        logging.basicConfig(filename='log_capture.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        self.camera  = gp.check_result(gp.gp_camera_new())
        self.context = gp.gp_context_new()
        try:
            gp.check_result(gp.gp_camera_init(self.camera, self.context))
        except gp.GPhoto2Error:
            logging.error("Camera cannot be reached. Probably off.")
            return

        # Set config to save to sd-card
        config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))
        capture_target = gp.check_result(gp.gp_widget_get_child_by_name(config, 'capturetarget'))
        count = gp.check_result(gp.gp_widget_count_choices(capture_target))
        value = gp.check_result(gp.gp_widget_get_choice(capture_target, 1))
        gp.check_result(gp.gp_widget_set_value(capture_target, value))
        gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))

    def capture(self, dir = "photos"):
        camera_file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE, self.context))
        camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, camera_file_path.folder, camera_file_path.name, gp.GP_FILE_TYPE_NORMAL, self.context))

        save_path = '/home/pi/photobox/{0}/{1}'.format(dir, camera_file_path.name)
        gp.gp_file_save(camera_file,save_path)
        gp.gp_camera_file_delete(self.camera, camera_file_path.folder, camera_file_path.name, self.context)

        del camera_file, camera_file_path

        return save_path

class captureImage_without_connection():
    def __init__(self):
        logging.basicConfig(filename='log_capture.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        #self.camera  = gp.check_result(gp.gp_camera_new())
        #self.context = gp.gp_context_new()
        try:
            gp.check_result(gp.gp_camera_init(self.camera, self.context))
        except gp.GPhoto2Error:
            logging.error("Camera cannot be reached. Probably off.")
            return

        # Set config to save to sd-card
        config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))
        capture_target = gp.check_result(gp.gp_widget_get_child_by_name(config, 'capturetarget'))
        count = gp.check_result(gp.gp_widget_count_choices(capture_target))
        value = gp.check_result(gp.gp_widget_get_choice(capture_target, 1))
        gp.check_result(gp.gp_widget_set_value(capture_target, value))
        gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))

    def capture(self, dir = "photos"):
        camera_file_path = gp.check_result(gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE, self.context))
        camera_file = gp.check_result(gp.gp_camera_file_get(self.camera, camera_file_path.folder, camera_file_path.name, gp.GP_FILE_TYPE_NORMAL, self.context))

        save_path = '/home/pi/photobox/{0}/{1}'.format(dir, camera_file_path.name)
        gp.gp_file_save(camera_file,save_path)
        gp.gp_camera_file_delete(self.camera, camera_file_path.folder, camera_file_path.name, self.context)

        del camera_file, camera_file_path

        return save_path

if __name__ == '__main__':
    u2i = captureImage()
    u2i.capture()