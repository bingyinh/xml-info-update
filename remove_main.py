## Bingyin Hu 20171116
## XML existing field removing main script
## =============================================================================
## This code takes input from the XML update main script (str get from csv)
## and formulates the input of the XML existing field removing tool.

## =============================================================================
## Input:
## Xml file directory and key cascades to be removed. All of these are read
## from a csv file in a master script. Format conventions of the csv file
## see README. see instructions and examples on these methods:
## >>>keyCassParse(xmlDir, keyCassString)

## =============================================================================
## Output:
## 1] field to remove
##    keyCass: a dict {{xml file 1: [[key cascade], [cascade], [cascade]...]},
##                      xml file 2: [[key cascade], [cascade], [cascade]...]}}
## The keys of the dict are all xml file directories
##
## Example:
## keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Title',
##                          './/DATA_SOURCE/Citation/CommonFields/Publisher',
##                          './/MATERIALS/Filler/FillerComponent/ChemicalName']}

## =============================================================================
from remove_xml_field import singleXmlFieldRemove
# A helper method to parse the string form of key cascades into a 1d list and
# to package it into a dictionary using the xmlDir string as the key. The dict
# looks like the keyCass dict in the example. Within the keyCassString, the keys
# should be separate by "/" within a key cascade. Different key cascades are
# separated by ";".
# string form example:
# '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Volume];
#    [PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Corresponding Author]'''

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

# The main method that reads strings from csv file, converts each xml entry
# into dicts using keyCassParse(), feeds the dicts into remove()

def remove(xmlDir, keyCassString):
    keyCass = keyCassParse(xmlDir, keyCassString)
    singleXmlFieldRemove(xmlDir, keyCass)

## Test Code
##xmlDir = "test2.xml"
##keyCassString = '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields]; [PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/AddTest1/AddTest2/AddTest3]; [Polymernanocomposite/MATERIALS/Filler/FillerComponent/ChemicalName]'''
##saveDir = "./test_xml"
##remove(xmlDir, keyCassString)
