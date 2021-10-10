#!/usr/bin/env python3

__author__ = 'Adam Marciniak'
__version__ = '0.1.0'
__license__ = 'MIT'

import tkinter as tk
import gphoto2 as gp
#from upload2Insta import upload2Insta
from captureImage import captureImage
from tkinter.font import Font
import RPi.GPIO as GPIO
# except ModuleNotFoundError:
#     import _fake_GPIO as GPIO
from PIL import Image, ImageOps, ImageTk

class PhotoBox():

    CAPTURE_DELAY   = 4
    VIEW_TIME       = 6
    UPLOAD_SCREEN   = 6
    UPLOAD          = True
    AUTO_UPLOAD     = False
    HASHTAG         = "#lärmundliebe"
    SHARE_SCREEN_TIME = 3
    IMAGE_WIDTH     = 6000  #Check in Camera
    IMAGE_HEIGHT    = 3368  #Check in Camera
    
    
    def __init__(self):
        self.ci = captureImage()
        #self.u2i = upload2Insta()
        self.tk = tk.Tk()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.tk.title("PhotoBox by Adam Marciniak (Gerpo)")
        self.tk['background'] = "#232b2b"
        self.font = Font(family="Arial", size=72)
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.attributes("-fullscreen", True)
        self.fullScreenState = False
        self.activeTrigger = False
        self.image_factor = (self.IMAGE_WIDTH / self.IMAGE_HEIGHT)
        self.calculated_height = int(1280 / self.image_factor)
    
    def start(self):
        self.content = tk.Label(self.tk, text="Starting PhotoBox", bg="#232b2b", fg="#F1F1F1", font=self.font)
        self.content.pack(expand=1, fill=tk.BOTH)
        
       
        #self.button = tk.Button(self.tk, text="Click me", command=self._triggerCapture).pack()
        #self.button = tk.Button(self.tk, text="Upload me", command=self._uploadPicture).pack()

        self.reset()
        GPIO.add_event_detect(23, GPIO.RISING, callback=self._triggerCapture, bouncetime=300)
        #GPIO.add_event_detect(21, GPIO.RISING, callback=self._uploadPicture, bouncetime=300)

        self.tk.mainloop()

    def toggle_fullscreen(self, event=None):
        self.fullScreenState = not self.fullScreenState  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.fullScreenState)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullScreenState = False
        self.tk.attributes("-fullscreen", False)
        return "break"

    def reset(self):
        self._changeText("Hit the black Button! \n\n #lärmundliebe \n\n #coronaclosing")
        self.content['image'] = ""
        self.uploadable = False
        self.activeTrigger = False

    def _triggerCapture(self, channel=0):
        if not self.activeTrigger:
            self.activeTrigger = True
            self._countdown(self.CAPTURE_DELAY, self._takePicture)

    def _takePicture(self):
        try:
            path = self.ci.capture()
            print (path)
        except gp.GPhoto2Error:
            self._changeText("Ohh, an error occurred. \n\n Just try again later.")
            self.tk.after(1500, self.reset)
            return
        
    
        #print("fotogemacht")
        #time.sleep(1)
        image = Image.open(path)
        #print("fotogemacht")
        image = ImageOps.fit(image, size=(1280, self.calculated_height), centering=(0.5, 0.5))
        #für Bildgröße 6000x3368 (Faktor 1,7814) bei Raspi Auflösung 1280 x 1024
        #print("fotogemacht")
        self.image_source = ImageTk.PhotoImage(image)
        #print("fotogemacht")
        #self.croppedImagePath = path.replace('.JPG', '_cropped.JPG')
        #croppedImage.save(self.croppedImagePath)

        self.content['image'] = self.image_source
#         self.uploadable = True
        
#         if self.AUTO_UPLOAD and self.UPLOAD:
#             self._uploadPicture()
        #print("fotogemacht")
        #if self.UPLOAD:
        #    self.tk.after(self.VIEW_TIME * 1000, self._uploadScreen)
        #else:
        self.tk.after(self.VIEW_TIME * 1000, self.reset)

#     def _uploadScreen(self):
#         if self.uploadable and self.image_source is not None:
#             self._changeText("Want to share? \n\n Press the red button!")
#             self.content['image'] = ""
#             self.tk.after(self.UPLOAD_SCREEN * 1000, self.reset)

#     def _uploadPicture(self, channel=0):
#         if self.uploadable and self.image_source is not None:
#             self.uploadable = False
#             print('Uploaded')
#             self._photoShared()
#             self.u2i.upload(self.croppedImagePath, self.HASHTAG)
#         else:
#             print("Forbidden!!!")
            
#     def _photoShared(self):
#         self.content['image'] = ""
#         self._changeText("Search for \n\n #lärmundliebe \n\n on Instagram")
#         self.tk.after(self.SHARE_SCREEN_TIME * 1000, self.reset)

    def _changeText(self, textInput):
        self.content['text'] = textInput

    def _countdown(self, remaining = None, callback = lambda: True):
        if remaining is not None:
            self.remaining = remaining
        
        if remaining is not None:
            self.countdown_callback = callback

        if self.remaining <= 0:
            self.countdown_callback()
        else:
            self._changeText(str(self.remaining))
            self.remaining = self.remaining - 1
            self.tk.after(1000, self._countdown)

    def __del__(self):
        GPIO.remove_event_detect(23)
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        photoBox = PhotoBox()
        photoBox.start()
    except KeyboardInterrupt:
        print('Bye')
        GPIO.cleanup()
    #except RuntimeError:
    #    print('Bye')
    #    GPIO.cleanup()
