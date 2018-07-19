import shutil,os,re

# Get "Home path" from where the Python file lives, set Dropbox path using it.
home_path = os.path.expanduser("~")
project_path = os.path.join(home_path, 'Dropbox', 'LegislationRA')
os.chdir(project_path)

# Assumes your Dropbox/Project lives in:
# ... C://Users/YOURNAME/Dropbox/Project,
# ... if not, set it accordingly,
# data_path = os.path.join('THEPATHWHEREDROPBOXLIVES','Dropbox')

# Defining some folder names
inputdata_path = os.path.join(project_path, 'Input')
outputdata_path = os.path.join(project_path, 'Output')

# This checks to make sure we have an input folder to pull files from
if not os.path.exists(inputdata_path):
    warning_message = 'Cannot find input data path {0!s}'.format(inputdata_path)
    print(warning_message)
    exit(1)

# Inner function for the loop:
def analyse_file_name(inputfilename):

    print(inputfilename)

    file_path, filenameonly = os.path.split(inputfilename) # new files are placed/renamed based on prev location and name
    filename_numbers = filenameonly[:5] # This will extract the 5 digit file number from each filename
    filename_extension = os.path.splitext(filenameonly)[1] # This extracts the extension from the files
    file_host, subpath = os.path.split(file_path) # This creates directories that can be used in creating a new file structure

    re_year_1 = re.findall('\((.*?)-', filenameonly) # This will extract the file year from the original file name for type 1
    re_year_2 = re.findall('\((.*?)\)', filenameonly) # This will extract the file year from the original file name for type 2
    re_num = re.findall('-(.*?)\)', filenameonly) # This will extract the file number from the original file name
    print(re_num)

    if not re_year_1:
        # This is the new filename without re_num
        new_filenameonly = "%s_%s_%s%s" % (subpath, str(*re_year_2), filename_numbers, filename_extension)
    else:
        # This is the new filename with re_num
        new_filenameonly = "%s_%s_%s_%s%s" % (subpath, str(*re_year_1), str(*re_num), filename_numbers, filename_extension)

    # Creating new full output path from main output path + subpath:
    output_path = os.path.join(outputdata_path, subpath)

    # This checks to see if output folders are there,
    if not os.path.exists(output_path):
        # This makes the folders if they aren't
        os.makedirs(output_path)

    # Now create full output filename:
    outputfilename = os.path.join(output_path, new_filenameonly)
    print(outputfilename)

    # Copy input file to new output filename:
    shutil.copy2(inputfilename, outputfilename)

# This function iterates the above function over the whole filetree in the input folder
count = 0
for root, dirs, files in os.walk(inputdata_path):
    for name in files:
        if name.endswith('.pdf'):
                fullfilename = os.path.join(root, name)
                analyse_file_name(fullfilename)
                count += 1
                print(count)
