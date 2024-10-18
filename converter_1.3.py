from PIL import Image, ImageDraw, ImageFont
from getFilesInDir import getFilesInDir

import getImageDimensions
from os import chdir, makedirs, path, getcwd
from getTextProperties import getTextProperties
from getStimulusSheet import getStimulusSheet
from converterGUI import MyGUI

import math

def create_text_image(text, text_color, font_path, initial_font_size, line_spacing, kerning, size_adjustment, imageDimensions):
    # Function to wrap text
    def wrap_text(text, font, imageDimensions):
        lines               = []
        words               = text.split()
        current_line        = []
        max_width           = imageDimensions["wrap_width"] 
        current_width       = imageDimensions["page_borders"]       

        for word in words:
            word_width = sum(font.getlength(char) + kerning for char in word) - kerning
            space_width = font.getlength(' ') + kerning
            if current_width + word_width + space_width <= max_width:
                current_line.append(word)
                current_width += word_width + space_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width + space_width

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    font = ImageFont.truetype(font_path, round(initial_font_size * size_adjustment))
    wrapped_lines = wrap_text(text, font, imageDimensions)

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

    for line in wrapped_lines:
        x = imageDimensions["page_borders"]        
        for char in line:


            draw.text((x, y), char, font=font, fill=text_color)
            x += font.getlength(char) + kerning
        # measures each line height for each iteration, decides on Y axis 
        # y += font.getsize(line)[1] * line_spacing

        # uses a designated character for retrieveing text height (like Y or y, descending chars are preferred)
        # y += charsize * line_spacing
        y += current_line_spacing

    return image



# initialize the Readability Tool converter GUI 
interface = MyGUI()

print(interface.fontSize)
print(type(interface.fontSize))

# get font files
allfonts = getFilesInDir(interface.fontfpath)

textprops_small = getTextProperties(font_files=allfonts, font_sizes=interface.fontSize, letter_spacings=interface.spacings, line_spacings="1")

stim_props = getStimulusSheet(interface.filepath)

imageDimensions = getImageDimensions.get_dimensions(interface.val_pixelsx, interface.val_pixelsy)

output_path = interface.folderpath

for index, currentTrial in stim_props.all_trials.iterrows():

    for fontName in textprops_small.allconditions:
        print('font name', fontName)
        currentCondition = textprops_small.allconditions[fontName]
        adjustment_scalar = textprops_small.get_adjustment_factor(currentCondition["font"])
        print(currentTrial["textid"])        
        image = create_text_image(currentTrial["text"], 
                                  'black',
                                  currentCondition["font"], 
                                  math.ceil(currentCondition["size"]), 
                                  currentCondition["line_sp"], 
                                  currentCondition["kerning"], 
                                  adjustment_scalar,
                                  imageDimensions)
        pathName =  "/".join([output_path,"_".join([currentTrial["textid"],fontName])]) + ".PNG"

        if not path.isdir(output_path):
            makedirs(output_path)
 
        if not output_path == getcwd():
            chdir(output_path)

        image.save(pathName)



