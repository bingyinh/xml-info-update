## Bingyin Hu 20171117
## XML updating master script
## =============================================================================
## This code asks for the csv file that contains all the actions required by the
## user and conduct those actions accordingly by calling the tools.

## =============================================================================
## Input:   
## A prompt will ask for the directory of the csv file. The format of the csv
## file please refer to README.txt.

## =============================================================================
## Output:
## Void. xml files will be changed according to the actions specified in the
## csv file.

## =============================================================================
import csv
import os
from change_main import change
from add_main import add
from remove_main import remove
from move_main import move
from rename_main import rename
# A function that takes in the directory of csv, reads through it, and take
# actions as required.
def actionCenter(csvDir, saveDir):
    with open(csvDir, "rt") as infile:
        for row in csv.DictReader(infile):
            if (row['action'] == 'change'):
                callChange(row, saveDir)
            elif (row['action'] == 'add'):
                callAdd(row, saveDir)
            elif (row['action'] == 'remove'):
                callRemove(row, saveDir)
            elif (row['action'] == 'move'):
                callMove(row, saveDir)
            elif (row['action'] == 'rename'):
                callRename(row, saveDir)

# A helper method that takes in a row from the csv reader that specifies to
# "change" in the action column and calls the existing field info changing tool.
def callChange(row, saveDir):
    # first assert whether the row in csv has everything in the right place
    assert(row['xml directory'] != '')
    assert(row['key cascades'] != '')
    assert(row['infos'] != '')
    assert(row['destination key cascades'] == '')
    change(row['xml directory'], row['key cascades'], row['infos'], saveDir)

# A helper method that takes in a row from the csv reader that specifies to
# "add" in the action column and calls the field adding tool.
def callAdd(row, saveDir):
    # first assert whether the row in csv has everything in the right place
    assert(row['xml directory'] != '')
    assert(row['key cascades'] != '')
    assert(row['destination key cascades'] == '')
    add(row['xml directory'], row['key cascades'], row['infos'], saveDir)
    
# A helper method that takes in a row from the csv reader that specifies to
# "remove" in the action column and calls the field removing tool.
def callRemove(row, saveDir):
    # first assert whether the row in csv has everything in the right place
    assert(row['xml directory'] != '')
    assert(row['key cascades'] != '')
    assert(row['infos'] == '')
    assert(row['destination key cascades'] == '')
    remove(row['xml directory'], row['key cascades'], saveDir)

# A helper method that takes in a row from the csv reader that specifies to
# "move" in the action column and calls the existing field moving tool.
def callMove(row, saveDir):
    # first assert whether the row in csv has everything in the right place
    assert(row['xml directory'] != '')
    assert(row['key cascades'] != '')
    assert(row['infos'] == '')
    assert(row['destination key cascades'] != '')
    move(row['xml directory'], row['key cascades'],
         row['destination key cascades'], saveDir)

# A helper method that takes in a row from the csv reader that specifies to
# "change" in the action column and calls the existing field tag renaming tool.
def callRename(row, saveDir):
    # first assert whether the row in csv has everything in the right place
    assert(row['xml directory'] != '')
    assert(row['key cascades'] != '')
    assert(row['infos'] != '')
    assert(row['destination key cascades'] == '')
    rename(row['xml directory'], row['key cascades'], row['infos'], saveDir)
    
def run_info_update(csvDir, saveDir):
    if not os.path.exists(saveDir):
        print '"' + saveDir + '"' + "does not exist but has been created."
        os.makedirs(os.getcwd() + "/" + saveDir)
    actionCenter(csvDir, saveDir)
    
if __name__ == "__main__":
##    csvDir = raw_input("Please type in the directory of the csv file:")
##    while csvDir == "":
##        csvDir = raw_input("Please type in the directory of the csv file:")
##    saveDir = raw_input("Where would you like your updated xml files saved?")
##    while saveDir == "":
##        saveDir = raw_input("Where would you like your updated xml files saved?")
    csvDir = "E:/Dropbox/DIBBS/data_update/info_update_xml/schema/042917to010918test.csv"
    saveDir = "E:/Dropbox/DIBBS/data_update/info_update_xml/schema"
    run_info_update(csvDir, saveDir)
