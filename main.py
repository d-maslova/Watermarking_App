from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageDraw, ImageFont

window = Tk()
files = []


def upload_image():  # add labels to show which/how many images are there to process
    global files
    filepaths = fd.askopenfilenames(initialdir="C:/Pictures", title="Select images to watermark",
                                    filetypes=[('Images', '*.jpg *.jpeg *.png')])
    for file in filepaths:
        files.append(file)
    return files


def select_watermark():
    watermark_im = fd.askopenfilename(initialdir="/", title="Select logo to use",
                                      filetypes=[('Images', '*.jpg *.jpeg *.png')])  # watermark image
    watermark = Image.open(watermark_im)
    watermark_copy = watermark.copy()  # watermark copy
    return watermark_copy


def watermark_text():
    global text_ent
    text_lb = Label(text="Type your watermark below:")
    text_lb.grid(row=1, column=1)
    text_ent = Entry(master=window, width=25)
    text_ent.grid(row=2, column=1)
    text_ent.focus()
    return text_ent, text_lb


def save_watermarked():
    watermark = select_watermark()
    images = files
    wm_x, wm_y = watermark.size
    try:
        text_wm = text_ent.get()
    except NameError:
        for file in images:
            im = Image.open(file)  # opens image
            im_copy = im.copy()  # makes copy of image
            x, y = im_copy.size
            resized_width, resized_height = (x // 10), (y // 10)  # size watermark to a 10th of background
            watermark.thumbnail((resized_width, resized_height))  # thumbnail keeps resize proportional
            padding = 5
            bottom_right = (x-padding - wm_x, y - padding - wm_y)  # position for bottom right corner of the background image
            im_copy.paste(watermark, bottom_right, watermark)
            im_copy.save(f"{file}_watermarked.png")
            im_copy.show()

    else:
        fontsize = 10
        image_fraction = 0.5
        font = ImageFont.truetype("arial.ttf", fontsize)  # Calculate the size of font so its viewable
        for file in images:
            im = Image.open(file)  # opens image
            im_copy = im.copy()  # makes copy of image
            im_copy_edit = ImageDraw.Draw(im_copy)
            while font.getsize(text_wm)[0] < image_fraction*im_copy.size[0]:
                fontsize += 1
                font = ImageFont.truetype("arial.ttf", fontsize)
            im_copy_edit.text((15, 15), text_wm, font=font)  # Calculate the size of font so its viewable goes here
            im_copy.save("this.png")
            im_copy.show()


window.title("WATERMARKER v1.0")
window.config(padx=50, pady=50)
canvas = Canvas(width=400, height=400)

# LABELS
img_label = Label(text="Choose image/s to watermark")
img_label.grid(row=0, column=0)
wm_label = Label(text="Select watermark to apply")
wm_label.grid(row=0, column=2)

var = IntVar()

# BUTTONS
im_button = Button(text="Upload", width=20, command=upload_image)
im_button.grid(row=1, column=0, padx=10, pady=10,)
ok_button = Button(text="Place and Save", width=20, command=save_watermarked)
ok_button.grid(row=3, column=1, padx=10, pady=10,)

# RADIO BUTTONS
rb_wm = Radiobutton(text="Use text", width=15, var=var, value=0, command=watermark_text, indicatoron=0)
rb_logo = Radiobutton(text="Use logo", width=15, var=var, value=1, command=select_watermark, indicatoron=0)
rb_wm.grid(row=1, column=2)
rb_logo.grid(row=2, column=2)


window.mainloop()
