from PIL import Image, ImageDraw, ImageFont
from getFilesInDir import getFilesInDir

import getImageDimensions
from os import chdir, makedirs, path, getcwd
from getTextProperties import getTextProperties
from getStimulusSheet import getStimulusSheet
from converterGUI import MyGUI

from bidi.algorithm import get_display
import arabic_reshaper
import string

import math
import time

def create_text_image(text, text_color, font_path, initial_font_size, line_spacing, kerning, size_adjustment, imageDimensions, backupFontProperties):
    # Function to wrap text
    def wrap_text(text, font, imageDimensions):
        lines               = []
        words               = text.split()
        current_line        = []
        line_offset       = []
        max_width           = imageDimensions["wrap_width"] 
        current_width       = imageDimensions["page_borders"]       
        word_width          = []
        for word in words:            
            word_width = sum(font.getlength(char) + kerning for char in word) - kerning
            space_width = font.getlength(' ') + kerning
            if current_width + word_width + space_width <= max_width:
                current_line.append(word)
                current_width += word_width + space_width
            else:
                if lines:
                    line_offset.append(max_width-current_width)
                else: 
                    line_offset.append(max_width-current_width+imageDimensions["page_borders"])
                
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width + space_width            

        if current_line:
            line_offset.append(max_width-current_width)
            lines.append(' '.join(current_line))


            return lines, line_offset
    
    # TODO: Loop through all font conditions, and load in backup fonts for each one 
    if renderLanguage == "arabic":
        current_font = backupFontProperties.get_font_name(font_path)
        current_font_condition = current_font[current_font.rindex('_')+1:]

        for backup_fonti in backupFontProperties.font_files:            
            backup_font_name = backupFontProperties.get_font_name(backup_fonti)
            backup_font_condition = backup_font_name[backup_font_name.rindex('_')+1:]
            print(backup_fonti)
            print(backup_font_condition)    
            if current_font_condition == backup_font_condition:
                backup_font_path = backup_fonti
                break

    
    font = ImageFont.truetype(font_path, round(initial_font_size * size_adjustment))   
    backup_font = ImageFont.truetype(backup_font_path , round(initial_font_size * size_adjustment))
    wrapped_lines, line_offset = wrap_text(text, font, imageDimensions)

    # Create an image with white background
    image = Image.new('RGB', (imageDimensions["width"], imageDimensions["height"]), 'white')
    draw = ImageDraw.Draw(image)
    # charsize = font.getsize(testChars)[1]

    # line spacing type 
    # current_line_spacing = charsize * 1.2 * line_spacing

    # 1 point in line spacing corresponds to %120 of base font size
    current_line_spacing = initial_font_size * 1.2 * line_spacing 

    # Calculate text height getbbox(line)[3] gets the height of that line
    total_height = int(round(sum(font.getbbox(line)[3] + current_line_spacing for line in wrapped_lines) - line_spacing))

    # find the vertical position (y axis) for the start of paragraph 
    centered_y = imageDimensions["center_y"] - (total_height/4)

    # assign centered vertical position for the starting point of paragraph
    y = centered_y

    # shift baseline towards lower line for latin characters 
    shift_baseline = (abs(backupFontProperties.get_font_baseline(font_path) - backupFontProperties.get_font_baseline(backup_font_path)) * initial_font_size * size_adjustment) / 2
    
    backup_font_chars = ''.join([string.ascii_letters, '()[]\"'])
    for line,offset in zip(wrapped_lines,line_offset):
        if renderLanguage == "arabic":
            line = get_display(line)
            x = offset
        else:
            x = imageDimensions["page_borders"]
                
        for char in line:
            if char in backup_font_chars:
                print('switched to backup font')
                render_font = backup_font
                offset_y = shift_baseline
            else:
                render_font = font
                offset_y = 0
            draw.text((x, y + offset_y), char, font=render_font, fill=text_color)
            x += render_font.getlength(char) + kerning
        # measures each line height for each iteration, decides on Y axis 
        # y += font.getsize(line)[1] * line_spacing

        # uses a designated character for retrieveing text height (like Y or y, descending chars are preferred)
        # y += charsize * line_spacing
        y += current_line_spacing

    return image



# initialize the Readability Tool converter GUI 

renderLanguage = "arabic" # TODO (mert): add a feature where you can select Latin or Arabic alphabet.
fastLoadTestData = True
fastLoadFolder = "arabic"
backup_font_path  = ""
startingPath = ""

def DoAllThings(progressBarUpdate = None, interface=None, finishCallback=None):
    global fastLoadTestData
    global startingPath
    sheetPath = ""
    fontPath = ""
    output_path = ""
    if startingPath == "":
        startingPath = getcwd() + "\\projects"
        folderExists = path.isdir(startingPath+ "\\"+fastLoadFolder) # TODO (mert): check path for all folders below, and then continue w fast-loading.
        fastLoadTestData = fastLoadTestData and folderExists     
    if fastLoadTestData:
        currentPath = startingPath
        output_path = currentPath + "\\"+fastLoadFolder+"\\images"
        fontPath = currentPath + "\\"+fastLoadFolder+"\\fonts"
        backup_font_path = currentPath + "\\"+fastLoadFolder+"\\backup_fonts"
        sheetPath = currentPath + "\\"+fastLoadFolder+"\\stimulus_set.xlsx"
        pass
    else:
        output_path = interface.folderpath
        sheetPath = interface.filepath
        fontPath = interface.fontfpath

    print(interface.fontSize)
    print(type(interface.fontSize))

    # get font files
    allfonts = getFilesInDir(fontPath)
    allBackupFonts = getFilesInDir(backup_font_path)

    backupFontProperties = getTextProperties(font_files = allBackupFonts, font_sizes=interface.fontSize, letter_spacings=interface.spacings, line_spacings="1")

    fontProperties = getTextProperties(font_files=allfonts, font_sizes=interface.fontSize, letter_spacings=interface.spacings, line_spacings="1")

    stimProperties = getStimulusSheet(sheetPath)

    imageDimensions = getImageDimensions.get_dimensions(interface.val_pixelsx, interface.val_pixelsy)

    rowCount = stimProperties.all_trials.shape[0]
    for index, currentTrial in stimProperties.all_trials.iterrows():
        # process text if language is arabic 
        if renderLanguage == "arabic":
            currentTrial["text"] = arabic_reshaper.reshape(currentTrial["text"])        
            
        for fontName in fontProperties.allconditions:
            print('font name', fontName)
            currentCondition = fontProperties.allconditions[fontName]

            adjustment_scalar = 1 #fontProperties.get_adjustment_factor(currentCondition["font"])

            print(currentTrial["textid"])
            startTime = time.time()
            image = create_text_image(currentTrial["text"], 
                                    'black',
                                    currentCondition["font"], 
                                    math.ceil(currentCondition["size"]), 
                                    currentCondition["line_sp"], 
                                    currentCondition["kerning"], 
                                    adjustment_scalar,
                                    imageDimensions,
                                    backupFontProperties)
            
            pathName =  "/".join([output_path,"_".join([currentTrial["textid"],fontName])]) + ".PNG"

            print ("it took : " + str(time.time()- startTime))

            if not path.isdir(output_path):
                makedirs(output_path)
    
            if not output_path == getcwd():
                chdir(output_path)

            image.save(pathName)
        progressBarUpdate((index+1)/rowCount)
    finishCallback()


_interface = MyGUI(conversion_callback=DoAllThings, fastLoadTest=fastLoadTestData)