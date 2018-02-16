## Bingyin Hu 20171114
## JSON updating csv file generator
## =============================================================================
## This code generates the csv file required by info_update_master.py and then
## calls info_update_master.py to update xml files.

## =============================================================================
## Input:
## Several prompts will ask users to input what has been updated in the schema.

## =============================================================================
## Output:
## Void. xml files will be changed base on the answers to the prompts by users.

## =============================================================================
import csv
import glob

def schemaInfo():
    xmls = xmlFolder()
    csvDir = raw_input("Please name your output csv file:")
    if (csvDir.strip()[-4:] != ".csv"):
        csvDir = csvDir.strip() + ".csv"
    # do same set of actions to every xml files in xmls
    
    # use a flag to sign when users finish logging in the changes of the schema
    flag = False
    while not flag:
        action = actionPrompt()
        # if user would like to change
        if (action == "change"):
            # csvLine is a dict of lines to be write into the csv file
            csvLine = changeModule()
        # if user would like to add
        if (action == "add"):
            print 1
        # if user would like to remove
        if (action == "remove"):
            print 1
        # if user would like to move
        if (action == "move"):
            print 1
        # if user would like to rename
        if (action == "rename"):
            print 1
        flag = finishPrompt("Finish logging in the updates? (Y/N)")

# A helper method to ask users for the directory of the folder of all xml files
def xmlFolder():
    wd = raw_input("Please type in the directory of the folder containing all xml files:")
    xmls = glob.glob(wd + "/*.xml")
    return xmls
    
# A helper method to ask users for actions
def actionPrompt():
    action = raw_input("What action would you like to take? (change/add/remove/move)")
    while (action.lower() not in ["change", "add", "remove", "move"]):
        print action + " is not avaiable!" 
        action = raw_input("Please select from change, add, remove, or move:")
    return action.lower()    

# A helper method to ask users for key cascades
def keycasPrompt():
    keyCas = raw_input("Please type in the key cascade using '/' to delimit between key levels, example: key_lv1/key_lv2/key_lv3/key_lv4... :")
    # add a function here to check whether the field exists
    
    return keyCas    

# A helper method to determine whether users have finished logging
def finishPrompt(promptString):
    finish = raw_input(promptString)
    finish = finish.strip()
    while (len(finish) != 1):
        finish = raw_input("Please type in a single letter 'Y' or 'N', case-insensitive:")
    if (finish.lower() == "y"):
        return True
    return False

# A helper method to ask users for infos
def infosPrompt():
    infos = raw_input("Please type in the info to be placed in the field:")
    return infos

## Change module
def changeModule():
    csvLine = dict()
    # action column 0
    csvLine["action"] = "change"
    # xml directory column 1 (define outside this function)
    # need a flag to indicate whether user has finished inputing changes
    flag = True
    # key cascades & infos
    keyCasString = ""
    infoString = ""
    while (flag):
        print "==================Path of field to be changed=================="
        keyCasString += "; " + "[" + keycasPrompt() + "]"
        infosString  += "; " + infosPrompt()
        flag = finishPrompt("Finish logging in the changes? (Y/N)")
    csvLine["key cascades"] = keyCasString[1:]
    csvLine["infos"] = infoString[1:]
    csvLine['destination key cascades'] = ""
    return csvLine

schemaInfo()
