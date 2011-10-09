import numpy as np
import Image
import ImageDraw
import ImageFont
from sys import platform

def txt2img(img_np, text, location,
            text_color="#ffffff", bg_color='#888888',
            font="DroidSans.ttf", FontSize=14):
    """
    Draws text with a transparent background   
    """
    if len(location) == 3:
        scale = location[2]
    else:
        scale = 1.0

    location = np.array(location[:2]) / scale
    img = Image.fromarray(np.uint8(img_np * 255))
    if platform == 'linux2':
        font_dir = "/usr/share/fonts/TTF/"
    elif platform == 'win32':
        font_dir = "C:/Windows/Fonts/"

    font_size = FontSize
    fnt = ImageFont.truetype(font_dir + font, font_size)

    #Draw a transparent black rectangle under the text

    # make an entirely black image
    imgblack = Image.new('RGBA', img.size, "#000000")

    # make a mask that masks out all
    mask = Image.new('L', img.size, "#000000")

    drawmask = ImageDraw.Draw(mask)
    drawmask.rectangle(
        [(location[1], location[0]),
         (location[1] + FontSize * len(text) * .6,
          location[0] + FontSize + 5)],
        fill = bg_color)

    # put the (somewhat) transparent bg on the main
    img.paste(imgblack, mask=mask)
    del drawmask

    #Draw the actual text
    draw = ImageDraw.Draw(img)

    # add some text to the main
    draw.text((location[1] + 5, location[0]),
              text, font=fnt, fill=text_color)
    del draw

    img_np = np.asarray(img) / 255.0
    return img_np


def draw_rect(im, loc, color=[1.0, 0, 0], win_size=[128, 64]):
    """
    Draws a rectangle with the boundary color
    """
    if len(loc) == 3:
        cur_sc = loc[2]
    else:
        cur_sc = 1.0  # normal size

    loc = loc / cur_sc

    win_size = np.array(win_size) / cur_sc

    color = tuple((np.array(color) * 255).astype('int'))
    img = Image.fromarray(np.uint8(im * 255))

    drawer = ImageDraw.Draw(img)

    drawer.line([(loc[1], loc[0]),
                 (loc[1], loc[0] + win_size[0])], fill=color)

    drawer.line([(loc[1], loc[0] + win_size[0]),
                 (loc[1] + win_size[1], loc[0] + win_size[0])], fill=color)

    drawer.line([(loc[1] + win_size[1], loc[0] + win_size[0]),
                 (loc[1] + win_size[1], loc[0])], fill=color)

    drawer.line([(loc[1] + win_size[1], loc[0]),
                 (loc[1], loc[0])], fill=color)

    return np.asarray(img) / 255.0


def draw_bounding_box(im, loc, score=None, text=None,
                      color=[1, 0, 0], win_size=[128, 64]):
    """
    Draw a bounding box
    """
    im = draw_rect(im, np.array(loc), color, win_size)

    if score is not None:
        im = txt2img(im, "%.3f" % score, loc,
                     bg="#ffffff", font="DroidSans.ttf", FontSize=14)
    elif text is not None:
        im = txt2img(im, text, loc,
                     bg="#ffffff", font="DroidSans.ttf", FontSize=14)

    return im

#def draw_rect(im, loc, color=[1.0,0,0],win_size = [128,64]):
#    window_size = np.array(win_size)
#
#    if len(loc) == 3:
#        cur_sc = loc[2]#np.power(1.2,sc)
#    else:
#        cur_sc = 1.0 #normal size
#
#    cur_loc = loc / cur_sc
#
#    ylo = max(cur_loc[0],0)
#    yhi = min(cur_loc[0]+window_size[0]/cur_sc, im.shape[0]-1)
#
#    xlo = max(cur_loc[1],0)
#    xhi = min(cur_loc[1]+window_size[1]/cur_sc, im.shape[1]-1)
#
#    r_color = np.array(color)
#
#    im[ylo,xlo:xhi,:] = r_color[np.newaxis,np.newaxis,:]
#    im[yhi,xlo:xhi,:] = r_color[np.newaxis,np.newaxis,:]
#
#    im[ylo:yhi,xlo,:] = r_color[np.newaxis,np.newaxis,:]
#    im[ylo:yhi,xhi,:] = r_color[np.newaxis,np.newaxis,:]
#
#    return im
