from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageDraw, ImageFont

window = Tk()
file_frame = Frame(window)
files = []
watermark_copy = Image


def upload_image():  # add labels to show which/how many images are there to process
    global files
    filepaths = fd.askopenfilenames(initialdir="C:/Pictures", title="Select images to watermark",
                                    filetypes=[('Images', '*.jpg *.jpeg *.png')])
    for file in filepaths:
        files.append(file)
    list_images(files)
    return files


def list_images(im_files):
    file_len = len(im_files)
    for i in range(file_len):
        myl_abel = Label(text=im_files[i][-10:]).grid(column=1, row=i+2)


def select_watermark():
    global watermark_copy
    watermark_im = fd.askopenfilename(initialdir="/", title="Select logo to use",
                                      filetypes=[('Images', '*.jpg *.jpeg *.png')])  # watermark image
    watermark = Image.open(watermark_im)
    watermark_copy = watermark.copy()  # watermark copy
    return watermark_copy


def watermark_text():
    global text_ent
    text_ent = Entry(master=window, width=25)
    text_ent.grid(column=0, row=5, padx=10, pady=10)
    text_ent.focus()
    return text_ent


def save_watermarked():
    images = files
    try:
        text_wm = text_ent.get()
    except NameError:
        watermark = watermark_copy
        wm_x, wm_y = watermark.size
        for file in images:
            im = Image.open(file)
            im_copy = im.copy()
            x, y = im_copy.size
            resized_width, resized_height = (x // 10), (y // 10)  # size watermark to 1/10th of background
            watermark.thumbnail((resized_width, resized_height))  # thumbnail keeps resize proportional
            padding = 10
            # position for bottom right corner of the background image:
            bottom_right = (x-padding - wm_x, y - padding - wm_y)
            im_copy.paste(watermark, bottom_right, watermark)
            im_copy.save(f"{file}_watermarked.png")
            im_copy.show()
    else:
        fontsize = 10
        image_fraction = 0.1  # 1/10th of image size
        font = ImageFont.truetype("arial.ttf", fontsize)
        for file in images:
            im = Image.open(file)
            im_copy = im.copy()
            im_copy_edit = ImageDraw.Draw(im_copy)
            # CALCULATE FONT SIZE
            while font.getsize(text_wm)[0] < image_fraction*im_copy.size[0]:
                fontsize += 1
                font = ImageFont.truetype("arial.ttf", fontsize)
            im_copy_edit.text((15, 15), text_wm, font=font)
            im_copy.save(f"{file}_w_text.png")
            im_copy.show()


window.title("WATERMARKER v1.0")
window.config(padx=40, pady=40)
canvas = Canvas(width=400, height=400)

# LABELS
img_label = Label(text="1. Choose image/s to watermark")
img_label.grid(row=0, column=0)
wm_label = Label(text="2. Select watermark to apply")
wm_label.grid(row=2, column=0)

var = IntVar()

# BUTTONS
im_button = Button(text="Upload", width=20, command=upload_image)
im_button.grid(row=1, column=0, padx=10, pady=10,)
ok_button = Button(text="3. Place and Save", width=20, command=save_watermarked)
ok_button.grid(row=6, column=0, padx=10, pady=10,)

# RADIO BUTTONS
rb_wm = Radiobutton(text="Use text", width=15, var=var, value=0, command=watermark_text, indicatoron=0,)
rb_logo = Radiobutton(text="Use logo", width=15, var=var, value=1, command=select_watermark, indicatoron=0)
rb_wm.grid(row=3, column=0, padx=5, pady=5)
rb_logo.grid(row=4, column=0, padx=5, pady=5)

window.mainloop()
