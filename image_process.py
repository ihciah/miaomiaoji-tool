#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "ihciah"

import cv2

class ImageConverter:
    @staticmethod
    def pre_process(im, interpolation=cv2.INTER_AREA):
        fixed_width = 384
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) if len(im.shape) == 3 and im.shape[2] != 1 else im
        multi = float(fixed_width) / gray.shape[1]
        dim = (fixed_width, int(gray.shape[0] * multi))
        new_im = cv2.resize(gray, dim, interpolation=interpolation)
        return new_im

    @staticmethod
    def frombits(bits):
        chars = []
        for b in range(len(bits) / 8):
            byte = bits[b*8:(b+1)*8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)

    @staticmethod
    def im2bmp(im, interpolation=cv2.INTER_AREA):
        im = ImageConverter.pre_process(im, interpolation)
        retval, im_binary = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)
        ret = ''
        for h in range(im_binary.shape[0]):
            pixels = [im_binary[h, w] for w in range(im_binary.shape[1])]
            binary = map(lambda x: 1 if x == 0 else 0, pixels)
            ret += ImageConverter.frombits(binary)
        return ret

    @staticmethod
    def image2bmp(path, interpolation=cv2.INTER_AREA):
        return ImageConverter.im2bmp(cv2.imread(path), interpolation)

class TextConverter:
    @staticmethod
    def text2bmp(text, height=70, pos=(10, 50), font=cv2.FONT_HERSHEY_SIMPLEX, size=2, color=0, thick=2):
        import numpy as np
        blank_image = np.zeros((height, 384), np.uint8)
        blank_image.fill(255)
        img = cv2.putText(blank_image, text, pos, font, size, color, thick)
        return ImageConverter.im2bmp(img)

if __name__ == "__main__":
    cv2.imshow("test", TextConverter.text2bmp("Coding by"))
    cv2.waitKey(0)
