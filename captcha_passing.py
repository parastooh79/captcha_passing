import cv2
import numpy as np
import pytesseract
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import os


class CaptchaPassing:
    def save_image(self, img_url):
        image_url = img_url                # image link on site
        save_name = 'my_image.jpg'         # name of picture in my system
        urllib.request.urlretrieve(image_url, save_name)

    def delete_image(self,img_name):
        os.remove(img_name)    

    def get_captcha_image_link(self, page_url):
        res = requests.get(page_url)                 
        soup = BeautifulSoup(res.text, 'html.parser')
        val = soup.find_all('img',attrs={'example':'example'})         # find image url
        if len(val) == 0:
            print('ghadimie')
            raise Exception
            
        image_link = val[0]         # create right url of captcha picture
        return image_link

    def find_captcha_code(self, ads_link):
        image_url = self.get_captcha_image_link(ads_link)
        image = 'my_image.jpg'
        self.save_image(image_url)
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ekernel = np.ones((1,2),np.uint8)              # Taking a matrix of size (1,2) as the kernel
        eroded = cv2.erode(gray, ekernel, iterations = 1)
        """
        
          The first parameter is the original image, 
          kernel is the matrix with which image is convolved 
          and third parameter is the number of iterations, 
          which will determine how much you want to erode/dilate a given image.
          
        """
        
        dkernel = np.ones((2,3),np.uint8)
        dilated_once = cv2.dilate(eroded, dkernel, iterations = 1)
        ekernel = np.ones((2,2),np.uint8)
        dilated_twice = cv2.erode(dilated_once, ekernel, iterations = 1)
        th, threshed = cv2.threshold(dilated_twice, 200, 255, cv2.THRESH_BINARY)
        dkernel = np.ones((2,2),np.uint8)
        threshed_dilated = cv2.dilate(threshed, dkernel, iterations = 1)
        ekernel = np.ones((2,2),np.uint8)
        threshed_eroded = cv2.erode(threshed_dilated, ekernel, iterations = 1)
        text = pytesseract.image_to_string(threshed_eroded)
        image_code = ''.join(x for x in text if x.isdigit())

        self.delete_image(image)

        return image_code


CaptchaPassing().find_captcha_code('here is a sample url for test')
