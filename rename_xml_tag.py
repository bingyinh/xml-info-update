## Bingyin Hu 20171117
## XML existing field tag renaming tool
## =============================================================================
## This code updates the designiated xml file with renamed tags specified by
## the user.

## =============================================================================
## Input:
## 1] fields to rename
##    keyCass: a dict {{xml file 1: [[key cascade], [cascade], [cascade]...]},
##                      xml file 2: [[key cascade], [cascade], [cascade]...]}}
## 2] the new field tags
##    tags: a dict {{xml file 1: [info 1, info 2, info 3...]},
##                   xml file 2: [info 1, info 2, info 3...]}}
## The keys of the two dicts are all xml file directories
## 3] a directory for saving the modified xml files

## =============================================================================
## Output:
## Void, but the xml file will be updated

## =============================================================================
import xml.etree.ElementTree as ET

# The function to rename tags in several xml files in a batch
def batchXmlTagRename(keyCass, tags):
    for xmlDir in keyCass: # equivalent to "for (xmlDir in tags):"
        singleXmlTagRename(xmlDir, keyCass, tags)
        
# The function to rename tags in several fields in a single xml file
def singleXmlTagRename(xmlDir, keyCass, tags):
    tree = ET.parse(xmlDir)
    root = tree.getroot()
    # unpack the two dicts keyCass and tags
    keylist = keyCass[xmlDir]
    taglist = tags[xmlDir]
    assert(len(keylist) == len(taglist))
    for x in xrange(len(keylist)):
        if (tree.find(keylist[x]) is None):
            # print '"' + keylist[x] + '"'
            # print "This field does not exist. No rename done. Please check!"
            continue
        else:
            tree.find(keylist[x]).tag = taglist[x]
    # newXmlDir = saveDir + "/" + xmlDir.split("/")[-1]
    # tree.write(newXmlDir)
    tree.write(xmlDir, encoding="UTF-8", xml_declaration=True)

## Test codes    
##xmlDir = "test2.xml"
##keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields/Title',
##                         './/DATA_SOURCE/Citation/CommonFields/Publisher',
##                         './/MATERIALS/Filler/FillerComponent/ChemicalName']}
##tags = {"test2.xml": ['Title_rename', 'Publisher_rename', 'Chemical_rename']}
##saveDir = "./test_xml"
##singleXmlTagRename(xmlDir, keyCass, tags, saveDir)
