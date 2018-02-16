## Bingyin Hu 20171115
## XML existing field info changing main script
## =============================================================================
## This code takes input from the XML update main script (str get from csv)
## and formulates the input of the XML existing field info changing tool.

## =============================================================================
## Input:   
## XML file directory, key cascades, and infos to be changed to. All of these
## are read from a csv file in a master script. Format conventions of the csv
## file see README. see instructions and examples on these methods:
## >>>keyCassParse(xmlDir, keyCassString)
## >>>infosParse(xmlDir, infosString)

## =============================================================================
## Output:
## 1] field to update
##    keyCass: a dict {{xml file 1: [[key cascade], [cascade], [cascade]...]},
##                      xml file 2: [[key cascade], [cascade], [cascade]...]}}
## 2] updated info to put in the field
##    infos: a dict {{xml file 1: [info 1, info 2, info 3...]},
##                    xml file 2: [info 1, info 2, info 3...]}}
## The keys of the two dicts are all xml file directories
##
## Example:
## keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Title',
##                          './/DATA_SOURCE/Citation/CommonFields/Publisher',
##                          './/MATERIALS/Filler/FillerComponent/ChemicalName']}
## infos = {"test2.xml": ['test title', 'test publisher', 'test chemical']}

## =============================================================================
from change_xml_info import singleXmlInfoUpdate
# A helper method to parse the string form of key cascades into a list and to
# package it into a dictionary using the xmlDir string as the key. The dict
# looks like the keyCass dict in the example. Within the keyCassString, the keys
# should be separate by "/" within a key cascade. Different key cascades are
# separated by ";".
# string form example:
# '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Title];
#    [PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Publisher];
#    [PolymerNanocomposite/MATERIALS/Filler/FillerComponent/ChemicalName]'''

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
# '''test title; test publisher; test chemical'''
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
# into dicts using keyCassParse() and infosParse(), feeds the dicts into change()

def change(xmlDir, keyCassString, infosString, saveDir):
    keyCass = keyCassParse(xmlDir, keyCassString)
    infos = infosParse(xmlDir, infosString)
    singleXmlInfoUpdate(xmlDir, keyCass, infos, saveDir)
    
## Test Cases
def testKeyCassParse():
    xmlDir = "test2.xml"
    kcs = '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Title]; [PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Publisher]; [PolymerNanocomposite/MATERIALS/Filler/FillerComponent/ChemicalName]'''
    keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Title',
                             './/DATA_SOURCE/Citation/CommonFields/Publisher',
                             './/MATERIALS/Filler/FillerComponent/ChemicalName'
                             ]
              }
    assert(keyCass == keyCassParse(xmlDir, kcs))
    print "keyCassParse() test passed!"

def testInfosParse():
    xmlDir = "test2.xml"
    infosString = '''test title; test publisher; test chemical'''
    infos = {"test2.xml": ['test title', 'test publisher', 'test chemical']}
    assert(infos == infosParse(xmlDir, infosString))
    print "infosParse() test passed!"
##    
##testKeyCassParse()
##testInfosParse()
##xmlDir = "test2.xml"
##kcs = '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Title]; [PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Publishe]; [PolymerNanocomposite/MATERIALS/Filler/FillerComponent/ChemicalName]'''
##infosString = '''test title; test publisher; test chemical'''
##saveDir = "./test_xml"
##change(xmlDir, kcs, infosString, saveDir)
