
# import pandas for reading from excel file 

import pandas as pd

class getStimulusSheet:

    def __init__(self,sheet_path):
        """
        Creates a class for handling stimulus sheet

        :param sheet_path: Path of the stimulus sheet
        """
        self.sheet_path = sheet_path
        
        if (self.sheet_path[len(self.sheet_path)-1] == 'x'):
            self.sheet_data = pd.read_excel(self.sheet_path)
        else:
            self.sheet_data = pd.read_csv(self.sheet_path)
        
        self.all_trials = self.__generate_trials(self)


    def item_count(self,textVar):
        """
        Returns the numbers typed at the end of a string as integers 

        Used for extracting screen count for passages

        :param textVar: String input with numbers at the end. 
        """
        count1 = int(textVar[len(textVar)-1])
        count2 = textVar[len(textVar)-2].isnumeric() # check if second character from last if a number (indicates two digit number)
        #print(count2)
        if count2:
            # if there is more than 9 items get last two characters for counting how many items there are
            itemCount = textVar[len(textVar)-2] + textVar[len(textVar)-1]
            itemCount = int(itemCount)        
        else:
            itemCount = count1

        #print('item count of: ',textVar, itemCount)
        return itemCount
    

    def get_passage_info(self,current_trial):
        """
        Returns passage information contained in trialProperties header of stimulus sheet.
        
        :param current_trial: A row of pandas data frame extracted from stimulus sheet.
        """        
        # get the contents of trialproperties 
        trialProperties = current_trial["trialproperties"]
        # #print('trial properties', trialProperties)
        # split it into components 
        trialProperties = trialProperties.split(';')

        return trialProperties[0]
    

    def passage_count(self,current_trial):
        """
        Returns the passage screen counts specified in "trialProperties" header of the stimulus sheet.

        :param current_trial: A row of the stimulus sheet representing a trial.
        """
        textVar = self.get_passage_info(current_trial)

        return self.item_count(textVar)


    
    def get_text(self,current_trial):
        """
        Returns header labels of passage texts contained in stimulus sheet.
        These labels are then used for getting the text.

        :param current_trial: A row of the stimulus sheet representing a trial.
        """
        # get passage count for this trial (count means how many screens that this passage will be shown in)
        howManyScreens  = self.passage_count(current_trial)

        # #print('size of excel sheet',shape(passage_sheet))
        ## PASSAGE SHEET VARIABLES ##
        id_columns = []
        text_columns = []
        for i in range(1,howManyScreens+1):
            id_columns.append("pas"+str(i)+"ID")
            text_columns.append("pas"+str(i)+"text")

        return dict(zip(id_columns,text_columns))
    @staticmethod
    def __generate_trials(self):
        alltrials = pd.DataFrame({})
        for index, currentTrial in self.sheet_data.iterrows():
            
            textDict =  self.get_text(currentTrial)

            for currentID in textDict:
                currentFrame = pd.DataFrame({
                    "setID": [currentTrial["setID"]],
                    "type" : [currentTrial["trialType"]],
                    "textid" : [currentTrial[currentID]],
                    "text": currentTrial[[textDict[currentID]]],
                })
                alltrials = pd.concat([alltrials, currentFrame],ignore_index=True)
            
        return alltrials