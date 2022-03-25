# To have permission to delete folders, run cmd or PowerShell as admin.

import os
import shutil
import stat
import datetime
import schedule
import time

def __init__():
	pass

# Variables.
dir_delete				= 'G:\\f372b92c-0f83-404f-bb2e-03409e995146'				# Folder with subfolders to be deleted.
retain_days				= 15														# Will delete subfolder older than this amount of days.
matches					= ['2020', '2021-01', '2021-02', '2021-03', '2021-04']		# Terms to be searched. Ref: https://stackoverflow.com/questions/3389574/check-if-multiple-strings-exist-in-another-string
path_log_general		= 'C:\\Users\\adm.ga\\Desktop\\log_general.txt'				# Path to general log.
path_log_deleted		= 'C:\\Users\\adm.ga\\Desktop\\log_deleted.txt'				# Path to log with deleted folders.
path_log_not_deleted	= 'C:\\Users\\adm.ga\\Desktop\\log_not_delete.txt'			# Path to log with folders that were not deleted.

def test():
	print('Test: ' + str(datetime.datetime.now()))

# In case of remove error:
def on_rm_error(func, path, exc_info):		# Ref: https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
											# 'path' contains the path of the file that couldn't be removed let's just assume that it's read-only and unlink it.
	os.chmod(path, stat.S_IWRITE)			# Changes the mode of file/folder in path to "Write by owner". Ref: https://www.tutorialspoint.com/python/os_chmod.htm
	#os.unlink(path) # Threw error.

def scan_and_remove():
	# Creating/acessing log files. Ref: https://www.guru99.com/reading-and-writing-files-in-python.html
	#log_general = open(path_log_general,'w+')									
	#log_deleted = open(path_log_deleted,'w+')									
	#log_not_deleted = open(path_log_not_deleted,'w+')

	# Logging:
	log_general = open(path_log_general,'a+')
	log_general.write(str(datetime.datetime.now()) + ': Started scan and remove.' + '\n')
	log_general.close()
	print(str(datetime.datetime.now()) + ': Started scan and remove.')

	# Going to directory. Ref: https://www.tutorialspoint.com/python3/os_walk.htm
	os.chdir(dir_delete)														

	# Adding specific days to 'matches', from [today - 90 days] to [today - retain_days]:
	day = datetime.date.today() - datetime.timedelta(90)
	while day < datetime.date.today() - datetime.timedelta(retain_days):
		matches.append(str(day))
		day = day + datetime.timedelta(1)
	print(matches)

	# Logging:
	log_general = open(path_log_general,'a+')
	log_general.write(str(datetime.datetime.now()) + ': Strings to be searched: ' + str(matches) + '\n')
	log_general.close()

	# Starting scan and removal procedure:
	for root, _, _ in os.walk('.', topdown = True):
	
		print(str(datetime.datetime.now()) + ': ' + root)
		#a = input('a:' )

		# If any string of 'matches' is in 'root'. Ref: https://www.afternerd.com/blog/python-string-contains/
		if any(x in root for x in matches):					

			# Removing folder. On error, calls method on_rm_error(). Refs:
			#	https://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty
			#	https://stackoverflow.com/questions/4829043/how-to-remove-read-only-attrib-directory-with-python-in-windows
			shutil.rmtree(root, onerror = on_rm_error)
		
			# Logging:
			log_deleted = open(path_log_deleted,'a+')
			log_deleted.write(str(datetime.datetime.now()) + ': ' + root + '\n')
			log_deleted.close()

			#print('Deleting: ' + root)
		else:
			# Logging:
			log_not_deleted = open(path_log_not_deleted,'a+')
			log_not_deleted.write(str(datetime.datetime.now()) + ': ' +root + '\n')
			log_not_deleted.close()
		
		#print('Subfolders: ' + str(dirs))
		#print(files)

	# Logging:
	log_general = open(path_log_general,'a+')
	log_general.write(str(datetime.datetime.now()) + ': Finished scan and remove.' + '\n')
	log_general.close()
	print(str(datetime.datetime.now()) + ': Finished scan and remove.')

# Running 1st time:
scan_and_remove()

# Schedule to run from time to time. https://www.youtube.com/watch?v=zwIGxcDxS5o
schedule.every(1).day.do(scan_and_remove)
#schedule.every(1).second.do(test)

# Watching pending activities.
while True:
	print(str(datetime.datetime.now()) + ': Watching pending activities.')
	schedule.run_pending()
	time.sleep(60)
	#time.sleep(1)


