# Project Name: Image Editor
# Version: 0.1

# Importing necessary modules, packages
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import os
import cv2
import numpy as np
import re

# Making the Root App
root = Tk()
root.geometry("500x720")
root.title("Image Editor v0.1")
root.iconbitmap("./images/ImageEditor.ico")

# Global variable declaration
global img, original_image, just_file_name, my_image, my_img_string, img90, img90_c, img180, img_flip_v, img_flip_h, img_flip_vh, edited_image, resized_image
global img2, rotated_msg, create_msg
save_count = 0
screen_width = root.winfo_screenwidth()

# Regular Expression needed for String Separation
delimiters = ",", ".", " ", ";"
regex_pattern = '|'.join(map(re.escape, delimiters))

# Setting up empty Image URL
labelText = StringVar()
labelText.set("No Image")


# Creating custom hover button
class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self["activebackground"]

    def on_leave(self, e):
        self['background'] = self.defaultBackground


# Creating all the functions
# Function for Opening files
def openfile():
    global my_image, img, my_img_string, original_image, just_file_name, edited_image, image_url
    root.filename = filedialog.askopenfilename(initialdir=os.path.expanduser('~'), title="Select a file",
                                               filetypes=(("", "*.jpg"), ("", "*.png"), ("", "*.bmp"), ("All files", "*.*")))
    my_img_string = root.filename
    labelText.set(my_img_string)

    just_file_name_array = my_img_string.split("/")
    just_file_name = just_file_name_array[-1]

    # Taking the image in cv2
    img = cv2.imread(my_img_string, -1)
    original_image = img
    edited_image = img


def openfile2():
    global img2
    root.filename2 = filedialog.askopenfilename(initialdir=os.path.expanduser('~'), title="Select a file",
                                                filetypes=(("", "*.jpg"), ("", "*.png"), ("", "*.bmp"), ("All files", "*.*")))
    my_img_string2 = root.filename2
    # Taking the image in cv2
    img2 = cv2.imread(my_img_string2, -1)


# Rotation Functions
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


def img_rotate_custom():
    global img, edited_image, rotated_msg
    # getting image height and weight
    (h, w) = img.shape[:2]

    # getting center point of image height and weight
    img_center = w / 2, h / 2

    # Setting up custom angle and scale
    img_custom_angle = simpledialog.askinteger("User Input", "Please Enter Any Angle to Rotate")
    rotated_msg = str(img_custom_angle) + " Degree"
    scale = 1.0

    # Functions that can performed custom rotation
    M = cv2.getRotationMatrix2D(img_center, img_custom_angle, scale)
    img_custom_rotated = cv2.warpAffine(img, M, (w, h))
    edited_image = img_custom_rotated


# Flipping Functions
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


# Applying Rotation functions into one single function
def rotate_image():
    get_rotation = rotate_option.get()
    global rotated_msg
    successful_rotate = False

    while True:
        try:
            if get_rotation == "90 Degree Clockwise":
                rotate90()
                rotated_msg = "90 Degree"
                successful_rotate = True
                break
            elif get_rotation == "90 Degree Counter Clockwise":
                rotate90_c()
                rotated_msg = "90 Degree"
                successful_rotate = True
                break
            elif get_rotation == "180 Degree":
                rotate180()
                rotated_msg = "90 Degree"
                successful_rotate = True
                break
            elif get_rotation == "Custom Degree":
                img_rotate_custom()
                successful_rotate = True
                break
            else:
                messagebox.showwarning("Invalid Rotation", "Please select a rotation")
                break
        except NameError:
            messagebox.showwarning("No Image is Selected", "Please Open an Image")
            break

    if successful_rotate:
        messagebox.showinfo("Rotation Successful", "Image Rotated " + rotated_msg)


