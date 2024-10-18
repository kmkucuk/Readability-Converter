# get image dimensions

def round_for_image(value):
    return int(round(float(value)))

def get_dimensions(x_pixels,y_pixels):
    # resize scalar
    resize_scalar=1

    # intialize image dictionary
    image_dimensions = {}    
    
    # Obtain image dimensions (width, height, center positions)
    image_dimensions["width"]           = round_for_image(x_pixels) * resize_scalar
    image_dimensions["height"]          = round_for_image(y_pixels) * resize_scalar 
    image_dimensions["center_x"]        = round_for_image(image_dimensions["width"] / 2)
    image_dimensions["center_y"]        = round_for_image(image_dimensions["height"] / 2) 

    # left - right indent of text (%2.5 for each side)
    image_dimensions["page_borders"]    = round_for_image(image_dimensions["width"] /40) 

    # length of text wrapping
    image_dimensions["wrap_width"]       = round_for_image(image_dimensions["width"] - image_dimensions["page_borders"]*2) 

    # top - bottom indent
    image_dimensions["wrap_height"]      = round_for_image(image_dimensions["height"]  - image_dimensions["height"] /20) 

    return image_dimensions


