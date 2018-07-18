import shutil,os,re,getpass

# This makes sure you're running this from the correct folder
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
thegreatandpowerfuluser = getpass.getuser()
# This checks to make sure we have an input folder to pull files from
if not os.path.exists('Input'):
    print('Hi ' + thegreatandpowerfuluser + ' there isn\'t an input folder... maybe you\'re running this in the wrong folder?')
    quit()

# Defining some folder names
inputdir = path + '\\' + 'Input'
outputdir = 'Output'

def analyse_file_name(fname):
    filePath, coords = os.path.split(fname) # new files are placed/renamed based on prev location and name
    coordsFname = coords[:5] # This will extract the 5 digit file number from each filename
    dirs = filePath.split("\\") # This creates a list of directories that can be used in creating the new file structure
    re_year_1 = re.findall('\((.*?)-', coords) # This will extract the file year from the original file name for type 1
    re_year_2 = re.findall('\((.*?)\)', coords) # This will extract the file year from the original file name for type 1
    re_num = re.findall('-(.*?)\)', coords) # This will extract the file number from the original file name
    print(re_num)
    coordsExt = os.path.splitext(fname) # This extracts the extention from the files
    if not re_year_1:
        fname2 = os.path.join(os.path.join(os.path.join(path, outputdir), str(dirs[-1])), str(dirs[-1]) + '_' + str(*re_year_2) + '_' + coordsFname + coordsExt[1]) # This is the new filename without re_num
    else:
        fname2 = os.path.join(os.path.join(os.path.join(path, outputdir), str(dirs[-1])), str(dirs[-1]) + '_' + str(*re_year_1) + '_' + str(*re_num) + '_' + coordsFname + coordsExt[1]) # This is the new filename with re_num
    print(fname)
    print(fname2)
    if not os.path.exists(os.path.join(os.path.join(path, outputdir), str(dirs[-1]))): # This checks to see if the folders are there
        os.makedirs(os.path.join(os.path.join(path, outputdir), str(dirs[-1]))) # This makes the folders if they aren't
    shutil.copy2(fname, fname2) # The copy function

# This function iterates the above function over the whole filetree in the input folder
count = 0
for root, dirs, files in os.walk(inputdir):
    for name in files:
        fn = os.path.join(root, name)
        analyse_file_name(fn)
        count += 1
        print(count)
