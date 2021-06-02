from tkinter import *
import time
import cv2
from PIL import Image, ImageTk
import numpy as np
import dlib
from imutils import face_utils
from tkinter import filedialog


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
        self.image_photo = 0

        self.camera_label = Label(self.root, text='')
        self.back_button = Button(self.root, text='')
        self.capture_button = Button(self.root, text='')
        self.camera_label = Label(self.root, text='')
        self.photo_label = Label(self.root, text='')
        self.edit_label = Label(self.root, text='')

        self.root.title('My App - Camera 1.3')
        self.root.iconbitmap('camera.ico')
        self.root.resizable(0, 0)
        self.root['bg'] = 'black'

        # Defining VideoOn class object
        #self.vid = VideoOn(video_source)

        #  Defining Buttons
        self.camera_button = Button(self.root, text='Camera', width=30, height=2, font=5, bg='#606060',
                                    activebackground='#404040', command=self.camera_button_func)
        self.detector_button = Button(self.root, text='Detection', width=30, height=2, font=5, bg='#606060',
                                      activebackground='#404040', command=self.detector_button_func)
        self.edit_button = Button(self.root, text='Edit Image', width=30, height=2, font=5, bg='#606060',
                                  activebackground='#404040', command=self.edit_window)
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

        self.vid.video.release()

        self.camera_button = Button(self.root, text='Camera', width=30, height=2, font=5, bg='#606060',
                                    activebackground='#404040', command=self.camera_button_func)
        self.detector_button = Button(self.root, text='Detection', width=30, height=2, font=5, bg='#606060',
                                      activebackground='#404040', command=self.detector_button_func)
        self.edit_button = Button(self.root, text='Edit Image', width=30, height=2, font=5, bg='#606060',
                                  activebackground='#404040', command=self.edit_window)
        self.exit_button = Button(self.root, text='Exit', width=30, height=2, font=5, bg='#606060',
                                  activebackground='#404040', command=self.root.quit)

        # Packing Buttons
        self.camera_button.pack(pady=(35, 15))
        self.detector_button.pack(pady=15)
        self.edit_button.pack(pady=15)
        self.exit_button.pack(pady=15)

    def revive_home_after_editing(self):
        # Clearing Window
        self.cleanup()

        #self.vid.video.release()

        self.camera_button = Button(self.root, text='Camera', width=30, height=2, font=5, bg='#606060',
                                    activebackground='#404040', command=self.camera_button_func)
        self.detector_button = Button(self.root, text='Detection', width=30, height=2, font=5, bg='#606060',
                                      activebackground='#404040', command=self.detector_button_func)
        self.edit_button = Button(self.root, text='Edit Image', width=30, height=2, font=5, bg='#606060',
                                  activebackground='#404040', command=self.edit_window)
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

        self.vid = VideoOn(self.video_source)
        time.sleep(15)

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

        self.vid = VideoOn(self.video_source)
        time.sleep(15)

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

    def edit_window(self):
        self.cleanup()
        self.root.filename = filedialog.askopenfilename(initialdir='D:/', title='Select a File...',
                                                        filetypes=(('jpg files', '*.jpg'), ('png files', '*.png*')))

        photo = cv2.imread(self.root.filename)
        #photo = cv2.cvtColor(photo, cv2.COLOR_BGR2RGB)
        self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060', activebackground='#404040',
                                  command=self.revive_home_after_editing)
        self.back_button.pack(anchor=NE, expand=True)

        self.editing_label = Label(self.root, text='Editing Window', bg='black', fg='white', font=17)
        self.editing_label.pack(fill='both', side='top')

        self.image_photo = ImageTk.PhotoImage(Image.open(self.root.filename).resize((630,500)))


        self.photo_label = Label(self.root, image=self.image_photo)
        self.photo_label.pack()
        tool_frame = LabelFrame(self.root, text='Editing Tools', bg='gray', bd=2)
        tool_frame.pack(fill="both", expand="yes", pady=(10, 5))

        def gray_func():
            self.cleanup()

            self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060',
                                      activebackground='#404040',
                                      command=self.revive_home_after_editing)
            self.back_button.pack(anchor=NE, expand=True)

            self.editing_label = Label(self.root, text='Gray Image', bg='black', fg='white', font=17)
            self.editing_label.pack(fill='both', side='top')

            gray_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
            print(type(gray_photo))
            #gray_photo_save = gray_photo
            self.photo_label.pack_forget()
            gray_photo = ImageTk.PhotoImage(Image.fromarray(gray_photo))
            self.photo_label = Label(self.root, image=gray_photo)
            self.photo_label.pack()

            def save():
                image_name = 'IMG-' + time.strftime('%H-%M-%S-%d-%m') + '.jpg'
                cv2.imwrite(image_name, gray_photo)
                #self.root.quit()

            save_button = Button(self.root, text='Save', width=30, command=save)
            save_button.pack()

        def bright_func():
            self.cleanup()

            self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060',
                                      activebackground='#404040',
                                      command=self.revive_home_after_editing)
            self.back_button.pack(anchor=NE, expand=True)

            self.editing_label = Label(self.root, text='Bright Image', bg='black', fg='white', font=17)
            self.editing_label.pack(fill='both', side='top')

            bright_photo = cv2.convertScaleAbs(photo, alpha=1, beta=100)
            #gray_photo_save = gray_photo
            self.photo_label.pack_forget()
            bright_photo = ImageTk.PhotoImage(Image.fromarray(bright_photo))
            self.photo_label = Label(self.root, image=bright_photo)
            self.photo_label.pack()

            def save():
                image_name = 'IMG-' + time.strftime('%H-%M-%S-%d-%m') + '.jpg'
                cv2.imwrite(image_name, bright_photo)
                #self.root.quit()

            save_button = Button(self.root, text='Save', width=30, command=save)
            save_button.pack()

        def pencil_sketch_func():
            self.cleanup()

            self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060',
                                      activebackground='#404040',
                                      command=self.revive_home_after_editing)
            self.back_button.pack(anchor=NE, expand=True)

            self.editing_label = Label(self.root, text='Sketch Image', bg='black', fg='white', font=17)
            self.editing_label.pack(fill='both', side='top')

            sketch_photo, colored_sketch_photo = cv2.pencilSketch(photo, 200, 0.1, shade_factor=0.1)
            #gray_photo_save = gray_photo
            self.photo_label.pack_forget()
            sketch_photo = ImageTk.PhotoImage(Image.fromarray(sketch_photo))
            self.photo_label = Label(self.root, image=sketch_photo)
            self.photo_label.pack()

            def save():
                image_name = 'IMG-' + time.strftime('%H-%M-%S-%d-%m') + '.jpg'
                cv2.imwrite(image_name, sketch_photo)
                #self.root.quit()

            save_button = Button(self.root, text='Save', width=30, command=save)
            save_button.pack()

        def color_sketch_func():
            self.cleanup()

            self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060',
                                      activebackground='#404040',
                                      command=self.revive_home_after_editing)
            self.back_button.pack(anchor=NE, expand=True)

            self.editing_label = Label(self.root, text='Sketch Image', bg='black', fg='white', font=17)
            self.editing_label.pack(fill='both', side='top')

            sketch_photo, colored_sketch_photo = cv2.pencilSketch(photo, 200, 0.1, shade_factor=0.1)
            # gray_photo_save = gray_photo
            self.photo_label.pack_forget()
            colored_sketch_photo = ImageTk.PhotoImage(Image.fromarray(colored_sketch_photo))
            self.photo_label = Label(self.root, image=colored_sketch_photo)
            self.photo_label.pack()

            def save():
                image_name = 'IMG-' + time.strftime('%H-%M-%S-%d-%m') + '.jpg'
                cv2.imwrite(image_name, colored_sketch_photo)
                # self.root.quit()

            save_button = Button(self.root, text='Save', width=30, command=save)
            save_button.pack()

        def sharp_func():
            self.cleanup()

            self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060',
                                      activebackground='#404040',
                                      command=self.revive_home_after_editing)
            self.back_button.pack(anchor=NE, expand=True)

            self.editing_label = Label(self.root, text='Sharp Image', bg='black', fg='white', font=17)
            self.editing_label.pack(fill='both', side='top')

            kernal = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]])

            sharp_photo = cv2.filter2D(photo, -1, kernal)
            #gray_photo_save = gray_photo
            self.photo_label.pack_forget()
            sharp_photo = ImageTk.PhotoImage(Image.fromarray(sharp_photo))
            self.photo_label = Label(self.root, image=sharp_photo)
            self.photo_label.pack()

            def save():
                image_name = 'IMG-' + time.strftime('%H-%M-%S-%d-%m') + '.jpg'
                cv2.imwrite(image_name, sharp_photo)
                #self.root.quit()

            save_button = Button(self.root, text='Save', width=30, command=save)
            save_button.pack()

        def contrast_func():
            self.cleanup()

            self.back_button = Button(self.root, text='Back', width=30, font=25, bg='#606060',
                                      activebackground='#404040',
                                      command=self.revive_home_after_editing)
            self.back_button.pack(anchor=NE, expand=True)

            self.editing_label = Label(self.root, text='Contrast Image', bg='black', fg='white', font=17)
            self.editing_label.pack(fill='both', side='top')

            contrast_photo = cv2.convertScaleAbs(photo, alpha=2.0, beta=30)
            #gray_photo_save = gray_photo
            self.photo_label.pack_forget()
            contrast_photo = ImageTk.PhotoImage(Image.fromarray(contrast_photo))
            self.photo_label = Label(self.root, image=contrast_photo)
            self.photo_label.pack()

            def save():
                image_name = 'IMG-' + time.strftime('%H-%M-%S-%d-%m') + '.jpg'
                cv2.imwrite(image_name, contrast_photo)
                #self.root.quit()

            save_button = Button(self.root, text='Save', width=30, command=save)
            save_button.pack()

        gray_button = Button(tool_frame, text='Gray', width=25, command=gray_func)
        gray_button.grid(row=0, column=0, padx=40, pady=3)

        bright_button = Button(tool_frame, text='Bright', width=25, command=bright_func)
        bright_button.grid(row=0, column=1, padx=40, pady=3)

        pencil_sketch_button = Button(tool_frame, text='Sketch', width=25, command=pencil_sketch_func)
        pencil_sketch_button.grid(row=0, column=2, padx=40, pady=3)

        color_sketch_button = Button(tool_frame, text='Saturation', width=25, command=color_sketch_func)
        color_sketch_button.grid(row=1, column=0, padx=40, pady=3)

        sharpness_button = Button(tool_frame, text='Sharpness', width=25, command=sharp_func)
        sharpness_button.grid(row=1, column=1, padx=40, pady=3)

        contrast_button = Button(tool_frame, text='Contrast', width=25, command=contrast_func)
        contrast_button.grid(row=1, column=2, padx=40, pady=3)

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