# Applying all flip functions into single flip function
def flip_image():
    get_flip = flip_option.get()
    successful_flip = False
    flip_msg = "None"

    while True:
        try:
            if get_flip == "Flip Vertical":
                img_flip_vertical()
                flip_msg = "Flipped Vertically"
                successful_flip = True
                break
            elif get_flip == "Flip Horizontal":
                img_flip_horizontal()
                flip_msg = "Flipped Horizontally"
                successful_flip = True
                break
            elif get_flip == "Flip Vertical and Horizontal":
                img_flip_v_h()
                flip_msg = "Flipped Vertically and Horizontally"
                successful_flip = True
                break
            else:
                messagebox.showwarning("Invalid Flip", "Please select a Flip")
                break
        except NameError:
            messagebox.showwarning("No Image is Selected", "Please Open an Image")
            break
    if successful_flip:
        messagebox.showinfo("Flip Successful", "Image is " + flip_msg)


def make_black_and_white():
    if labelText.get() == "No Image":
        messagebox.showwarning("No Image Input", "Please Open an Image First")
    else:
        global img, my_img_string, edited_image
        img = cv2.imread(my_img_string, 0)
        edited_image = img
        messagebox.showinfo("Make Black and White Image Successful",
                            "Image is successfully made Black and White, Click View to See it.")


# Image Resize function
def image_resize():
    global edited_image, resized_image, img

    if labelText.get() == "No Image":
        messagebox.showwarning("No Image Input", "Please Open an Image First")
    else:
        img_height = simpledialog.askinteger("User Input", "Please Enter New Height")
        img_width = simpledialog.askinteger("User Input", "please Enter New Width")
        custom_image_size = img_height, img_width
        resized_image = cv2.resize(img, custom_image_size)
        edited_image = resized_image
        messagebox.showinfo("Image Resize Successful", "Image is Resized to " + str(img_height) + "px X " + str(
            img_width) + "px. Click View to see the new image.")


# Create Blank Image function
def create_blank_img():
    global img, original_image, edited_image, my_img_string, just_file_name, create_msg

    img_height = simpledialog.askinteger("User Input", "Please Enter Image Height")
    img_width = simpledialog.askinteger("User Input", "Please Enter Image Width")

    blank_image_color = simpledialog.askinteger("User Input", "Please Enter Color Choice: 0 = Black, 255 is White ")
    if blank_image_color == 0:
        img = np.zeros((img_height, img_width, 3), np.uint8)
        original_image = img
    elif blank_image_color == 255:
        img = np.ones((img_height, img_width, 3), np.uint8) * 255
        original_image = img
    else:
        messagebox.showwarning("Invalid Choice", "Please try again")

    edited_image = img
    my_img_string = "Blank Image"
    just_file_name = my_img_string
    labelText.set(my_img_string)
    create_msg = "Blank Image"
    messagebox.showinfo("Create Successful", create_msg + " is Created, Click View to See the Image")


def create_blank_page():
    global img, original_image, edited_image
    img_height = simpledialog.askinteger("User Input", "Please Enter Image Height")
    img_width = simpledialog.askinteger("User Input", "Please Enter Image Width")
    blank_image_color = simpledialog.askinteger("User Input", "Please Enter Background Color Choice: 0 = Black, 255 is White ")

    if blank_image_color == 0:
        img = np.zeros((img_height, img_width, 3), np.uint8)
        original_image = img
    elif blank_image_color == 255:
        img = np.ones((img_height, img_width, 3), np.uint8) * 255
        original_image = img
    else:
        messagebox.showwarning("Invalid Choice", "Please try again")

    edited_image = img


# Create Line function
def create_line():
    global img, edited_image, my_img_string, just_file_name, create_msg, regex_pattern

    create_blank_page()
    line_pos1 = re.split(regex_pattern, simpledialog.askstring("User Input", "Please Enter Line Co-Ordinate x1, y1"))
    line_x1, line_y1 = int(line_pos1[0]), int(line_pos1[1])
    line_pos2 = re.split(regex_pattern, simpledialog.askstring("User Input", "Please Enter Line Co-Ordinate x2, y2"))
    line_x2, line_y2 = int(line_pos2[0]), int(line_pos2[1])
    line_color_string = re.split(regex_pattern,
                                 simpledialog.askstring("User Input", "Please Enter Line color in RGB mode. Ex. 255,0,0"))
    line_color_string.reverse()
    line_color = tuple([int(i) for i in line_color_string])
    line_weight = simpledialog.askinteger("User Input", "Please Enter Line weight")
    img = cv2.line(img, (line_x1, line_y1), (line_x2, line_y2), line_color, line_weight)
    edited_image = img
    my_img_string = "Line"
    just_file_name = my_img_string
    labelText.set(my_img_string)
    create_msg = "Line"
    messagebox.showinfo("Create Successful", create_msg + " is Created, Click View to See the Image")


