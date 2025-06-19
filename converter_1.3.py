# get from: https://pypi.org/project/arabic-reshaper/
import arabic_reshaper
import string
import math
import time
import getImageDimensions
from PIL import Image, ImageDraw, ImageFont
from os import chdir, makedirs, path, getcwd
from getTextProperties import getTextProperties
from getStimulusSheet import getStimulusSheet
from converterGUI import MyGUI
# get from: https://pypi.org/project/python-bidi/
from bidi.algorithm import get_display
from getFilesInDir import getFilesInDir


# Function to wrap text
def wrap_text(text, font, kerning, imageDimensions, referenceFont):
    lines               = []
    words               = text.split()
    current_line        = []
    lineOffset         = []
    max_width           = imageDimensions["wrap_width"]
    current_width       = imageDimensions["page_borders"]
    word_width          = []
    for word in words:            
        if applyKerningWithReference:
            word_width = sum(referenceFont.getlength(char) + kerning for char in word) - kerning
            space_width = referenceFont.getlength(' ') + kerning
        else:
            word_width = sum(font.getlength(char) + kerning for char in word) - kerning
            space_width = font.getlength(' ') + kerning

        if current_width + word_width + space_width <= max_width:
            current_line.append(word)
            current_width += word_width + space_width
        else:
            if lines:
                lineOffset.append(max_width-current_width)
            else: 
                lineOffset.append(max_width-current_width+imageDimensions["page_borders"])
            
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width + space_width            

    if current_line:
        lineOffset.append(max_width-current_width)
        lines.append(' '.join(current_line))
        return lines, lineOffset


def create_text_image(text, text_color, trialProperties, sizeAdjustment, imageDimensions, backupProperties, referenceFontPath):

    fontPath = trialProperties["font"]
    fontSize = math.ceil(trialProperties["size"])
    lineSpacing = trialProperties["line_sp"]
    kerning = trialProperties["kerning"]

    image = Image.new('RGB', (imageDimensions["width"], imageDimensions["height"]), 'white')
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(fontPath, round(fontSize * sizeAdjustment))      
    referenceFont =  ImageFont.truetype(referenceFontPath, round(fontSize * sizeAdjustment))
    
    wrappedLines, lineOffset = wrap_text(text, font, kerning, imageDimensions, referenceFont)

    # TODO: Loop through all font conditions, and load in backup fonts for each one 
    if renderLanguage == "arabic":
        currentFont = backupProperties.get_font_name(fontPath)
        currentFontCondition = currentFont[currentFont.rindex('_')+1:]

        for bfonti in backupProperties.font_files:            
            backupFontName = backupProperties.get_font_name(bfonti)
            backupFontCondition = backupFontName[backupFontName.rindex('_')+1:]

            if currentFontCondition == backupFontCondition: 
                backupFontPath = bfonti
                backupFont = ImageFont.truetype(backupFontPath , round(fontSize * sizeAdjustment))
                break

    # line spacing type 
    # currentLineSpacing = charsize * 1.2 * lineSpacing

    # 1 point in line spacing corresponds to %120 of base font size
    currentLineSpacing = fontSize * 1.2 * lineSpacing 

    # Calculate text height getbbox(line)[3] gets the height of that line
    total_height = int(round(sum(font.getbbox(line)[3] + currentLineSpacing for line in wrappedLines) - lineSpacing))

    # find the vertical position (y axis) for the start of paragraph 
    centered_y = imageDimensions["center_y"] - (total_height/4)

    # assign centered vertical position for the starting point of paragraph
    y = centered_y

    if renderLanguage == "arabic":
        # shift baseline towards lower line for latin characters 
        shift_baseline = (abs(backupProperties.get_font_baseline(fontPath) - backupProperties.get_font_baseline(backupFontPath)) * fontSize * sizeAdjustment) / 2
    
        backupFontChars = ''.join([string.ascii_letters, '%()[]\"'])

    for line, offset in zip(wrappedLines, lineOffset):
        if renderLanguage == "arabic":
            line = get_display(line)
            x = offset
        else:
            x = imageDimensions["page_borders"]
                
        for char in line:
            if renderLanguage == "arabic" and (char in backupFontChars):
                print('switched to backup font')
                renderFont = backupFont
                offset_y = shift_baseline
            else:
                renderFont = font
                offset_y = 0
            draw.text((x, y + offset_y), char, font = renderFont, fill=text_color)
            if applyKerningWithReference:
                x += referenceFont.getlength(char) + kerning
            else:
                x += renderFont.getlength(char) + kerning
        # measures each line height for each iteration, decides on Y axis 
        # y += font.getsize(line)[1] * lineSpacing

        # uses a designated character for retrieveing text height (like Y or y, descending chars are preferred)
        # y += charsize * lineSpacing
        y += currentLineSpacing

    return image

