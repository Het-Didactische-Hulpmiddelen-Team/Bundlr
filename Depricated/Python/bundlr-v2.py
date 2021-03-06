import sys
import os
import re
import shutil
from distutils.dir_util import copy_tree

name = ""
folder = "../examen_vragen/"
outputfile = "xxxxxxxxxxx"
txtfilelocation = "files-v2.txt"

if len(sys.argv) > 1:
    name = sys.argv[1]
    outputfile = name + "_zip_to_upload"
    if(len(sys.argv) > 2):
        txtfilelocation = sys.argv[2]
else:
    exitstr = "\nThis script requires at least 1 parameter:"
    exitstr += "\n   1: Your name, to be used in the zip's name (e.g.: BolaTom)."
    exitstr += "\n   2: (Optional) The .txt file with the names of the files or folders you wish to zip. Defaults to '"+txtfilelocation+"'. More info on this file can be found in the documentation."
    sys.exit(exitstr)
  
filesAndFolders = []
absentFiles = []

# read all lines from txt file
inputt = open(txtfilelocation, 'r')
in_lines = inputt.readlines()
inputt.close()

# process read in lines
for i in range(0, len(in_lines)):
    l = in_lines[i].strip().rstrip("[\r\n]")
    if i == 0:
        folder = l
    else:
        filesAndFolders.append(l)

# printing some info for the user
print("\nCreating a zip file '"+outputfile+"' for '"+name+"' based on the files in '"+folder+"' and the criteria declared in '"+txtfilelocation+"'.")  
   
# process
if not os.path.isdir('temp'): os.mkdir("temp")
def processDir(dirpath):
    for x in filesAndFolders:
        t = os.path.join(dirpath, x)
        p = 'temp/'+x
        if(os.path.exists(t)):
            if os.path.isdir(t):
                copy_tree(t, p)
            elif os.path.isfile(t):
                p2 = re.sub(r"/[^/]*$", "", p)
                if not os.path.exists(p2):
                    os.makedirs(p2)
                if not os.path.exists(p): shutil.copy(t, p)
        else:
            absentFiles.append(x)
        
processDir(folder)

# showing the user what files he is missing
print( "\nYou are missing these files and/or folders:" )
for x in absentFiles:
    print("  -    "+ x)

# zipping the temp folder
print("\nAdding all files to zip file '"+outputfile+"'...")
shutil.make_archive(outputfile, 'zip', "temp/")

# remove the temp folder
print('\nCleaning up temporary files...')
if os.path.exists('temp/'): shutil.rmtree("temp/")

# done
print("\nSUCCESS: Your zip should be created!\n")