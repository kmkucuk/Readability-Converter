
from fontTools.ttLib import TTFont

arial_font = TTFont('Arial.ttf')
opendys_font = TTFont('OpenDyslexic.ttf')

a = 0 



class getTextProperties():

    def __init__(self,font_files,font_sizes,letter_spacings,line_spacings):
        """
        Creates a class with all text properties like fonts (font files),
        font sizes, letter spacings, line spacings. These parameters can be 
        further processed using the methods embedded in this class

        :param font_files: A list of font file paths.

        :param font_sizes: The requested sizes for fonts, in pixels.
        :param letter_spacings: A list of letter spacing values in em units, separated by commas
                            (e.g. -0.05,0,0,05)
        :param line_spacings: A list of line spacing values in ratio units, separated by commas
                            (e.g. 1, 1.2, 1.5)
        """
        self.font_files = font_files
        self.font_sizes = self.__get_font_sizes(font_sizes)
        self.letter_spacings = self.__get_letter_spacing(letter_spacings)
        self.line_spacings = self.__get_line_spacing(line_spacings)
        self.allconditions = self.__generate_conditions(self)

    @staticmethod
    def __get_font_sizes(font_sizes):
        """
        Returns two lists containing standardized font size labels, 
        and respective font size values (in px). 

        Raises an error if no size was entered
        
        """
        
        if isinstance(font_sizes, (int, float)):
            font_sizes = str(font_sizes)

        try:
            # split size values by commas
            size_vector = font_sizes.split(',')            

        except AttributeError:
            raise AttributeError('Incorrect input type for font size, enter comma separated string values: ', font_sizes, type(font_sizes))

        size_names = []
        # if there are any size values
        if len(size_vector)>1:    
            # sort these values
            size_vector.sort()
            for k in range(0,len(size_vector)):
                # create a vector of font size levels (e.g. fsz1, fsz2, fsz3) for image name generation
                size_names.append("_fsz"+str(k+1))
                size_vector[k] = round(float(size_vector[k]))
        elif len(size_vector)==1:
            # if there is only 1 font size, do not register level of font size on image file names
            size_names = ["undefined"]
            if len(size_vector[0]) == 0:
            # if no size was entered in the GUI raise an error 
                raise Exception("Please enter a valid font size")                
            else:
            # use the single size value specified in GUI
                size_vector[0] = round(float(size_vector[0]))

       
        return dict(zip(size_names,size_vector))


    @staticmethod
    def __get_letter_spacing(letter_spacings):
        """
        Returns two lists containing standardized letter spacing labels, 
        and respective letter spacing values in float type. 

        Returns empty list of spacing names if there is only one spacing value entered.
        
        """

        if isinstance(letter_spacings, (int, float)):
            letter_spacings = str(letter_spacings)

        try:
            # split spacing values by commas
            kerning_vector = letter_spacings.split(',')

        except AttributeError:
            raise AttributeError('Incorrect input type for letter spacing, enter comma separated string values: ', letter_spacings, type(letter_spacings))
        kerning_names = []
        # if there are any spacing values
        if len(kerning_vector)>1:    
            # sort these values
            kerning_vector.sort()
            for k in range(0,len(kerning_vector)):
                # create a vector of spacing levels (e.g. sp1, sp2, sp3) for image name generation
                kerning_names.append("_sp"+str(k+1))
                kerning_vector[k] = float(kerning_vector[k])
        elif len(kerning_vector)==1:
            # if there is only 1 spacing, do not register level of spacing on image file names
            kerning_names = ["undefined"]
            if len(kerning_vector[0]) == 0:
            # if no spacings were specified, only use 0 spacing
            # leave the spacing name empty in this case        
                kerning_vector = [0.00]
            else:
            # use the spacing value specified in the GUI
                kerning_vector[0] = float(kerning_vector[0])


        return dict(zip(kerning_names,kerning_vector))
   

    @staticmethod
    def __get_line_spacing(line_spacings):
        """
        Returns two lists containing standardized line spacing labels, 
        and respective line spacing values in float type. 

        Returns empty list of line spacing names if there is only one spacing value entered.
        
        """

        if isinstance(line_spacings, (int, float)) :
            line_spacings = str(line_spacings)

        # split spacing values by commas
        line_spacing_vector = line_spacings.split(',')

        try:
            # split size values by commas
            line_spacing_vector = line_spacings.split(',')            
            
        except AttributeError:
            raise AttributeError('Incorrect input type for line spacing, enter comma separated string values: ', line_spacings, type(line_spacings))
                
        line_spacing_names = []
        # if there are any spacing values
        if len(line_spacing_vector)>1:    
            # sort these values
            line_spacing_vector.sort()
            for k in range(0,len(line_spacing_vector)):
                # create a vector of spacing levels (e.g. fsz1, fsz2, fsz3) 
                # for image name generation
                line_spacing_names.append("lnsp"+str(k+1))
                line_spacing_vector[k] = float(line_spacing_vector[k])
        elif len(line_spacing_vector)==1:
            # if there is only 1 spacing, do not register level of spacing 
            # on image file names
            line_spacing_names = ["undefined"]
            if len(line_spacing_vector[0]) == 0:
            # if no spacings were specified, only use 0 spacing
            # leave the spacing name empty in this case        
                line_spacing_vector = [1.2]
            else:
            # use the spacing value specified in the GUI
                line_spacing_vector[0] = float(line_spacing_vector[0])
        
        return dict(zip(line_spacing_names,line_spacing_vector))


    def get_glyph_height(self, font_path, character):
        """
        Get height of a character using fonttools library

        Returns a character height value, it should be multiplied by the font size 
        to get the exact pixel value of that character's height.        
        
        """
        # Load the font
        font = TTFont(font_path)

        if 'glyf' in font:
            glyfTableTag = 'glyf'
        elif 'CFF ' in font:
            glyfTableTag = 'CFF'
        elif 'CFF2' in font:
            glyfTableTag = 'CFF2'
        else:            
            raise KeyError('Font file does not have a glyf table!')
        
        # Get the units per em
        units_per_em = font['head'].unitsPerEm

        # Get the glyph name for the character
        glyph_name = font.getBestCmap().get(ord(character))
        if not glyph_name:
            print(f"Character '{character}' not found in the font.")
            return

        # Get the glyph
        glyph = font[glyfTableTag][glyph_name]

        # Calculate the height of the glyph
        if glyph.isComposite():
            print(f"Character '{character}' is a composite glyph, height calculation may not be accurate.")
            return 



        height = (glyph.yMax - glyph.yMin) / units_per_em
        return height
    
    def get_adjustment_factor(self,target_font,reference_font,character):
        """
        Returns ratio of the reference to target font character height
        """    
        adjustment_ratio = self.get_glyph_height(reference_font,character) / self.get_glyph_height(target_font,character)
        return adjustment_ratio

    def get_font_baseline(self, font_path):
        # Load the font file
        font = TTFont(font_path)
        
        # Access the 'OS/2' table (Windows Metrics)
        os2_table = font["OS/2"]

        # Get the units per em
        units_per_em = font['head'].unitsPerEm

        # Extract baseline information
        baseline = (os2_table.sTypoAscender - os2_table.sTypoDescender) / units_per_em
        
        print(f"Font Baseline (Ascender - Descender): {baseline}")
        print(f"Ascender: {os2_table.sTypoAscender}, Descender: {os2_table.sTypoDescender}")
        
        return baseline
    
    def get_font_name(self,font_path):
        """
        Strips a path string from its parent directory and file extension. 
        Returns a string only with the file name.

        :param font_path: A string of font file path.
        """        

        try:
            # check if there is a file extension
            font_path = font_path[font_path.rindex('\\')+1:font_path.rindex('.')]
            return font_path
        except (IndexError, ValueError) as err:
            print(err)
            print(font_path)
            raise err("File path either does not have a parent path or does not include a file extension:")
            
        
    @staticmethod
    def __generate_conditions(self):
        allconditions = {}

        for fonti in self.font_files:
            fontName = self.get_font_name(fonti)

            for sizeName in self.font_sizes:

                for letterName in self.letter_spacings:

                    for lineName in self.line_spacings:
                        condName = ("".join(
                                [fontName,
                                letterName,
                                lineName, 
                                sizeName]
                                )).replace('undefined','')
                        
                        allconditions[condName] =  {
                                                    "font": fonti,
                                                    "size": self.font_sizes[sizeName],
                                                    "kerning": self.letter_spacings[letterName],
                                                    "line_sp": self.line_spacings[lineName]
                                                }

        return allconditions


        
        