# Create Circle function
def create_circle():
    global img, edited_image, my_img_string, just_file_name, create_msg

    create_blank_page()
    circle_pos = re.split(regex_pattern, simpledialog.askstring("User Input", "Please Enter Circle Co-Ordinate x1, y1"))
    circle_pos_x1, circle_pos_y1 = int(circle_pos[0]), int(circle_pos[1])
    circle_radius = simpledialog.askinteger("User Input", "Please Enter Circle Radius")
    circle_color_string = re.split(regex_pattern,
                                   simpledialog.askstring("User Input", "Please Enter Circle color in RGB mode. Ex. 255,0,0"))
    circle_color_string.reverse()
    circle_color = tuple([int(i) for i in circle_color_string])
    img = cv2.circle(img, (circle_pos_x1, circle_pos_y1), circle_radius, circle_color, -1)
    edited_image = img
    my_img_string = "Circle"
    just_file_name = my_img_string
    labelText.set(my_img_string)
    create_msg = "Circle"
    messagebox.showinfo("Create Successful", create_msg + " is Created, Click View to See the Image")


# Create Ellipse function
def create_ellipse():
    global img, edited_image, my_img_string, just_file_name, create_msg
    create_blank_page()
    img = cv2.ellipse(img, (256, 256), (170, 50), 0, 0, 360, (0, 180, 0), -1)
    edited_image = img
    my_img_string = "Ellipse"
    just_file_name = my_img_string
    labelText.set(my_img_string)
    create_msg = "Ellipse"
    messagebox.showinfo("Create Successful", create_msg + " is Created, Click View to See the Image")


# Create Rectangle function
def create_rectangle():
    global img, edited_image, my_img_string, just_file_name, create_msg
    create_blank_page()

    rectangle_pt1 = re.split(regex_pattern,
                             simpledialog.askstring("User Input", "Please Enter Rectangle Point1:  x1, y1"))
    pt1 = (int(rectangle_pt1[0]), int(rectangle_pt1[1]))
    rectangle_pt2 = re.split(regex_pattern,
                             simpledialog.askstring("User Input", "Please Enter Rectangle Point2: x2, y2"))
    pt2 = int(rectangle_pt2[0]), int(rectangle_pt2[1])
    rectangle_color_string = re.split(regex_pattern,
                                      simpledialog.askstring("User Input", "Please Enter Line color in RGB mode: Ex. 255,0,0"))
    rectangle_color_string.reverse()
    rectangle_color = tuple([int(i) for i in rectangle_color_string])
    rectangle_thickness = simpledialog.askinteger("User Input", "Please Enter rectangle thickness")

    img = cv2.rectangle(img, pt1, pt2, rectangle_color, rectangle_thickness)
    edited_image = img
    my_img_string = "Rectangle"
    just_file_name = my_img_string
    labelText.set(my_img_string)
    create_msg = "Rectangle"
    messagebox.showinfo("Create Successful", create_msg + " is Created, Click View to See the Image")


# Put Text into image function
def put_text():
    global img, edited_image, my_img_string, just_file_name

    while True:
        try:
            your_text = simpledialog.askstring("User Input", "Please Enter Your Text: ")
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_pos_string = re.split(regex_pattern,
                                       simpledialog.askstring("User Input", "Please Enter Text Position:  x1, y1"))
            text_pos = (int(text_pos_string[0]), int(text_pos_string[1]))

            text_color_string = re.split(regex_pattern,
                                         simpledialog.askstring("User Input", "Please Enter Text color in RGB mode. Ex. 255,0,0"))
            text_color_string.reverse()
            text_color = tuple([int(i) for i in text_color_string])
            text_size = simpledialog.askfloat("User Input", "Please Enter Font Size: ")
            text_weight = simpledialog.askinteger("User Input", "Please Enter Text Thickness or Weight: ")
            cv2.putText(img, your_text, text_pos, font, text_size, text_color, text_weight, cv2.LINE_AA)
            edited_image = img
            cv2.imshow('image', img)
            cv2.waitKey(0)
            break
        except NameError:
            messagebox.showwarning("No Image is selected", "Please open an image or create a blank image first")
            break


