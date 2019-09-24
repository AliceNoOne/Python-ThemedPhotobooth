import tkinter
import cv2
import math
import PIL.Image, PIL.ImageTk

class App:
    def __init__(self, window, window_title, image_path="yes.jpg"):
        self.window = window
        self.window.title(window_title)

        self.cv_img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        self.cv_img = self.cv_img[100:920,0:1280]
        self.height, self.width, no_channels = self.cv_img.shape

        self.canvas = tkinter.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.grid()

        self.rows = 4
        self.buttons = []

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0,image=self.photo, anchor=tkinter.NW)
        self.canvas.grid(rowspan=self.rows)

        #self.btn_blur=tkinter.Button(self.window, text="Blur", width=25, command=self.blur_image)
        #self.btn_blur.grid(row=0, column=1)

        self.cv_img2 = cv2.resize(self.cv_img, (200,math.floor(self.height/self.rows)), interpolation=cv2.INTER_AREA)
        self.photoCopy = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img2))
        for y in range(self.rows):
            for x in range(2,5):
                self.btn_blur=tkinter.Button(self.window, image=self.photoCopy, command= self.blur_image) #command=lambda: self.test(self.btn_blur))
                self.btn_blur.grid(row=y, column=x)
    
        self.window.mainloop()

    def blur_image(self):
        #self.cv_img = cv2.blur(self.cv_img, (3, 3))
        self.cv_img = cv2.GaussianBlur(self.cv_img, (5, 5), 0, 0)        
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.cv_img))
        self.canvas.create_image(0,0,image=self.photo, anchor=tkinter.NW)

    def test(self, a):
        a.configure(text="hi", image="")

App(tkinter.Tk(), "Tkinter and OpenCV")