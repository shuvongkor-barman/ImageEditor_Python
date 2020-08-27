from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import cv2

root = Tk()
root.geometry("500x720")
root.title("Image Editor")
global original_image, just_file_name, my_image, my_img_string, img, img90, img90_c, img180, img_flip_v, img_flip_h, img_flip_vh, edited_image, resized_image
save_count = 0

labelText = StringVar()
labelText.set("No Image")


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self,master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


def openfile():
    global my_image, img, my_img_string, original_image, just_file_name, edited_image, image_url
    root.filename = filedialog.askopenfilename(initialdir="C:/", title="Select a file", filetypes=(("", "*.jpg"), ("", "*.png"), ("", "*.bmp"), ("All files", "*.*")))
    my_img_string = root.filename
    labelText.set(my_img_string)

    just_file_name_array = my_img_string.split("/")
    just_file_name = just_file_name_array[-1]

    # Taking the image in cv2
    img = cv2.imread(my_img_string, -1)
    original_image = img
    edited_image = img


# Rotating the image in various Degree
def rotate90():
    global img90, edited_image
    img90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    edited_image = img90


def rotate90_c():
    global img90_c, edited_image
    img90_c = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    edited_image = img90_c


def rotate180():
    global img180, edited_image
    img180 = cv2.rotate(img, cv2.ROTATE_180)
    edited_image = img180


# Flipping the image
def img_flip_vertical():
    global img, edited_image, img_flip_v
    img_flip_v = cv2.flip(img, 0)
    edited_image = img_flip_v


def img_flip_horizontal():
    global img, edited_image, img_flip_h
    img_flip_h = cv2.flip(img, 1)
    edited_image = img_flip_h


def img_flip_v_h():
    global img, edited_image, img_flip_vh
    img_flip_vh = cv2.flip(img, -1)
    edited_image = img_flip_vh


def img_rotate_custom():
    global img, edited_image
    # getting image height and weight
    (h, w) = img.shape[:2]

    # getting center point of image height and weight
    img_center = w / 2, h / 2

    # Setting up custom angle and scale
    img_custom_angel = simpledialog.askinteger("User Input", "Please Enter Any Angel to Rotate")
    scale = 1.0

    # Functions that can performed custom rotation
    M = cv2.getRotationMatrix2D(img_center, img_custom_angel, scale)
    img_custom_rotated = cv2.warpAffine(img, M, (w, h))
    edited_image = img_custom_rotated


def make_black_and_white():
    global img, my_img_string, edited_image
    img = cv2.imread(my_img_string, 0)
    edited_image = img


def reset_original_image():
    global edited_image, original_image, img
    edited_image = original_image
    img = original_image


def image_resize():
    global edited_image, resized_image, img
    img_height = simpledialog.askinteger("User Input", "Please Enter New Height")
    img_width = simpledialog.askinteger("User Input", "please Enter New Width")
    custom_image_size = img_height, img_width
    resized_image = cv2.resize(img, custom_image_size)
    edited_image = resized_image


# Showing Rotated Image
def view_image():
    global edited_image, img, my_img_string

    while True:
        try:
            cv2.imshow(my_img_string, edited_image)
            cv2.waitKey(0)
            break
        except NameError:
            openfile()
            cv2.imshow(my_img_string, edited_image)
            cv2.waitKey(0)
            break


default_option = StringVar(root)
default_option.set("jpg")
format_selection = OptionMenu(root, default_option, "jpg", "png", "bmp")
format_selection.config(font=('arial', 15, 'bold'), width=12, bg='green', fg='white')


def save_image():
    global just_file_name, save_count
    get_format = "." + default_option.get()
    cv2.imwrite('data/Image_Editor/' + just_file_name + "_Edited_" + str(save_count) + get_format, edited_image)
    save_count = save_count + 1


button_Open = HoverButton(root, text="Open File", font=('arial', 15, 'bold'), bg='green', fg='white', activebackground='#3061f2', command=openfile).pack(side=TOP)
image_url = Label(root, textvariable=labelText, font=('arial', 10)).pack()
separator_line1 = Label(root, text="_________________________________", font=('arial', 11, 'bold')).pack()
optionLabel = Label(root, text="Select an option", font=('arial', 15, 'bold')).pack()
button_BW = HoverButton(root, text="Make Black and White", font=('arial', 12, 'bold'), activebackground='silver', command=make_black_and_white).pack(side=TOP)
button_Rotate1 = HoverButton(root, text="Rotate 90", font=('arial', 12, 'bold'), activebackground='silver', command=rotate90).pack(side=TOP)
button_Rotate2 = HoverButton(root, text="Rotate 90 CCW", font=('arial', 12, 'bold'), activebackground='silver', command=rotate90_c).pack(side=TOP)
button_Rotate3 = HoverButton(root, text="Rotate 180", font=('arial', 12, 'bold'), activebackground='silver', command=rotate180).pack(side=TOP)
button_Rotate4 = HoverButton(root, text="Flip Vertical", font=('arial', 12, 'bold'), activebackground='silver', command=img_flip_vertical).pack(side=TOP)
button_Rotate5 = HoverButton(root, text="Flip Horizontal", font=('arial', 12, 'bold'), activebackground='silver', command=img_flip_horizontal).pack(side=TOP)
button_Rotate6 = HoverButton(root, text="Flip Vertical & Horizontal", font=('arial', 12, 'bold'), activebackground='silver', command=img_flip_v_h).pack(side=TOP)
button_Rotate7 = HoverButton(root, text="Custom Angel Rotation of Image", font=('arial', 12, 'bold'), activebackground='silver', command=img_rotate_custom).pack(side=TOP)

button_Resize = HoverButton(root, text="Image Resize", border=3, font=('arial', 12, 'bold'), activebackground='silver', command=image_resize).pack(side=TOP)
separator_line2 = Label(root, text="_________________________________", font=('arial', 11, 'bold')).pack(pady=(0, 0))

button_View = HoverButton(root, text="View", font=('arial', 12, 'bold'), bg='#9db87f', fg='black', width=15, activebackground='green', command=view_image).pack(side=TOP, pady=(15, 0))

separator_line2 = Label(root, text="_________________________________", font=('arial', 11, 'bold')).pack(side=TOP, pady=(0, 0))
format_label = Label(root, text="Select Format", font=('arial', 12, 'bold')).pack()

format_selection.pack()

button_save = HoverButton(root, text="Save Image", font=('arial', 15, 'bold'), bg='green', fg='white', width=15, activebackground='#3061f2', command=save_image).pack()
button_reset = HoverButton(root, text="Reset Image", font=('arial', 12, 'bold'), bg='#48869c', fg='white', activebackground='#3061f2', command=reset_original_image).pack()

button_Exit = HoverButton(root, text="Exit", font=('arial', 18, 'bold'), bg='#b82623', fg='white', width=root.winfo_reqwidth(), activebackground='#3061f2', command=exit).pack(side=BOTTOM)


root.mainloop()
