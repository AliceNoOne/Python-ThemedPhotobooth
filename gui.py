import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
import numpy as np
#self.window.attributes("-fullscreen", True)


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
        self.window.configure(background='black')
        
        #self.window.geometry('1280x720')
        self.window.attributes("-fullscreen", True)
        self.window.update()
        self.twoThirds = self.window.winfo_width()-self.window.winfo_width()/3
        self.window.grid_columnconfigure(0, minsize=self.twoThirds)
        
        #span Cols
        self.camCanvas = tkinter.Canvas(self.window, width = 1280, height = 720)
        self.camCanvas.grid(rowspan=3, sticky=tkinter.NW)

        self.cols = 4

        self.photo = self.imgTest()

        for x in range(1,3):
            for y in range(self.cols):
                self.gridTest(x,y)

        self.btn = tkinter.Button(self.window, text="SayCheese",width=30,height=2)
        self.btn.grid(column=0, row=2, rowspan=2)

        self.chromaArray = np.array([[0,0,120], [110,230,255]])

        self.adjustChromaKey()
        self.delay = 1
        self.update()

        self.window.mainloop()

    def imgTest(self):
        cv_img = cv2.cvtColor(cv2.imread("yes.jpg"), cv2.COLOR_BGR2RGB)
        cv_img = cv2.resize(cv_img, ((int)(self.window.winfo_width()/6),(int)(self.window.winfo_height()/4)))
        #self.cv_img = self.cv_img[412:612,412:612]
        self.height, self.width, no_channels = cv_img.shape

        photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
        
        return photo 

    def gridTest(self, colNum, rowNum):
        self.canvas = tkinter.Canvas(self.window, width=self.width, height=self.height)      
        self.canvas.create_image(0,0,image=self.photo, anchor=tkinter.NW)
        self.canvas.grid(column=colNum, row=rowNum, sticky=tkinter.W)

    def backgroundImageSetup(self):
        chromaImg = cv2.cvtColor(cv2.imread("yes.jpg"), cv2.COLOR_BGR2RGB)
        dim = (int(self.vid.width), int(self.vid.height))
        chromaImg = cv2.resize(chromaImg, dim, interpolation=cv2.INTER_AREA)
        return chromaImg


    def chromaKey(self, frame):
        #lowerGreen = np.array([0,0,100])
        #upperGreen = np.array([120,100,255])

        for x in range(2):
            for y in range(3):
                self.chromaArray[x][y] = self.Offset[x][y].get()

        #blrframe = cv2.blur(frame, (6,6))
        blrframe = cv2.GaussianBlur(frame, (3,3), 0, 0)
        self.mask = cv2.inRange(blrframe, self.chromaArray[0], self.chromaArray[1])
        frame[self.mask != 0] = [0, 0, 0]

        img = self.backgroundImageSetup()
        img[self.mask == 0] = [0, 0, 0]

        finalImg = frame + img

        return finalImg

    def adjustChromaKey(self):
        self.sliderWindow = tkinter.Tk()
        self.sliderWindow.title("ChromaKey Offset")
        self.sliderWindow.protocol('WM_DELETE_WINDOW', self.offsetExit)

        rgbHighFrame = tkinter.Frame(self.sliderWindow)
        rgbHighFrame.pack(anchor=tkinter.SW)
        rgbLowFrame = tkinter.Frame(self.sliderWindow)
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
            self.camPhoto = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.camCanvas.create_image(0, 0, image = self.camPhoto, anchor = tkinter.NW)
            self.window.after(self.delay, self.update)

    def offsetExit(self):
        self.sliderWindow.destroy()
        self.window.destroy()




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
    App(tkinter.Tk(), "Halloween Photo")