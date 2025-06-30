
# youtube link: https://www.youtube.com/watch?v=ibf5cx221hk

import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *


class MyGUI:    

    def __init__(self, fastLoadTest = False, conversion_callback = None):
        self.conversionCallback = conversion_callback
        self.root       = tk.Tk()

        self.root.title("Readability Tool Text to Image Converter")

        self.root.iconbitmap("icon.ico")

        
        # make the dialog box 700 x 400 pixels 
        dbox_x          = 700
        dbox_y          = 425

        # convert dialog box size into string for geometry function below
        dbox_size_text  = str(dbox_x) + "x" + str(dbox_y)        

        self.root.geometry(dbox_size_text)

        # positions 
        start_x         = 50 # position where entry/buttons start (x axis)
        start_y         = 10 # position where entry/buttons start (y axis)
        barhop_y        = 20 # pixels to pad after labels of entries 
        linehop_y       = 60 # pixels to pad after each button/entry component (x axis)
        


        # pathing sizes
        pathrect_x      = 300 # width of path entry 
        buttonrect_x    = 100 # width of path buttons 

        columnhop_x      = pathrect_x + buttonrect_x + 50

        # font size for GUI
        fontsize        = 8

        file_path       = tk.StringVar(self.root) # initialize file path
        folder_path     = tk.StringVar(self.root) # initialize folder path 
        font_folder_path  = tk.StringVar(self.root) # initialize font scaling file path 
        reference_font_path = tk.StringVar(self.root) # initialize reference font path
        pixels_x_text   = tk.StringVar(self.root,value="1024") # initialize image file size in pix (x axis)
        pixels_y_text   = tk.StringVar(self.root,value="768") # initialize image file size in pix (y axis)
        font_extension  = tk.StringVar(self.root,value=".woff") # initialize font file extension
        font_size       = tk.StringVar(self.root,value="24") # initialize font size for image output

        # convert button state (enabled after entries)
        convState =  ["disabled" , 'normal'] [fastLoadTest]

        ###############
        # SELECT FILE #
        ###############
        # path label
        self.fontFileLabel      = tk.Label(self.root, text = "Select Stimulus Set", font = ('Arial', fontsize))
        # position label
        self.fontFileLabel.place(x = start_x, y=start_y)
        # path entry bar
        self.selectFile         = tk.Entry(self.root,textvariable=file_path)
        #position the bar
        self.selectFile.place(x = start_x, y=start_y+barhop_y, width = pathrect_x)

        # SELECT FILE BUTTON
        # specifies what is and where the select stim set file button will be
        self.fileButton         = tk.Button(self.root,text = "Select File", font = ('Arial',fontsize),command = self.browse_file_button)      

        self.fileButton.place(x = int(round(pathrect_x*1.05))+start_x, y=start_y+barhop_y , width = buttonrect_x)

        ##########################
        # SELECT REFERENCE FONT  #
        ##########################
        # path label
        self.referenceFontLabel      = tk.Label(self.root, text = "Select Reference Font", font = ('Arial', fontsize))
        # position label
        self.referenceFontLabel.place(x = start_x + columnhop_x, y=start_y)
        # path entry bar
        self.selectReferenceFont         = tk.Entry(self.root, textvariable=reference_font_path)
        #position the bar
        self.selectReferenceFont.place(x = start_x + columnhop_x, y=start_y + barhop_y, width = pathrect_x)

        # SELECT FILE BUTTON
        # specifies what is and where the select stim set file button will be
        self.fileButton         = tk.Button(self.root,text = "Select File", font = ('Arial',fontsize),command = self.browse_reference_font)      

        self.fileButton.place(x = int(round(pathrect_x*1.05))+start_x + columnhop_x, y= start_y + barhop_y , width = buttonrect_x)


        #################
        # SELECT FOLDER #
        #################
        secondLineY = start_y+linehop_y
        # path label
        self.folderLabel        = tk.Label(self.root, text = "Select Image Output Folder", font = ('Arial',fontsize))
        # position label
        self.folderLabel.place(x = start_x, y = start_y + linehop_y)
        # path entry bar         
        self.selectFolder       = tk.Entry(self.root,textvariable=folder_path)
        # position the bar 
        self.selectFolder.place(x = start_x, y=secondLineY+barhop_y, width = pathrect_x)

        # SELECT FOLDER BUTTON 
        # specifies what is and where the select image output folder button will be
        self.folderButton       = tk.Button(self.root,text = "Select Folder", font = ('Arial',fontsize),command = self.browse_folder_button)
        self.folderButton.place(x = int(round(pathrect_x*1.05))+start_x, y=start_y+linehop_y+barhop_y , width = buttonrect_x)

        ##############
        # FONT FILES #
        ##############```   `
        
        thirdLineY              = start_y+(linehop_y*2)
        # path label
        self.fontFileLabel      = tk.Label(self.root, text = "Select Font Files", font = ('Arial',fontsize))
        # position label
        self.fontFileLabel.place(x = start_x, y = thirdLineY)
        # path entry bar
        self.selectFontFile     = tk.Entry(self.root,textvariable=font_folder_path)
        #position the bar
        self.selectFontFile.place(x = start_x, y=thirdLineY+barhop_y, width = pathrect_x)

        # SELECT FONT SCALING BUTTON
        # specifies what is and where the select stim set file button will be
        self.fontFileButton     = tk.Button(self.root,text = "Select File", font = ('Arial',fontsize),command = self.browse_font_folder)      

        self.fontFileButton.place(x = int(round(pathrect_x*1.05))+start_x, y=thirdLineY+barhop_y , width = buttonrect_x)        

        #########################
        # IMAGE SIZE PIXELS BAR #
        #########################
        # X AXIS 
        fourthLineY = start_y+(linehop_y*3)
        # x axis label
        self.pixelsXlabel       = tk.Label(self.root, text = "Pixels X axis (horizontal)", font = ('Arial',fontsize))
        # position label
        self.pixelsXlabel.place(x = start_x, y=fourthLineY)
        # entry bar
        self.pixelsX            = tk.Entry(self.root,textvariable=pixels_x_text)
        # position the bar
        self.pixelsX.place(x = start_x, y=fourthLineY+barhop_y, width = pathrect_x/3)

        # Y AXIS 
        # y axis label
        self.pixelsXlabel       = tk.Label(self.root, text = "Pixels Y axis (vertical)", font = ('Arial',fontsize))
        # position label
        self.pixelsXlabel.place(x = (start_x+(pathrect_x/3))*1.3, y=fourthLineY)
        # entry bar
        self.pixelsY            = tk.Entry(self.root,textvariable=pixels_y_text)
        # position the bar
        self.pixelsY.place(x = (start_x+(pathrect_x/3))*1.3, y=fourthLineY+barhop_y, width = pathrect_x/3)

        ######################
        # FONT EXTENSION BAR #
        ######################
        # extension label 
        self.extensionLabel     = tk.Label(self.root, text = "Font file extension", font = ('Arial',fontsize))
        # position label
        self.extensionLabel.place(x = (start_x+(pathrect_x/3)*2)*1.3, y=fourthLineY)
        # entry bar
        self.extensionEntry     = tk.Entry(self.root,textvariable=font_extension)
        # position the bar
        self.extensionEntry.place(x = (start_x+(pathrect_x/3)*2)*1.3, y=fourthLineY+barhop_y, width = pathrect_x/4)

        #################
        # FONT SIZE BAR #
        #################
        # size label 
        self.sizeLabel          = tk.Label(self.root, text = "Font size (pixels)", font = ('Arial',fontsize))
        # position sizeLabel
        self.sizeLabel.place(x = (start_x+(pathrect_x/3)*3)*1.3, y=fourthLineY)
        # size entry bar
        self.sizeEntry          = tk.Entry(self.root,textvariable=font_size)
        # position the bar
        self.sizeEntry.place(x = (start_x+(pathrect_x/3)*3)*1.3, y=fourthLineY+barhop_y, width = pathrect_x/4)        

        ###############
        # SPACING BAR #
        ###############
        fifthLineY = start_y+(linehop_y*4)
        # spacing label
        self.spacingLabel       = tk.Label(self.root, text = "Enter letter spacing in em units (e.g. 0.05,0,0.05), leave empty for 0 spacing", font = ('Arial', fontsize))
        # position label
        self.spacingLabel.place(x = start_x, y = fifthLineY)
        # spacing entry bar
        self.spacingEntry       = tk.Entry(self.root, textvariable="")
        # position the bar
        self.spacingEntry.place(x = start_x, y=fifthLineY + barhop_y, width = pathrect_x/2)

        # START CONVERT BUTTON
        sixthLineY              = start_y+(linehop_y*5)
        # specifies what is and where the CONVERT button will be
        self.convertButton      = tk.Button(self.root,text = "Convert", font = ('Arial',fontsize*2),command = self.return_values, state=convState)
        self.convertButton.place(x = start_x, y=sixthLineY, width = buttonrect_x*1.5)

        #############################################
        ##   PROGRESS BAR                        ####
        #############################################
        self.progress = tk.IntVar()
        self.progressBar= Progressbar(orient=tk.HORIZONTAL, variable=self.progress, length=int(dbox_x * 0.7))
        self.progressBar.place (x=start_x, y=start_y + linehop_y*6)

        def conv_button_update(*args):
            if (len(file_path.get())>5) and (len(folder_path.get())>5) and (len(font_folder_path.get())>5) and (len(reference_font_path.get())>5):
                self.convertButton.config(state='normal')
                #print('larger than 5')
            else:
                self.convertButton.config(state='disabled')
                #print('smaller than 5')

        # track entry inputs
        file_path.trace('w',conv_button_update)
        folder_path.trace('w',conv_button_update)
        font_folder_path.trace('w',conv_button_update)
        reference_font_path.trace('w', conv_button_update)

        # when you press X, on_sclosing is passed 
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    
    def browse_file_button(self):
        file_path = filedialog.askopenfilename(title='Select Stimulus Set File')
        #print('********************')
        #print(file_path)
        #print('********************')
        self.selectFile.delete(0,tk.END)
        self.selectFile.insert(0,file_path)

    def browse_reference_font(self):
        reference_font_path = filedialog.askopenfilename(title='Select Reference Font File')
        self.selectReferenceFont.delete(0,tk.END)
        self.selectReferenceFont.insert(0,reference_font_path)        

    def browse_font_folder(self):
        
        font_folder_path = filedialog.askdirectory(title='Select Font Folder')
        #print('********************')
        #print(font_folder_path)
        #print('********************')
        self.selectFontFile.delete(0,tk.END)
        self.selectFontFile.insert(0,font_folder_path)

    ##progress is 0 to 1
    def updateProgressBar(self, prog):
        
        self.progress.set(int(100*prog))
        self.root.update_idletasks()
        pass

    def browse_folder_button(self):
        folder_path = filedialog.askdirectory(title='Select Image Output Folder')
        #print('********************')   
        #print(folder_path)   
        #print('********************')   
        self.selectFolder.delete(0,tk.END)
        self.selectFolder.insert(0,folder_path)

    def on_closing(self):
        if messagebox.askyesno(title = "Quit?", message="Do you really want to quit?"):
            self.root.destroy()

    ## we can start all over if we like
    def conversionComplete(self):
        self.convertButton.config(state='normal')

    def return_values(self):
        if messagebox.askyesno(title = "Initializing Conversion", message="Do you want to start the conversion process?"):
            #print('output from function')
            #print(self.selectFontFile.get())
            #print(self.selectFolder.get())

            # register relevant values into the class object
            self.filepath       = self.selectFile.get()
            self.folderpath     = self.selectFolder.get()
            self.fontfpath      = self.selectFontFile.get()
            self.referencefpath = self.selectReferenceFont.get()
            self.val_pixelsx    = self.pixelsX.get()
            self.val_pixelsy    = self.pixelsY.get()
            self.spacings       = self.spacingEntry.get()
            self.fontExtension  = self.extensionEntry.get()
            self.fontSize       = self.sizeEntry.get()

            #self.selectFontFile.delete(0,tk.END)
            #self.selectFolder.delete(0,tk.END)
            ##self.root.destroy()
            self.convertButton.config(state='disabled')
            ## make a callback instead and disable buttons until we're done
            self.conversionCallback(progressBarUpdate = self.updateProgressBar, finishCallback=self.conversionComplete, interface=self)