# Add two image together function
def add_two_image():
    global img, img2, edited_image, my_img_string, just_file_name
    messagebox.showinfo("Please Select Two Images One", "Select the first image, then select the second image")

    openfile()
    openfile2()

    img_alpha = simpledialog.askfloat("User Input", "Please Enter Alpha Value for the first Image: 0.0 - 1.0 ")
    img2_beta = simpledialog.askfloat("User Input", "Please Enter Beta Value for the second Image: 0.0 - 1.0 ")
    img3 = cv2.addWeighted(img, img_alpha, img2, img2_beta, 0)
    edited_image = img3
    messagebox.showinfo("Image Blending Successful", "Click View to See the Image")


# Create Functions Applied into single create function
def image_create():
    global create_msg
    get_create = create_option.get()

    while True:
        try:
            if get_create == "Blank Image":
                create_blank_img()
                break
            elif get_create == "Line":
                create_line()
                break
            elif get_create == "Rectangle":
                create_rectangle()
                create_msg = "Rectangle"
                break
            elif get_create == "Circle":
                create_circle()
                break
            elif get_create == "Ellipse":
                create_ellipse()
                break
            else:
                messagebox.showwarning("Invalid Create", "Please select a Create Object")
                break
        except NameError:
            messagebox.showwarning("No Image is Selected", "Please Open an Image")
            break


# View Image function
def view_image():
    global edited_image, my_img_string

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


# Save Image function
def save_image():
    global just_file_name, save_count
    global my_image, img, my_img_string, original_image, just_file_name, edited_image, image_url

    if labelText.get() == "No Image":
        messagebox.showwarning("No Image Input", "Please Open an Image First")

    else:
        select_location = filedialog.askdirectory(initialdir="C:/", title="Select a folder")
        print(select_location)
        get_format = "." + default_option.get()
        cv2.imwrite(os.path.join(select_location, just_file_name + "_Edited_" + str(save_count)) + get_format, edited_image)
        save_count = save_count + 1
        messagebox.showinfo("Save Successful", "Image is Saved to " + select_location)


# Reset Image function
def reset_original_image():
    global edited_image, original_image, img

    if labelText.get() == "No Image":
        messagebox.showwarning("No Image Input", "There is nothing to reset. Please Open an image and edit it first")
    else:
        edited_image = original_image
        img = original_image
        messagebox.showinfo("Reset Successful", "Image is Reset to Original")


# About function
def about_info():
    messagebox.showinfo("About Image Editor",
                        "Image Editor \n Version 0.1 \n Made with Python, tkinter and OpenCV \n Code Writen by Shuvongkor Barman. \n "
                        "https://github.com/shuvongkor-barman/ImageEditor_Python")


# Drop down menu design
rotate_option = StringVar(root)
rotate_option.set("Select Rotation")
rotate_selection = OptionMenu(root, rotate_option, "90 Degree Clockwise", "90 Degree Counter Clockwise", "180 Degree",
                              "Custom Degree")
rotate_selection.config(font=('arial', 12, 'bold'), bg='green', fg='white')

flip_option = StringVar(root)
flip_option.set("Select Flip Option")
flip_selection = OptionMenu(root, flip_option, "Flip Vertical", "Flip Horizontal", "Flip Vertical and Horizontal")
flip_selection.config(font=('arial', 12, 'bold'), bg='green', fg='white')

default_option = StringVar(root)
default_option.set("jpg")
format_selection = OptionMenu(root, default_option, "jpg", "png", "bmp")
format_selection.config(font=('arial', 12, 'bold'), width=12, bg='green', fg='white')

create_option = StringVar(root)
create_option.set("Select Create Object")
create_selection = OptionMenu(root, create_option, "Blank Image", "Line", "Rectangle", "Circle", "Ellipse")
create_selection.config(font=('arial', 12, 'bold'), bg='green', fg='white')

# Button Design Section

