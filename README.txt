When the xml schema is updated, all existing data entries in NanoMine need to be updated
to the latest version of the schema. It will take three steps to do so.

    STEP 1 Download data entries (.xml) from NanoMine as json files.
    >>> get_data.py
    STEP 2 Update info in xml files
    >>> Details see Actions section
    STEP 3 Upload xml files to database
    >>> upload_to_db.py


Actions (change, add, remove, move, rename)

>>> The very first step: CSV file preparation
    The update of json files in batch is accomplished by utilizing a csv file. Each line
    of the csv file should specifiy one action to be conducted on one specified xml
    file.

    Users need to specify the action in the first column, say "change", "add", "remove",
    or "move". The second column is for xml file directory. One action can be conducted
    on several fields within one line in the csv file. This is accomplished via
    introducing delimiters "/" and ";" in the third and fourth column. To "change", 
    "add", "remove", or "move" several fields in one xml file all at once, we use ";"
    to separate these fields in one csv cell. Usually xml files will have a cascade of
    keys to store infos. Thus we use "/" to separate these keys. The third column is for
    key cascades delimited by "/" within each change and by ";" between changes. The
    fourth column is for "change" and "add" actions, which contains infos to be put in
    the corresponding field specified in the third column. Infos are delimited by ";". 
    The fifth column is the destination key cascades for the action "move".

    Example file see xml_update.csv.

>>> Change Info in a Field (pass test on 11/15/2017)
    1) Prepare a csv file, fill in column 1 with "change", fill in column 2 with the 
       directory of the xml file. In column 3, fill in the key cascade. For example: 
       [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]
       Then fill in column 4 with the info corresponding to the fields specified in
       column 2. For example:
       info1; info2
    2) Run info_update_master.py and enter the csv file directory on prompt.
    
>>> Add a Field (w/ and w/o info) (pass test on 11/15/2017)
    1) Prepare a csv file, fill in column 1 with "add", fill in column 2 with the 
       directory of the xml file. In column 3, fill in the key cascade. For example: 
       [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3]
       These key cascades should be the field to add into the xml file. Column 4 is
       for info to add with the new field but it is optional. It can either be left
       blank, or the corresponding infos with the same order as the key cascades in
       column 3. For example:
       info1; ; info3
    2) Run info_update_master.py and enter the csv file directory on prompt.

>>> Remove a Field (pass test on 11/16/2017)
    1) Prepare a csv file, fill in column 1 with "remove", fill in column 2 with the 
       directory of the xml file. In column 3, fill in the key cascade. For example: 
       [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3]
       These key cascades should be the field to be removed in the xml file.
    2) Run info_update_master.py and enter the csv file directory on prompt.

>>> Move a Field (pass test on 11/17/2017)
    1) Prepare a csv file, fill in column 1 with "move", fill in column 2 with the 
       directory of the xml file. In column 3, fill in the key cascade. For example: 
       [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3]
       These key cascades should be the field to be moved in the xml file. Users are
       recommended to leave column 4 blank. They still can type in whatever they want
       in the column 4 but our script will ignore it. In column 5, fill in the
       destination key cascade. They should be the new fields for the specified data
       to reside. For example: 
       [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3]
       The last subkey SK in each key cascade stands for the field to be moved, no matter
       it's a leaf or a parent node. The last subkey in each destination key cascade
       accordingly stands for the new node to store all the information that used to
       reside in node SK, i.e. you can name it the same as SK or you can change its tag
       to something else. Two examples for your intuition:
       ------------------------------------------------------------------------------------
       From: [PolymerNanocomposite/PROCESSING/MeltMixing/ChooseParameter/Solvent]
       To: [PolymerNanocomposite/PROCESSING/MeltMixing/ChooseParameter/Solvent/SolventName]
       This will move the string information stored in 'Solvent' to a new field named
       'SolventName' under 'Solvent'.
       ------------------------------------------------------------------------------------
       From: [PolymerNanocomposite/MATERIALS/Filler/FillerComposition/mass]
       To: [PolymerNanocomposite/MATERIALS/Filler/FillerComposition/Fraction/mass]
       This will move the double information stored in 'mass' to a new field named 'mass'
       under a new field 'Fraction'.
       ------------------------------------------------------------------------------------
    2) Run info_update_master.py and enter the csv file directory on prompt.


>>> Rename a Field Tag (pass test on 11/17/2017)
    1) Prepare a csv file, fill in column 1 with "rename", fill in column 2 with the 
       directory of the xml file. In column 3, fill in the key cascade. For example: 
       [key1/subkey1/subsubkey1]; [key2/subkey2/subsubkey2]; [key3/subkey3]
       These key cascades should be the field to be renamed in the xml file. Then fill
       in column 4 with the new tags corresponding to the fields specified in
       column 2. For example:
       newtag1; newtag2
    2) Run info_update_master.py and enter the csv file directory on prompt.


