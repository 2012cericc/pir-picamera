import time
import picamera
import gpiozero

# average out reading from motion sensor
def test_motion():
    motion_counter = 0
    
    for i in range(0, 100):
        if pir.motion_detected:
            motion_counter += 1
    if motion_counter > 20:
        return True
    else:
        return False

if __name__ == '__main__':
    camera = picamera.PiCamera()

    pir = gpiozero.MotionSensor(4)
    camera.resolution = (640, 480)
    camera.framerate = 24
    camera.rotation = 180
    camera.hflip = True
    
    time.sleep(2)
    index = 0 #filename index
    start_time = time.clock()

    recording = False

    while(index < 100):
        recording_time = time.clock() - start_time
        print("TIME %d" % recording_time)
        
        #start recording
        if test_motion() and recording == False:
            start_time = time.clock()

            prev_motion = True
            recording = True
            
            t = time.localtime()
            camera.annotate_text = time.asctime(t) #annotate video with start timestamp

            camera.start_recording('video%02d.h264' % index, format='h264', quality=30)
            index += 1
            
            camera.wait_recording(5)
            
        #stop recording if no motion or video is > 5mins
        elif recording and (not test_motion() or recording_time > 30):
            recording = False
            camera.stop_recording()



