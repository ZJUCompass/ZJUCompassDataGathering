# -*- coding:utf-8 -*-
import sys,os
from PIL import Image

if __name__ == "__main__":
    input_dir = r"data\teacher_imgs"
    output_dir = r"data\resized_teacher_imgs"
    imgs = os.listdir(input_dir)
    for img in imgs:
        try:
            input_file = os.path.join(input_dir,img)
            img = img.replace(".jpg",".png")
            img = "t_" + img
            output_file = os.path.join(output_dir,img)
            print input_file
            pil_im = Image.open(input_file)
            pil_im = pil_im.convert('RGB')
            width,length = pil_im.size
            min_len = min(width,length)
            if min_len == width:
                new_length = int(length * 128.0 / width)
                new_width = 128 
            else:
                new_width = int(width * 128.0 / length)
                new_length = 128
            pil_im = pil_im.resize((new_width,new_length))
            pil_im.save(output_file)
        except:
            pass
            

    """
    pil_im = Image.open("data/teacher_imgs/2462.jpg")
    #pil_im.thumbnail((128,128))
    pil_im = pil_im.convert('RGB')
    pil_im.save("data/resized_teacher_imgs/2462.jpg")
    """