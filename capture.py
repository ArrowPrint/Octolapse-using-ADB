# check device present: adb devices -> 5203d550fe3ea3ab
from time import clock, sleep
from subprocess import check_output, call
import re

import sys



#call this to capture image
def capture():
  clock()
  screen_on()
  clear_camera_folder()
  open_camera()
  press_camera_button()
  transfer_img()
  screen_off()
    
def screen_on():
  # check screen on/off state: adb shell dumpsys power | grep state --> Display Power: state=OFF\r\r or ON\r\r
  if DEBUG: print 'screen_on'.ljust(20), clock()
  r = check_output(['adb','shell','dumpsys','power'])
  try:
    state = re.search('Display Power: state=(.*)',r).group(1)
  except AttributeError:
    state = 'Unknown'

  ## DEBUG print 'state is',repr(state)
  # if OFF turn it on: adb shell input keyevent = POWER
  if state.strip() == 'OFF':
    r = check_output(['adb','shell','input','keyevent = POWER'])
    if DEBUG: print r.strip()
    r = check_output(['adb','shell','input','swipe','540','1600','540','100','1500'])

def open_camera():
  # check if camera is the top most: adb shell dumpsys activity activities | grep mFocusedActivity --> mFocusedActivity: ActivityRecord{f9da72a u0 com.sec.android.app.camera/.Camera t3967}
  if DEBUG: print 'open_camera'.ljust(20), clock()
  r = check_output(['adb','shell','dumpsys','activity','activities'])
  try:
    app = re.search('mFocusedActivity(.*)',r).group(1)
  except AttributeError:
    app = 'Unknown'
  
  # if not open camera app:adb shell am start -a android.media.action.STILL_IMAGE_CAPTURE
  if not 'com.sec.android.app.camera' in app:
    r = check_output(['adb','shell','am','start','-a','android.media.action.STILL_IMAGE_CAMERA'])
    if DEBUG: print r.strip()
  sleep(1)

def clear_camera_folder():
  #delete from phone: adb shell rm /sdcard/DCIM/Camera/*
  if DEBUG: print 'clear_camera_folder'.ljust(20), clock()
  r = check_output(['adb','shell','rm','/storage/emulated/0/DCIM/Camera/*'])
  if DEBUG: print r.strip()

def press_camera_button():
  #condition 1 screen on 2 camera open: adb shell input keyevent = CAMERA
  if DEBUG: print 'press_camera_button'.ljust(20), clock()
  r = check_output(['adb','shell','input','keyevent','KEYCODE_CAMERA'])
  if DEBUG: print r.strip()
  sleep(0.75)
  
def transfer_img():
  #looking for last file in DCIM/Camera: NO NEED cause we just have 1 picture (clear folder before capture)
  #copy to PC: adb pull /sdcard/DCIM/Camera/ c:/temp
  if DEBUG: print 'screen transfer_img'.ljust(20), clock()
  print(sys.argv[1])
  r = check_output(['adb','pull','/storage/emulated/0/DCIM/Camera/', str(sys.argv[1])])
  if DEBUG: print r.strip()

def screen_off():
  # assume it already on: adb shell input keyevent = POWER
  if DEBUG: print 'screen_off'.ljust(20), clock()
  r = check_output(['adb','shell','input','keyevent = POWER'])
  if DEBUG: print r.strip()






DEBUG = True
capture()

