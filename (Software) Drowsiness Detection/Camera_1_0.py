from tkinter import *
import time
import cv2
from PIL import Image, ImageTk
import numpy as np
import dlib
from imutils import face_utils


class App:
    def __init__(self, video_source=0):

        self.video_source = video_source

        # Creating Window
        self.root = Tk()

        # status marking for current state for Detector
        self.sleep = 0
        self.drowsy = 0
        self.active = 0
        self.status = ""
        self.color = (0, 0, 0)

        # Non Sense Defining
        self.frame1 = 0
        self.frame2 = 0
        self.frame3 = 0
        self.canvas1 = 0
        self.canvas2 = 0

        self.camera_label = Label(self.root, text='')
        self.back_button = Button(self.root, text='')
        self.capture_button = Button(self.root, text='')
        self.camera_label = Label(self.root, text='')

        self.root.title('My App - Camera 1.0')
        self.root.iconbitmap('camera.ico')
        self.root.resizable(0, 0)
        self.root['bg'] = 'black'

        # Defining VideoOn class object
        self.vid = VideoOn(video_source)

        #  Defining Buttons
        self.camera_button = Button(self.root, text='Camera', width=30, height=2, font=5, bg='#606060',
                                    activebackground='#404040', command=self.camera_button_func)
        self.detector_button = Button(self.root, text='Detection', width=30, height=2, font=5, bg='#606060',
                                      activebackground='#404040', command=self.detector_button_func)
        self.edit_button = Button(self.root, text='Edit Image', width=30, height=2, font=5, bg='#606060',
                                  activebackground='#404040')
        self.exit_button = Button(self.root, text='Exit', width=30, height=2, font=5, bg='#606060',
                                  activebackground='#404040', command=self.root.quit)

        # Packing Buttons
        self.camera_button.pack(pady=(35, 15))
        self.detector_button.pack(pady=15)
        self.edit_button.pack(pady=15)
        self.exit_button.pack(pady=15)

        self.root.mainloop()

    def revive_home(self):
        # Clearing Window
        self.cleanup()
        self.camera_button = Button(self.root, text='Camera', width=30, height=2, font=5, bg='#606060',
                                    activebackground='#404040', command=self.camera_button_func)
        self.detector_button = Button(self.root, text='Detection', width=30, height=2, font=5, bg='#606060',
                                      activebackground='#404040', command=self.detector_button_func)
        self.edit_button = Button(self.root, text='Edit Image', width=30, height=2, font=5, bg='#606060',
                                  activebackground='#404040')
        self.exit_button = Button(self.root, text='Exit', width=30, height=2, font=5, bg='#606060',
                                  activebackground='#404040', command=self.root.quit)

        # Packing Buttons
        self.camera_button.pack(pady=(35, 15))
        self.detector_button.pack(pady=15)
        self.edit_button.pack(pady=15)
        self.exit_button.pack(pady=15)

    def camera_button_func(self):
        # Clearing Window
        self.cleanup()

        self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060', activebackground='#404040',
                                  command=self.revive_home)
        self.back_button.pack(anchor=NE, expand=True)
        self.camera_label = Label(self.root, text='Camera', bg='black', fg='white', font=17)
        self.camera_label.pack(fill='both', side='top')
        status1, self.frame1 = self.vid.get_frame()
        if status1:
            self.canvas1 = Canvas(self.root, width=self.vid.width, height=self.vid.height)
            self.canvas1.pack()
            self.capture_button = Button(self.root, text='Capture', width=30, bg='#606060', activebackground='#404040',
                                         command=self.capture)
            self.capture_button.pack(anchor=CENTER, expand=True)
            self.update_camera_screen()

    def capture(self):
        image_name = 'IMG-' + time.strftime('%H-%M-%S-%d-%m') + '.jpg'
        cv2.imwrite(image_name, cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB))

    def update_camera_screen(self):
        status2, self.frame1 = self.vid.get_frame()
        if status2:
            self.frame2 = ImageTk.PhotoImage(Image.fromarray(self.frame1))
            self.canvas1.create_image(0, 0, image=self.frame2, anchor=NW)

        self.root.after(15, self.update_camera_screen)

    def cleanup(self):
        # self.camera_button.pack_forget()
        # self.detector_button.pack_forget()
        # self.edit_button.pack_forget()
        # self.exit_button.pack_forget()
        # self.camera_label.pack_forget()
        # self.capture_button.pack_forget()
        # self.camera_label.pack_forget()
        widgets = self.root.pack_slaves()
        for widget in widgets:
            widget.destroy()

    def detector_button_func(self):
        # Clearing Window
        self.cleanup()
        self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060', activebackground='#404040',
                                  command=self.revive_home)
        self.back_button.pack(anchor=NE, expand=True)
        self.camera_label = Label(self.root, text='Detector', bg='black', fg='white', font=10)
        self.camera_label.pack(fill='both', side='top')
        status2, self.frame3 = self.vid.get_frame()
        if status2:
            self.canvas2 = Canvas(self.root, width=self.vid.width, height=self.vid.height)
            self.canvas2.pack()

        self.update_detector_screen()

    def blinked(self, a, b, c, d, e, f):
        up = np.linalg.norm(b-d) + np.linalg.norm(c-e)
        down = np.linalg.norm(a-f)
        ratio = up / (2.0 * down)

        # Checking if it is blinked
        if ratio > 0.22:
            return 2
        elif (ratio > 0.14) and (ratio <= 0.22):
            return 1
        else:
            return 0

    def update_detector_screen(self):

        status2, self.frame3 = self.vid.get_frame()
        gray = cv2.cvtColor(self.frame3, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            left_blink = self.blinked(landmarks[36], landmarks[37], landmarks[38], landmarks[41],
                                      landmarks[40], landmarks[39])
            right_blink = self.blinked(landmarks[42], landmarks[43], landmarks[44], landmarks[47],
                                       landmarks[46], landmarks[45])

            if (left_blink == 0) or (right_blink == 0):
                self.sleep += 1
                self.drowsy = 0
                self.active = 0
                if self.sleep > 6:
                    self.status = "SLEEPING !!!"
                    self.color = (255, 0, 0)

            elif (left_blink == 1) or (right_blink == 1):
                self.sleep = 0
                self.active = 0
                self.drowsy += 1
                if self.drowsy > 6:
                    self.status = "Drowsy !"
                    self.color = (0, 0, 255)

            else:
                self.drowsy = 0
                self.sleep = 0
                self.active += 1
                if self.active > 6:
                    self.status = "Active :)"
                    self.color = (0, 255, 0)

            cv2.putText(self.frame3, self.status, (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.color, 3)
            # cv2.rectangle(self.frame3, (x1, y1), (x2, y2), self.color, 2)
            # for n in range(0, 68):
            #    (x, y) = landmarks[n]
            #    cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

            self.frame3 = ImageTk.PhotoImage(Image.fromarray(self.frame3))
            self.canvas2.create_image(0, 0, image=self.frame3, anchor=NW)

        self.root.after(15, self.update_detector_screen)


class VideoOn:
    def __init__(self, video_source=0):
        self.video = cv2.VideoCapture(video_source)
        if not self.video.isOpened():
            raise ValueError('No Camera Found \n try using another Camera Source')
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.video.isOpened():
            status, frame = self.video.read()
            if status:
                return status, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return status, None

        else:
            return None

    def __del__(self):
        if self.video.isOpened():
            self.video.release()


if __name__ == '__main__':
    # Initializing the face detector and landmark detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    App()
