## Bingyin Hu 20171116
## XML existing field removing tool
## =============================================================================
## This code removes existing fields specified by the user in the designiated
## xml file.

## =============================================================================
## Input:   
## 1] field to remove
##    keyCass: a dict {{xml file 1: [[key cascade], [cascade], [cascade]...]},
##                      xml file 2: [[key cascade], [cascade], [cascade]...]}}
## The keys of the dict are all xml file directories
## 2] a directory for saving the modified xml files

## =============================================================================
## Output:
## Void, but the xml file will be updated

## =============================================================================
import xml.etree.ElementTree as ET

# The function to remove fields in several xml files in a batch
def batchXmlFieldRemove(keyCass):
    for xmlDir in keyCass:
        singleXmlFieldRemove(xmlDir, keyCass)

# The function to find the first correctly matched fields with specified child
def findMyParent(tree, path, childTag):
    if tree.find(path) is None:
        # .find() finds the first match, if it's None then there isn't a match
        return None
    else:
        parents = tree.findall(path)
        for parent in parents:
            for child in list(parent):
                if child.tag == childTag:
                    return parent
    return None

# A function that help remove first empty field in an xml tree
def pinpointEmpty(tree):
    end = False
    while not end:
        end = True
        for field in tree.iter():
            # if we detect an empty field
            # print field
            if len(list(field)) == 0 and field.text is None:
                field.tag = "RRREEEMMOOOVVVEEEMMMEEE" # rename its tag
                treeStr = ET.tostring(tree.getroot()) # transform to string
                treeStr = treeStr.replace('<RRREEEMMOOOVVVEEEMMMEEE>', '') # remove leading tag
                treeStr = treeStr.replace('</RRREEEMMOOOVVVEEEMMMEEE>', '') # remove following tag
                treeStr = treeStr.replace('<RRREEEMMOOOVVVEEEMMMEEE />', '') # remove unpaired tag
                tree._setroot(ET.fromstring(treeStr)) # transform back to xml tree
                end = False
                break
    return tree
        
# The function to remove several fields in a single xml file
def singleXmlFieldRemove(xmlDir, keyCass):
    tree = ET.parse(xmlDir)
    root = tree.getroot()
    # unpack the two dicts keyCass and infos
    keylist = keyCass[xmlDir]
    for x in xrange(len(keylist)):
        keyCas = keylist[x].split("/")
        pathExist = "./" # use this variable to keep track of our path
        parentPath = '' # use this variable to keep track of the path of the parent node of the field to be removed
        # First find out whether the field to be removed exists
        # a flag for field existence
        exist = True
        for y in xrange(2, len(keyCas)):
            if (tree.find(pathExist + "/" + keyCas[y]) is None):
                # print '"' + pathExist + "/" + keyCas[y] + '"'
                # print "This field does not exist. No moving done. Please check!"
                exist = False
                break
            else:
                # last node then remove
                if (y == len(keyCas) - 1):
                    # find the parent node of the field to remove
                    parentPath = pathExist
                pathExist = pathExist + "/" + keyCas[y]
        # Now we have constructed the path of move-from field, let's find out
        # the occurrence of them in the xml
        occur = len(tree.findall(pathExist))
        if not exist:
            occur = 0
        # print tree.findall(pathExist)
        for field in xrange(occur): # If occur is 0, we won't enter the loop
            parent = findMyParent(tree, parentPath, keyCas[-1])
            child = tree.find(parentPath + "/" + keyCas[-1])
            # call remove(subfield)
            if parent is not None:
                parent.remove(child)
    # END OF THE LOOP
    # Final check of empty fields
    tree = pinpointEmpty(tree)
    # newXmlDir = saveDir + "/" + xmlDir.split("/")[-1]
    # tree.write(newXmlDir)
    tree.write(xmlDir, encoding="UTF-8", xml_declaration=True)

    
## Test code
##xmlDir = "test2.xml"
##keyCass = {"test2.xml": ['.//DATA_SOURCE/Citation/CommonFields',
##                         './/DATA_SOURCE/Citation/CommonFields/AddTest1/AddTest2/AddTest3',
##                         './/MATERIALS/Filler/FillerComponent/ChemicalName']}
##saveDir = "./test_xml"
##singleXmlFieldRemove(xmlDir, keyCass, saveDir)
