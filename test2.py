import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import numpy as np


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(self.window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

        self.adjustChromaKey()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()

        self.window.mainloop()

    def snapshot(self):
        #Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            frame = self.chromaKey(frame)
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y %H:%M:%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def chromaKey(self, frame):
        #lowerGreen = np.array([0,0,100])
        #upperGreen = np.array([120,100,255])
        Green = np.array([[0,0,120], [110,230,255]])

        for x in range(2):
            for y in range(3):
                Green[x][y] = self.Offset[x][y].get()

        #blrframe = cv2.blur(frame, (6,6))
        blrframe = cv2.GaussianBlur(frame, (3,3), 0, 0)
        self.mask = cv2.inRange(blrframe, Green[0], Green[1])
        frame[self.mask != 0] = [0, 0, 0]

        self.cv_img = cv2.cvtColor(cv2.imread("yes.jpg"), cv2.COLOR_BGR2RGB)
        #self.cv_img = self.cv_img[0:720,0:1280]
        dim = (int(self.vid.width), int(self.vid.height))
        self.cv_img = cv2.resize(self.cv_img, dim, interpolation=cv2.INTER_AREA)
        self.cv_img[self.mask == 0] = [0, 0, 0]

        finalImg = frame + self.cv_img

        return finalImg

    def adjustChromaKey(self):
        rgbHighFrame = tkinter.Frame()
        rgbHighFrame.pack(anchor=tkinter.SW)
        rgbLowFrame = tkinter.Frame()
        rgbLowFrame.pack(anchor=tkinter.SW)
        self.Offset = np.array([[0,1,2], [3,4,5]], dtype=tkinter.Scale)

        for x in range(2):
            for y in range(3):
                if (x == 0):
                    self.Offset[x][y] = tkinter.Scale(rgbLowFrame, from_=0, to_=255, orient=tkinter.HORIZONTAL)
                else:
                    self.Offset[x][y] = tkinter.Scale(rgbHighFrame, from_=0, to_=255, orient=tkinter.HORIZONTAL)
                self.Offset[x][y].pack(side=tkinter.LEFT)


    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            frame = self.chromaKey(frame)           
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source, cv2.CAP_V4L2)
        self.vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                frame = cv2.flip(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), flipCode=1)
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
if __name__ == "__main__":
    App(tkinter.Tk(), "Tkinter and OpenCV")