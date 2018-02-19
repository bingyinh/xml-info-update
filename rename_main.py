## Bingyin Hu 20171117
## XML existing field tag renaming main script
## =============================================================================
## This code takes input from the XML update main script (str get from csv)
## and formulates the input of the XML existing field tag renaming tool.

## =============================================================================
## Input:   
## XML file directory, key cascades, and infos to be changed to. All of these
## are read from a csv file in a master script. Format conventions of the csv
## file see README. see instructions and examples on these methods:
## >>>keyCassParse(xmlDir, keyCassString)
## >>>infosParse(xmlDir, infosString)

## =============================================================================
## Output:
## 1] fields to rename
##    keyCass: a dict {{xml file 1: [[key cascade], [cascade], [cascade]...]},
##                      xml file 2: [[key cascade], [cascade], [cascade]...]}}
## 2] the new field tags
##    tags: a dict {{xml file 1: [info 1, info 2, info 3...]},
##                   xml file 2: [info 1, info 2, info 3...]}}
## The keys of the two dicts are all xml file directories
##
## Example:
## keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Title',
##                          './/DATA_SOURCE/Citation/CommonFields/Publisher',
##                          './/MATERIALS/Filler/FillerComponent/ChemicalName']}
## tags = {"test2.xml": ['Title_rename', 'Publisher_rename', 'Chemical_rename']}

## =============================================================================
from rename_xml_tag import singleXmlTagRename
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

# A helper method to parse the string form of tags into a 1d list and to
# package it into a dictionary using the xmlDir string as the key. The dict
# looks like the tags dict in the example. Within the tagsString, the tags
# should be separate by ";".
# string form example:
# '''Title_rename; Publisher_rename; Chemical_rename'''
def tagsParse(xmlDir, tagsString):
    # create a blank list for 1d lists of infos, V stands for value
    tagsV = list()
    # separate key cascades
    tagStrings = tagsString.split(";")
    for tagString in tagStrings:
        # strip blank space and brackets
        tagString = tagString.strip()
        tagsV.append(tagString)
    return {xmlDir: tagsV}

# The main method that reads strings from csv file, converts each xml entry
# into dicts using keyCassParse() and tagsParse(), feeds the dicts into change()

def rename(xmlDir, keyCassString, tagsString):
    keyCass = keyCassParse(xmlDir, keyCassString)
    tags = tagsParse(xmlDir, tagsString)
    singleXmlTagRename(xmlDir, keyCass, tags)
    
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

def testTagsParse():
    xmlDir = "test2.xml"
    tagsString = '''Title_rename; Publisher_rename; Chemical_rename'''
    tags = {"test2.xml": ['Title_rename', 'Publisher_rename', 'Chemical_rename']}
    assert(tags == tagsParse(xmlDir, tagsString))
    print "tagsParse() test passed!"

## Test Code
##testKeyCassParse()
##testTagsParse()
##xmlDir = "test2.xml"
##kcs = '''[PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Title]; [PolymerNanocomposite/DATA_SOURCE/Citation/CommonFields/Publishe]; [PolymerNanocomposite/MATERIALS/Filler/FillerComponent/ChemicalName]'''
##tagsString = '''Title_rename; Publisher_rename; Chemical_rename'''
##saveDir = "./test_xml"
##rename(xmlDir, kcs, tagsString)