# initialize the Readability Tool converter GUI 
renderLanguage = "english" # TODO (mert): add a feature where you can select Latin or Arabic alphabet.

applyKerningWithReference = True
fastLoadTestData = True
fastLoadFolder = "dyslexia"
backupFontPath  = ""
startingPath = ""
startingPath = getcwd() + "\\projects"

def DoAllThings(progressBarUpdate = None, interface=None, finishCallback=None):
    global fastLoadTestData
    global startingPath
    sheetPath = ""
    fontPath = ""
    outputPath = ""

    if startingPath == "":
        startingPath = getcwd() + "\\projects"
        folderExists = path.isdir(startingPath+ "\\"+fastLoadFolder) # TODO (mert): check path for all folders below, and then continue w fast-loading.
        fastLoadTestData = fastLoadTestData and folderExists     

    if fastLoadTestData:
        currentPath = startingPath
        outputPath = currentPath + "\\"+fastLoadFolder+"\\images"
        fontPath = getFilesInDir(currentPath + "\\"+fastLoadFolder+"\\fonts")
        referenceFontPath = [currentPath + "\\"+fastLoadFolder+"\\fonts\\Arial.ttf"]
        sheetPath = currentPath + "\\"+fastLoadFolder+"\\stimulus_set.xlsx"
        
    else:
        outputPath = interface.folderpath
        sheetPath = interface.filepath
        fontPath = getFilesInDir(interface.fontfpath)
        referenceFontPath = interface.referencefpath

    if renderLanguage == "arabic" : 
        backupFontPath = startingPath + "\\"+fastLoadFolder+"\\backupFonts"        
        backupProperties = getTextProperties(font_files = backupFontPath, font_sizes=interface.fontSize, letter_spacings=interface.spacings, lineSpacings="1")

    else:
        backupProperties = None

    fontProperties = getTextProperties(font_files = fontPath, font_sizes=interface.fontSize, letter_spacings=interface.spacings, lineSpacings="1")   

    stimProperties = getStimulusSheet(sheetPath)

    imageDimensions = getImageDimensions.get_dimensions(interface.val_pixelsx, interface.val_pixelsy)

    rowCount = stimProperties.all_trials.shape[0]
    for index, currentTrial in stimProperties.all_trials.iterrows():
        # process text if language is arabic 
        if renderLanguage == "arabic":
            currentTrial["text"] = arabic_reshaper.reshape(currentTrial["text"])        
            
        for fontName in fontProperties.allconditions:
            print('font name', fontName)
            trialProperties = fontProperties.allconditions[fontName]

            adjustmentScalar = fontProperties.get_adjustment_factor(trialProperties["font"], referenceFontPath, 'x')

            print('adjustment scalar', adjustmentScalar)

            print(currentTrial["textid"])
            startTime = time.time()
            image = create_text_image(currentTrial["text"], 
                                    'black',
                                    trialProperties, 
                                    adjustmentScalar,
                                    imageDimensions,
                                    backupProperties,
                                    referenceFontPath)
            
            pathName =  "/".join([outputPath,"_".join([currentTrial["textid"],fontName])]) + ".PNG"

            print ("it took : " + str(time.time()- startTime))

            if not path.isdir(outputPath):
                makedirs(outputPath)
    
            if not outputPath == getcwd():
                chdir(outputPath)

            image.save(pathName)
        progressBarUpdate((index+1)/rowCount)
    finishCallback()


_interface = MyGUI(conversion_callback=DoAllThings, fastLoadTest=fastLoadTestData)