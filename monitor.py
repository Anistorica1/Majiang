import cv2
import numpy as np
from mss import mss

sct = mss()

print(sct.monitors[0]['height'])