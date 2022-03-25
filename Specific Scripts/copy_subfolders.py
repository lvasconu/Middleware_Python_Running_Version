import os
import shutil
import stat
from distutils.dir_util import copy_tree

# Folder with files to be evaluated:
source = 'G:\\ad71117f-20df-41a4-979c-f58c458d33c2'
destination = 'C:\\Users\\adm.ga\\Desktop'

os.chdir(source)										# Ref: https://www.tutorialspoint.com/python3/os_walk.htm

# Terms to be searched. Ref: https://stackoverflow.com/questions/3389574/check-if-multiple-strings-exist-in-another-string
# Since Milestone uses GUIDs (e.g. "0106d8c0-d848-4814-98f4-342e9fa1cd1c"), names (e.g. "Sony SNC-VB6xx/VM6xx/EM6xx Series (10.19.207.4) - Camera 1 - 2021-05-14") are not found.
matches = [
			'config.xml'
		   ]

print('Started')

for root, _, _ in os.walk('.', topdown = True):
	
	print(root)

	# Criteria:
	if any(x in root for x in matches):					# If any string in 'matches' is in 'root'. Ref: https://www.afternerd.com/blog/python-string-contains/

		copy_tree(source + '\\' + root, destination+ '\\' + root) # https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth

	
print('Finished')