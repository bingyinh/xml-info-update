## Bingyin Hu 20171115
## XML new field adding main script
## =============================================================================
## This code takes input from the XML update main script (str get from csv)
## and formulates the input of the XML new field adding tool.

## =============================================================================
## Input:   
## Xml file directory, key cascades, and infos to be added. All of these are
## read from a csv file in a master script. Format conventions of the csv file
## see README. see instructions and examples on these methods:
## >>>keyCassParse(xmlDir, keyCassString)
## >>>infosParse(xmlDir, infosString)

## =============================================================================
## Output:
## 1] field to add
##    keyCass: a dict {{xml file 1: [[key cascade], [cascade], [cascade]...]},
##                      xml file 2: [[key cascade], [cascade], [cascade]...]}}
## 2] info to put in the new field, could be an empty string ''
##    infos: a dict {{xml file 1: [info 1, info 2, info 3...]},
##                    xml file 2: [info 1, info 2, info 3...]}}
## The keys of the two dicts are all xml file directories
##
## Example:
## keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Issue',
##                          './/DATA_SOURCE/Citation/CommonFields/AddTest1/AddTest2/AddTest3',
##                          './/MATERIALS/Filler/FillerComponent/ChemicalName/AddTest4']}
## infos = {"test2.xml": ['test issue', '', 'test chemical']}


## =============================================================================
from add_xml_field import singleXmlFieldAdd
# A helper method to parse the string form of key cascades into a list and to
# package it into a dictionary using the xmlDir string as the key. The dict
# looks like the keyCass dict in the example. Within the keyCassString, the keys
# should be separate by "/" within a key cascade. Different key cascades are
# separated by ";".
# string form example:
# '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Issue];
#    [PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/AddTest1/AddTest2/AddTest3];
#    [PolymerNanocomposite/MATERIALS/Filler/FillerComponent/ChemicalName/AddTest4']'''

def keyCassParse(xmlDir, keyCassString):
    # create a blank list for 1d lists of key cascade, V stands for value
    keyCassV = list()
    # separate key cascades
    casStrings = keyCassString.split(";")
    for casString in casStrings:
        # create a blank list for inserting key strings
        keyCas = list()
        # strip blank space and brackets
        casString = casString.strip()
        casString = casString.strip("[")
        casString = casString.strip("]")
        # get rid of the leading "PolymerNanocomposite"
        left = 0
        if (casString.split("/")[0].lower() == "polymernanocomposite"):
            left = (casString.lower().find('polymernanocomposite') +
                    len('polymernanocomposite'))
        casString = casString[left:]
        casString = "./" + casString
        keyCassV.append(casString)
    return {xmlDir: keyCassV}

# A helper method to parse the string form of infos into a 1d list and to
# package it into a dictionary using the xmlDir string as the key. The dict
# looks like the infos dict in the example. Within the infosString, the infos
# should be separate by ";".
# string form example:
# '''test issue; ; test add'''
def infosParse(xmlDir, infosString):
    # create a blank list for 1d lists of infos, V stands for value
    infosV = list()
    # separate key cascades
    infoStrings = infosString.split(";")
    for infoString in infoStrings:
        # strip blank space and brackets
        infoString = infoString.strip()
        infosV.append(infoString)
    return {xmlDir: infosV}

# The main method that reads strings from csv file, converts each xml entry
# into dicts using keyCassParse() and infosParse(), feeds the dicts into add()

def add(xmlDir, keyCassString, infosString, saveDir):
    keyCass = keyCassParse(xmlDir, keyCassString)
    infos = infosParse(xmlDir, infosString)
    singleXmlFieldAdd(xmlDir, keyCass, infos, saveDir)

## Test Code
##xmlDir = "test2.xml"
##keyCassString = '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Issue];[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/AddTest1/AddTest2/AddTest3];  [PolymerNanocomposite/MATERIALS/Filler/FillerComponent/ChemicalName/AddTest4]'''
##infosString = '''test issue; ;test chemical'''
##saveDir = "./test_xml"
##add(xmlDir, keyCassString, infosString, saveDir)
