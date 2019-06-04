from tkinter import *
from tkinter import filedialog
import os as os
import numpy as np


def browse_button():
    global folder_path
    filename=filedialog.askdirectory()
    folder_path.set(filename)

#get in a folder open all the files and stores them in an array, using a double array format
def form_folder_to_arrays(path):
    data_storage= []
    data_storage_counter=0
    for file_names in os.listdir(path):
        #the files containing wavefront information are in wft extension
        if not str.endswith(file_names, ".wft"):
            continue
        f= open(path+'\\'+file_names,'r')
        data_storage.append([])
        for lines in f:
            raw=(lines.split('\t'))
            #replace NaN by 0 and convert to float
            filtered=list(map(lambda x: float(x) if not("NaN" in x) else 0., raw))
            #if list is not empty
            data_storage[data_storage_counter].append(filtered)
        data_storage_counter=data_storage_counter+1
    
    return data_storage

def calculate_RMS_images(data): 
    RMS_images=[None]*len(data)
    for i,image in enumerate(data):
        RMS_images[i]=np.std(image)
    return RMS_images

def calculate_RMS_pixel_by_pixel(data):
    RMS_pixels=np.std(data, axis=0)
    return RMS_pixels

        


def calculate_everything(path_to_folder):
    data=form_folder_to_arrays(path_to_folder)
    RMS_images=calculate_RMS_images(data)
    global mean_RMS
    mean_RMS.set(np.mean(RMS_images))
    global RMS_RMS
    RMS_RMS.set(np.std(RMS_images))
    RMS_pixel_by_pixel=calculate_RMS_pixel_by_pixel(data)
    global RMS_pixels
    RMS_pixels.set(np.mean(RMS_pixel_by_pixel))

root = Tk()
root.title("HAS Analyzer")
root.geometry("500x500")
folder_path = StringVar()
mean_RMS= DoubleVar()
RMS_RMS = DoubleVar()
RMS_pixels =DoubleVar()
lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=0, column=2)
button2 = Button(text="Browse folder", command=browse_button)
button2.grid(row=0, column=1)
button3 = Button(text="Do it", command=lambda: calculate_everything(folder_path.get()))
button3.grid(row=0, column=0)
#titles
lbl_mean_rms_global_title = Label(master=root, text="Mean of the RMS of the images: ")
lbl_mean_rms_global_title.grid(row=1, column=0, sticky="W")
lbl_rms_rms_global_title = Label(master=root, text="RMS of the RMS of the images: ")
lbl_rms_rms_global_title.grid(row=2, column=0, sticky="W")
lbl_rms_pixel_by_pixel_title = Label(master=root, text="Mean of RMS pixel by pixel: ")
lbl_rms_pixel_by_pixel_title.grid(row=3, column=0, sticky="W")


#values
lbl_mean_rms_global_value = Label(master=root, textvariable=mean_RMS)
lbl_mean_rms_global_value.grid(row=1, column=1, sticky="W")
lbl_rms_rms_global_value = Label(master=root, textvariable=RMS_RMS)
lbl_rms_rms_global_value.grid(row=2, column=1, sticky="W")
lbl_rms_pixel_by_pixel_value = Label(master=root, textvariable=RMS_pixels)
lbl_rms_pixel_by_pixel_value.grid(row=3, column=1, sticky="W")

mainloop()