# Open Button
button_open_icon = PhotoImage(file=os.path.join("./images/", "open.png"))
button_open_icon_fit = button_open_icon.subsample(2, 2)
button_Open = HoverButton(root, text="Open File", image=button_open_icon_fit, compound=LEFT, font=('arial', 15, 'bold'),
                          bg='gray', fg='white', activebackground='#3061f2', width=root.winfo_screenwidth(), command=openfile).pack(side=TOP)
# Image URL
image_url = Label(root, textvariable=labelText, font=('arial', 10)).pack()
button_BW = HoverButton(root, text="Make Black and White", font=('arial', 12, 'bold'), activebackground='silver',
                        command=make_black_and_white).pack(side=TOP)
# Rotate Selection Drop Down button
rotate_selection.pack()
button_rotate_icon = PhotoImage(file=os.path.join("./images/", "rotate.png"))
button_rotate_icon_fit = button_rotate_icon.subsample(2, 2)
button_Rotate = HoverButton(root, text="Rotate Image", image=button_rotate_icon_fit, compound=LEFT,
                            font=('arial', 12, 'bold'), activebackground='silver', command=rotate_image).pack(side=TOP)
# Flip Button
flip_selection.pack()
button_flip_icon = PhotoImage(file=os.path.join("./images/", "flip.png"))
button_flip_icon_fit = button_flip_icon.subsample(2, 2)
button_flip = HoverButton(root, text="Flip Image", image=button_flip_icon_fit, compound=LEFT,
                          font=('arial', 12, 'bold'), activebackground='silver', command=flip_image).pack(side=TOP)
# Resize Button
button_resize_icon = PhotoImage(file=os.path.join("./images/", "resize.png"))
button_resize_icon_fit = button_resize_icon.subsample(2, 2)
button_Resize = HoverButton(root, text="Image Resize", image=button_resize_icon_fit, compound=LEFT, border=3,
                            font=('arial', 12, 'bold'), activebackground='silver', command=image_resize).pack(side=TOP)

# Create Button
create_selection.pack()
button_create = HoverButton(root, text="Create", border=3, font=('arial', 12, 'bold'), activebackground='silver', command=image_create).pack(side=TOP)
# Put Text in image Button
button_put_text = HoverButton(root, text="Put Text in an Image", border=3, font=('arial', 12, 'bold'), activebackground='silver', command=put_text).pack(side=TOP)
# Add Two Image Button
button_add_two_image = HoverButton(root, text="Add Two Image", border=3, font=('arial', 12, 'bold'), activebackground='silver', command=add_two_image).pack(side=TOP)
separator_line2 = Label(root, text="_________________________________", font=('arial', 11, 'bold')).pack(pady=(0, 0))

# View Button
button_view_icon = PhotoImage(file=os.path.join("./images/", "view.png"))
button_view_icon_fit = button_view_icon.subsample(2, 2)
button_View = HoverButton(root, text="View", image=button_view_icon_fit, compound=LEFT, font=('arial', 12, 'bold'),
                          bg='#9db87f', fg='black', width=90, activebackground='green', command=view_image).pack(side=TOP, pady=(15, 0))
separator_line2 = Label(root, text="_________________________________", font=('arial', 11, 'bold')).pack(side=TOP, pady=(0, 0))

# Image Format Selection Drop down button
format_label = Label(root, text="Convert or Save Format", font=('arial', 12, 'bold')).pack()
format_selection.pack()

# Save Button
button_save = HoverButton(root, text="Save Image", font=('arial', 13, 'bold'), bg='green', fg='white', width=15,
                          activebackground='#3061f2', command=save_image).pack()
# Reset Button
button_reset = HoverButton(root, text="Reset Image", font=('arial', 12, 'bold'), bg='#48869c', fg='white',
                           activebackground='#3061f2', command=reset_original_image).pack()
# Button About
button_about = HoverButton(root, text="About", font=('arial', 8, 'bold'), bg='#48869c', fg='white',
                           activebackground='#3061f2', command=about_info).pack()
# Button Exit
button_Exit = HoverButton(root, text="Exit", font=('arial', 15, 'bold'), bg='#b82623', fg='white', width=screen_width, activebackground='#3061f2', command=exit).pack(side=BOTTOM)
# End of Program


root.mainloop()
