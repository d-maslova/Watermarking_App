from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageDraw, ImageFont

window = Tk()

files = []


def upload_image():
    global files
    filepaths = fd.askopenfilenames(initialdir="C:/Pictures", title="Select images to watermark",
                                filetypes=[('Images', '*.jpg *.jpeg *.png')])
    for file in filepaths:
        files.append(file)
    return files


def select_watermark():
    choice = var.get()
    if choice == 0:
        text_ent = Entry(master=window, text="Type your text here")
        text_ent.insert(0, "Type watermark here")
        text_ent.grid(row=1, column=1)
        return text_ent
    elif choice == 1:
        watermark_im = Image.open("logo.png")  # watermark image
        watermark_copy = watermark_im.copy()  # watermark copy
        return watermark_copy


def save_watermarked():
    images = files
    watermark = select_watermark()
    wm_x, wm_y = watermark.size
    for file in images:
        im = Image.open(file)  # opens image
        im_copy = im.copy()  # makes copy of image
        x, y = im_copy.size
        resized_width, resized_height = (x // 10), (y // 10)  # size watermark to a 10th of background
        watermark.thumbnail((resized_width, resized_height))  # thumbnail keeps resize proportional
        padding = 5
        bottom_right = (x - padding - wm_x, y - padding - wm_y)  # position for bottom right corner of the background image
        im_copy.paste(watermark, bottom_right, watermark)
        im_copy.save(f"{file}_watermarked.png")
        im_copy.show()


window.title("WATERMARKER 1.0")
window.config(padx=50, pady=50)
canvas = Canvas(width=400, height=400)

# LABELS
img_label = Label(text="Image/s to watermark")
img_label.grid(row=0, column=0)
wm_label = Label(text="Select watermark to apply")
wm_label.grid(row=0, column=2)

var = IntVar()

# BUTTONS
im_button = Button(text="Select", width=15, command=upload_image)
im_button.grid(row=1, column=0, padx=10, pady=10,)
ok_button = Button(text="Place and save", width=20, command=save_watermarked)
ok_button.grid(row=3, column=1, padx=10, pady=10,)

# RADIOBUTTONS
rb_wm = Radiobutton(text="Use text", width=15, var=var, value=0, command=select_watermark, indicatoron=0)
rb_logo = Radiobutton(text="Choose logo", width=15, var=var, value=1, command=select_watermark, indicatoron=0)
rb_wm.grid(row=1, column=2)
rb_logo.grid(row=2, column=2)


window.mainloop()
