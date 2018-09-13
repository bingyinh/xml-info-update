# xml batch updator

By Bingyin Hu

### 1. System preparations

Required packages:

- shutil
  - Python default package

- os
  - Python default package

- csv
  - Python default package

- glob
  - Python default package

- xml.etree.ElementTree
  - Python default package

- copy
  - Python default package

- string
  - Python default package

- lxml
  - We use this package to validate xml files with xsd schema
  - http://lxml.de/

Open the command or terminal and run
```
pip install -r requirements.txt
```
### 2. How to run

When the xml schema is updated, all existing data entries in NanoMine need to be updated to the latest version of the schema. It will take four steps to do so.

- STEP 1 Download data entries (.xml) from NanoMine as xml files.

- STEP 2 Prepare a csv file (Details see Preparations section)

- STEP 3 Update info in xml files (Details see Actions section)

- STEP 4 Validate the updated xml files (Details see Validation section)

- STEP 5 Upload xml files to database

The scripts of STEP 1 and STEP 5 contain sensitive information and thus are not provided. For STEP 2 through STEP 4, all users need to do is to prepare a single csv file that specifies all the actions required for updating one xml file (see example.csv), and in terminal run 
```
python main.py
```
The script will complete the csv file for all xml files in the given folder, copy and update all xml files in a new folder with the same name of the original xml folder tailed with "\_update", validate the updated xml files with the given xsd schema, and generate an error log.

### 3. Preparations

#### The very first step: CSV file preparation

The update of xml files in batch is accomplished by utilizing a csv file. Each line of the csv file should specifiy one action to be conducted on one specified xml file.

Users need to specify the action in the first column, say "change", "add", "remove", "move", "rename". The second column is for xml file directory. One action can be conducted on several fields within one line in the csv file. This is accomplished via introducing delimiters "/" and ";" in the third and fourth column. To "change", "add", "remove", "move", or "rename" several fields in one xml file all at once, we use ";" to separate these fields in one csv cell. Usually xml files will have a cascade of keys to store infos. Thus we use "/" to separate these keys. The third column is for key cascades delimited by "/" within each change and by ";" between changes. The fourth column is for "change" and "add" actions, which contains infos to be put in the corresponding field specified in the third column. Infos are delimited by ";". The fifth column is the destination key cascades for the action "move".

Example file see example.csv.

For updating of a folder of xml files using the same series of actions, which is usually the case when we update the xsd schema, we can prepare the actions as instructed in the previous paragraphs for just one xml file, and utilize the csv_completor.py to complete the csv file for all the xml files in the specified folder. 

csv_completor.py can be used separatedly or as a function by
``` 
from csv_completor import runcsvCompletor
```
Required inputs are:
1. the directory of the prepared csv file for only one xml file
2. the directory of the folder that contains all the xml files
3. the schema ID (optional, this is a NanoMine data feature, input '' if not used for NanoMine)

The completed csv file will be renamed to the original name tailed with "completed.csv". This script will also automatically duplicate the folder of xml files and rename it to the original folder name tailed with "\_updated". This is for original data backup purpose.

In the following step, the update works will all be done in the "\_updated" folder without making changes to the original xml files.

### 4. Actions (change, add, remove, move, rename)]

#### Change Info in a Field (pass test on 11/15/2017)

1. Prepare a csv file, fill in column 1 with "change", fill in column 2 with the directory of the xml file. In column 3, fill in the key cascade. For example: [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2] Then fill in column 4 with the info corresponding to the fields specified in column 2. For example: info1; info2
2. Run `info_update_master.py` and enter the csv file directory on prompt.
    
#### Add a Field (w/ and w/o info) (pass test on 11/15/2017)

1. Prepare a csv file, fill in column 1 with "add", fill in column 2 with the directory of the xml file. In column 3, fill in the key cascade. For example: [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3] These key cascades should be the field to add into the xml file. Column 4 is for info to add with the new field but it is optional. It can either be left blank, or the corresponding infos with the same order as the key cascades in column 3. For example: info1; ; info3

2. Run `info_update_master.py` and enter the csv file directory on prompt.

#### Remove a Field (pass test on 11/16/2017)

1. Prepare a csv file, fill in column 1 with "remove", fill in column 2 with the directory of the xml file. In column 3, fill in the key cascade. For example: [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3] These key cascades should be the field to be removed in the xml file.

2. Run `info_update_master.py` and enter the csv file directory on prompt.

#### Move a Field (pass test on 02/19/2017)

1. Prepare a csv file, fill in column 1 with "move", fill in column 2 with the directory of the xml file. In column 3, fill in the key cascade. For example: [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3] These key cascades should be the field to be moved in the xml file. Users are recommended to leave column 4 blank. They still can type in whatever they want in the column 4 but our script will ignore it. In column 5, fill in the destination key cascade. They should be the new fields for the specified data to reside. For example: [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3] The last subkey SK in each key cascade stands for the field to be moved, no matter it's a leaf or a parent node. The last subkey in each destination key cascade accordingly stands for the new node to store all the information that used to reside in node SK, i.e. you can name it the same as SK or you can change its tag to something else. Two examples for your intuition:
------------------------------------------------------
From: [PolymerNanocomposite/PROCESSING/MeltMixing/ChooseParameter/Solvent]

To: [PolymerNanocomposite/PROCESSING/MeltMixing/ChooseParameter/Solvent/SolventName]

This will move the string information stored in 'Solvent' to a new field named 'SolventName' under 'Solvent'.

From: [PolymerNanocomposite/MATERIALS/Filler/FillerComposition/mass]

To: [PolymerNanocomposite/MATERIALS/Filler/FillerComposition/Fraction/mass]

This will move the double information stored in 'mass' to a new field named 'mass' under a new field 'Fraction'.

2. Run `info_update_master.py` and enter the csv file directory on prompt.

#### Rename a Field Tag (pass test on 11/17/2017)

1. Prepare a csv file, fill in column 1 with "rename", fill in column 2 with the directory of the xml file. In column 3, fill in the key cascade. For example: [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3] These key cascades should be the field to be renamed in the xml file. Then fill in column 4 with the new tags corresponding to the fields specified in column 2. For example: newtag1; newtag2

2. Run `info_update_master.py` and enter the csv file directory on prompt.

### 5. Validation

When the xml files are updated, a call will be made to `xml_update_validator.py` to validate the updated xml files with the given schema. An error log will be exported in csv format.