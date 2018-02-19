## Bingyin Hu 20171116
## XML existing field moving main script
## =============================================================================
## This code takes input from the XML update main script (str get from csv)
## and formulates the input of the XML existing field moving tool.

## =============================================================================
## Input:   
## Xml file directory, key cascades, and destination key cascades. All of these
## are read from a csv file in a master script. Format conventions of the csv
## file see README. see instructions and examples on these methods:
## >>>keyCassParse(xmlDir, keyCassString)

## =============================================================================
## Output:
## 1] field to move from
##    keyCassFrom: a dict {{xml file 1: [[key cascade], [cascade]...]},
##                          xml file 2: [[key cascade], [cascade]...]}}
## 2] field to move to
##    keyCassTo: a dict {{xml file 1: [[key cascade], [cascade]...]},
##                        xml file 2: [[key cascade], [cascade]...]}}
## The keys of the two dicts are all xml file directories
##
## Example:
## keyCassFrom = {"test2.xml": [['PolymerNanocomposite','DATA_SOURCE',
##                               'Citation','CommonFields','Title'],
##                              ['PolymerNanocomposite','DATA_SOURCE',
##                               'Citation','CommonFields','FieldNotExists'],
##                              ['PolymerNanocomposite','DATA_SOURCE',
##                               'Citation','CommonFields']]}
## keyCassFrom = {"test2.xml": [['PolymerNanocomposite','DATA_SOURCE'],
##                              ['PolymerNanocomposite','DATA_SOURCE'],
##                              ['PolymerNanocomposite','MATERIALS','NewField']]}
## =============================================================================
from move_xml_field import singleXmlFieldMove
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
# into dicts using keyCassParse() and infosParse(), feeds the dicts into add()

def move(xmlDir, keyCassFromString, keyCassToString):
    keyCassFrom = keyCassParse(xmlDir, keyCassFromString)
    keyCassTo = keyCassParse(xmlDir, keyCassToString)
    singleXmlFieldMove(xmlDir, keyCassFrom, keyCassTo)

## Test Code
##xmlDir = "test2.xml"
##keyCassFromString = '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Title]; [PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/FieldNotExist/AddTest2/AddTest3]; [Polymernanocomposite/DATA_SOURCE/Citation/CommonFields]'''
##keyCassToString = '''[PolymerNanocomposite/DATA_SOURCE]; [PolymerNanocomposite/DATA_SOURCE]; [Polymernanocomposite/MATERIALS/NewField]'''
##saveDir = "./test_xml"
##move(xmlDir, keyCassFromString, keyCassToString)
