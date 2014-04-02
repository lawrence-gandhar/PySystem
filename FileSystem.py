"""
Copyright 2014 Lawrence Gandhar

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

#==============================================================================
#	File System Class
#==============================================================================

import os,sys
import glob
import Style
import Prompt
import OptionsHandler
from collections import defaultdict
from decimal import *

class FileSystem:
	
	def __init__(self):
		self.style = Style.Style()
		self.options = OptionsHandler.OptionsHandler()
		self.prompt = Prompt.Prompt()
		
		self.dict1 = {}

		self.h = True; self.del_call = False

#============================================================================================================
#""" search command """
#======================================================================================================================================
	def file_searcher(self,args):

		if args == "/?" or args == "?" or args == "-h" or args == "--help":
			print self.style.blue(" "*2+"Usage\n"+'-'*40+"\n"+" "*2+"search <file1>,<file2>")
			print self.style.blue(" "*2+"Search for all files based on the name.\n"+" "*2+"The names are case sensitive.\n")
		else:
			if not args.startswith("-") or args.startswith("--"):
				if args.find(',')!=-1:
					s = args.split(",")
				else:
					s = [args]

				print self.style.blue("\n\tSearching for files. Please Wait")
				print self.style.blue(" "*4 + "="*40)

				self.search_function(s)
			else:
				print self.style.blue(" "*2+"Usage\n"+'-'*40+"\n"+" "*2+"search <file1>,<file2>")
				print self.style.blue(" "*2+"search [?] [/?] [-h] [--help] for help")
				print self.style.blue(" "*2+"Search for all files based on the name.\n"+" "*2+"The names are case sensitive.\n")
		
#=============================================================================================================
#""" search files based on proper name. name is case sensitive irrespective of extension or filetype"""
#======================================================================================================================================
	def search_function(self,s):

		dicta1 = defaultdict(list)		# defaultdic called from collections

		for(rootDir,subDir,files) in os.walk("/"):
	
			for filea in s:	
				j = glob.glob(os.path.join(rootDir,filea))

				for filename in j:
					fullname = os.path.join(rootDir,filename)
					dicta1[filea].append(fullname)
		
		i = 0
		if len(dicta1.keys())>1:
			for keyd in dicta1.keys():
				i += 1
				self.dict1[i] = dicta1[keyd]
				print " %d) %d %s files found" %(i,len(dicta1[keyd]),keyd)

		if len(dicta1.keys())==1:
			for keyd in dicta1.keys():
				i += 1
				self.dict1[i] = dicta1[keyd]
				print "%d %s files found" %(len(dicta1[keyd]),keyd)
				print "="*40

		if self.del_call is True: self.display_del_files()
		else:self.display_files()

#=================================================================================================================
#""" Directory view/listing function. but this traverse all the subdirectories """	
#======================================================================================================================================			
	def dir_traversal(self,args):

		if args == "/?" or args == "?" or args == "-h" or args == "--help":
			print self.style.blue(" "*2+"Usage\n"+'-'*40+"\n"+" "*2+"dir <dirname>")
			print self.style.blue(" "*2+"dir [?] [/?] [-h] [--help] for help")
			print self.style.blue(" "*2+"Directory Listing.")
			print self.style.blue(" "*2+"This will even traverse the subfolders")
			print self.style.blue(" "*2+"Folders are shown in blue and files in yellow")
			print self.style.blue(" "*2+"No values result in listing current working directory")
		else:
			if not args.startswith("-") or args.startswith("--"):

				if len(args)>0:
					args2 = args
				else:
					args2 = os.getcwd()

				if os.path.exists(args2):
					if os.path.isdir(args2):
						for file in os.listdir(args2):
							if os.path.isdir(args2+"/"+file):
								print " "*2+self.style.blue(file)
								self.dir_traversal(args2+"/"+file)
							else:
								print " "*2+self.style.yellow(file)
					else:
						print self.style.errcode('\tis not a directory')	
				else:
					print self.style.errcode('\tpath doesnot exist')
			else:
				print self.style.blue(" "*2+"Usage\n"+'-'*40+"\n"+" "*2+"dir <dirname>")
				print self.style.blue(" "*2+"dir [?] [/?] [-h] [--help] for help")

#=====================================================================================================================
#""" advSearch function for advanced search options"""
#======================================================================================================================================
	def adv_Search(self,args):
		options = {
				0:['-e','--ext','Search based on extension','advSearch -e <.txt>,<.c>,..','string','required'],
				1:['-n','--name','Search based on name','advSearch -n <name1>,<name2>,..','string','required'],
				2:['-f','--fsize','Default Search in Bytes','advSearch -f <size>','integer','required'],
				3:['-fk','--fksize','Default file Search in KB','advSearch -fk <size>','integer','required'],
				4:['-fm','--fmsize','Default file Search in MB','advSearch -fm <size>','integer','required'],
				5:['-fg','--fgsize','Default file Search in GB','advSearch -fg <size>','integer','required'],
				6:['-h','--help','Help for Advance Search','advSearch -h','none','no'],
				7:['?','/?','Help for Advance Search','advSearch ?','none','no']
			  }
		
		note = """
			advSearch [-e][--ext] <.txt>,<.c>,...
				Search for files based on the extension. This will search 
				for the file on all partitions. Name of the file is not 
				required.

			advSearch [-n][--name] <name1>,<name2>,...
				Search for all files based on the name. The names are 
				case sensitive. It does not require extensions to be 
				specified.

			advSearch [-f][--fsize] <100>
				Search for all files based on the filesize less than or 
				equal to 100 Bytes.

			advSearch [-f][--fsize] <30-100>
				Search for all files based on the filesize greater than or 
				equal to 30 and less than equal to 100 Bytes. 

			advSearch [-fk][-fm][-fg] <30-100>
				Search for all files based on the filesize greater than or 
				equal to 30 and less than equal to 100 KB/MB/GB respectively. 

			advSearch [-e] <ext1,ext2>,... [-n] <name1>,<name2>,...
				This will search for the respective files based on names
				and extensions provided. Name is case sensitive.

			advSearch [-e] <ext1,ext2> [-f][--fsize] <100>
				Search for all files based on the extensions and filesize 
				less than or equal to 100 Bytes. You can use any size.	

			advSearch [-n] <name1,name2> [-f][--fsize] <100>
				Search for all files based on the name and filesize 
				less than or equal to 100 Bytes. You can use any size.		

			Do not use the help switches with other switches. If -e, -f or -n
			switch is used then the values should be provided else it will
			show an error.
			
			Use any one switch from -f, -fk, -fm and -fg.
			"""

		fdict = {}; size = {}; self.del_call = False

		optionList,optstatus = self.options.optionsCheck(options,args,note)

		if optstatus == 0 :

			if optionList is not None:
			
				fileList,dd = self.name_ext_filelister(optionList)

				#code for -f switch
			#---------------------------------------------------------------------------
	
				foptlist = ["-f","-fk","-fm","-fg","--fsize","--fksize","--fmsize","--fgsize"]
				
				fcount = 0; fout = ""

				if len(optionList.keys())==1:
					if (optionList.keys()[0]=="-f" or optionList.keys()[0]=="-fk" or
					    optionList.keys()[0]=="-fm" or optionList.keys()[0]=="-fg" or
					    optionList.keys()[0]=="--fsize" or optionList.keys()[0]=="--fksize" or
					    optionList.keys()[0]=="--fmsize" or optionList.keys()[0]=="--fgsize"):
						dd = 4
				
				for fin in foptlist:
					if fin in optionList.keys():
						fcount += 1
						fout = fin
	
				if fcount >= 2:
					print self.style.errcode("\tUse any one switch from -f, -fk, -fm and -fg.")
					print
					self.prompt.run_prompt()

				if fcount == 1:
					fdict,calculate,lower_boundary,upper_boundary = self.filesize_switch(optionList,fout)

			#---------------------------------------------------------------------------

				if len(fdict)>0:	
					size = fdict
				else:
					size = 0

				if dd == 0:
					print
					self.prompt.run_prompt()

				if dd == 1:
					self.dict1.clear()
					print self.style.blue("\n\tSearching for files. Please Wait\n"+" "*4 + "="*40)
					self.search_file_ext(fileList,size)
					
				if dd ==2:
					self.dict1.clear()
					print self.style.blue("\n\tSearching for files. Please Wait\n"+" "*4 + "="*40)
					self.search_files_nm(fileList,size)

				if dd == 3:
					self.dict1.clear()

					if len(fdict)>0:
						print self.style.errcode("Do not use advSearch -e <ext1> -n <name1>,<name2> -f/fk/fm/fg <size>")
						print
					else:	
						print self.style.blue("\n\tSearching for files. Please Wait\n"+" "*4 + "="*40)
						self.search_function(fileList)

				if dd == 4:
					self.dict1.clear()
					banner = "Searching for files "+lower_boundary+" "+calculate+" - "+upper_boundary+" "+calculate+". Please Wait"
					
					print self.style.blue("\n\t"+banner+"\n"+" "*4 + "="*(len(banner)+8))
					self.sized_file_finder(size,calculate)
				
#===============================================================================================================
# filesize switch calculations
#======================================================================================================================================
	def filesize_switch(self,optionList,key):

		fdict = defaultdict(list)
		min_max = optionList[key].split("-")

		if len(min_max)>2:
			print "%s has invalid values %s" %(key,optionList[key])	
			self.options.show_help_details(note)
	
		m = 1
		calculate = 'Bytes'
		lower_boundary = 1
		upper_boundary = 1

		if key=="-fk" or key=="--fksize":
			m = 1024
			calculate = 'KB'
			
		if key=="-fm" or key=="--fmsize":
			m = 1024*1024
			calculate = 'MB'

		if key=="-fg" or key=="--fgsize":
			m = 1024*1024*1024
			calculate = 'GB'

		if len(min_max)==1:
			if min_max[0].isdigit():	
				mini = 0 * m
				maxi = int(min_max[0]) * m
				fdict[key].append(mini)
				fdict[key].append(maxi)
				optionList.pop(key)
				
				lower_boundary = str(1)
				upper_boundary = min_max[0]
			
			else:
				print "%s has invalid values %s" %(key,optionList[key])							
		else:
			mini = min_max[0] 
			maxi = min_max[1] 

			lower_boundary = min_max[0]
			upper_boundary = min_max[1]

			if mini.isdigit() and maxi.isdigit():
				mini = int(mini)* m; maxi = int(maxi)* m 
				if mini > maxi:
					temp = mini
					mini = maxi
					maxi = temp
					fdict[key].append(mini)
					fdict[key].append(maxi)
					optionList.pop(key)
				else:
					fdict[key].append(mini)
					fdict[key].append(maxi)
					optionList.pop(key)
			else:
				print "%s has invalid values %s" %(key,optionList[key])
		return fdict,calculate,lower_boundary,upper_boundary

#===============================================================================================================
#"""put the arguments of the extension and the name switches accordingly into a list for further operations"""
#======================================================================================================================================		
	def name_ext_filelister(self,optionList):

		keys = optionList.keys()
		fileList = []; ext1=[]; name1=[]
	 	searchType = 0
	
		for s in keys:
			if s == "-e" or s == "--ext":
				ext = optionList[s]
				if ext!=" ":						
					if ext.find(',')!="-1":
						ext1 = ext.split(',')
					else:
						ext1 = [ext]
				else:
					ext1 = [" "]
					 	
			if s=="-n" or s =="--name": 
				name = optionList[s]
				if name!=" ":
					if name.find(',')!="-1":
						name1 = name.split(',')
					else:
						name1 = [name]
				else:
					name1 = [" "]
		if len(name1)>0:
			if len(ext1)>0:
				for names in name1:
					if names !=" ":
						for exten in ext1:
							if exten !=" ":
								fileList.append(names+exten)
								searchType = 3
							else:
								searchType = 0
			else:		
				for names in name1:
					if names!=" ":
						fileList.append(names)
						searchType = 2
					else:
						searchType = 0

		elif len(ext1)>0:
			for exten in ext1:
				if exten!=" ":
					fileList.append(exten)
					searchType = 1
				else:
					searchType = 0
				 
		return fileList,searchType
			
#===============================================================================================================
#""" Search for the files in the list provided by the name_ext_filelister() for extension based searches"""
#======================================================================================================================================
	def search_file_ext(self,filelist,size):

		dict1 = defaultdict(list)		# defaultdic called from collections

		gs = False

		if size == 0:
			gs = False
		else:
			key = size.keys()[0]
			
			if len(size[key])==1:
				size_min = 0
				size_max = size[key][0]

			if len(size[key])==2:
				size_min = size[key][0]
				size_max = size[key][1]

			gs = True

		for(rootDir,subDir,files) in os.walk("/"):
			for filename in files:
				for files1 in filelist:
					if filename.endswith(files1):
						fullname = os.path.join(rootDir,filename)
						
						if gs == True:
							if os.path.getsize(fullname)>=int(size_min) and os.path.getsize(fullname)<=int(size_max):
								
								dict1[files1].append(fullname)
						else:	
							dict1[files1].append(fullname)
		 
		i = 0
		
		if len(dict1.keys())>1:
			for keyd in dict1.keys():
				i += 1
				self.dict1[i] = dict1[keyd]
				print " %d) %d %s files found" %(i,len(dict1[keyd]),keyd)

		if len(dict1.keys())==1:
			for keyd in dict1.keys():
				i += 1
				self.dict1[i] = dict1[keyd]
				print "%d %s files found" %(len(dict1[keyd]),keyd)
				print "="*40

		if self.del_call is True: self.display_del_files()
		else:self.display_files()

	
#=====================================================================================================================
#""" Search for the files in the list provided by the name_ext_filelister() for name based searches"""
#======================================================================================================================================
	def search_files_nm(self,filelist,size):

		dict1 = defaultdict(list)		# defaultdic called from collections

		gs = False

		if size == 0:
			gs = False
		else:
			key = size.keys()[0]
			
			if len(size[key])==1:
				size_min = 0
				size_max = size[key][0]

			if len(size[key])==2:
				size_min = size[key][0]
				size_max = size[key][1]

			gs = True

		for(rootDir,subDir,files) in os.walk("/"):
	
			for filea in filelist:	
				j = glob.glob(os.path.join(rootDir,filea))
				f = glob.glob(os.path.join(rootDir,filea+".*"))
		
				for k in j:
					fullname = os.path.join(rootDir,k)
					if gs == True:
						if os.path.getsize(fullname)>=int(size_min) and os.path.getsize(fullname)<=int(size_max):
							dict1[filea].append(k)
					else:
						dict1[filea].append(k)

				for filename in f:
					fullname = os.path.join(rootDir,filename)
					if gs == True:
						if os.path.getsize(fullname)>=int(size_min) and os.path.getsize(fullname)<=int(size_max):
							dict1[filea].append(fullname)
					else:
						dict1[filea].append(fullname)
			
		i = 0
		if len(dict1.keys())>1:
			for keyd in dict1.keys():
				i += 1
				self.dict1[i] = dict1[keyd]
				print " %d) %d %s files found" %(i,len(dict1[keyd]),keyd)

		if len(dict1.keys())==1:
			for keyd in dict1.keys():
				i += 1
				self.dict1[i] = dict1[keyd]
				print "%d %s files found" %(len(dict1[keyd]),keyd)
				print "="*40

		if self.del_call is True: self.display_del_files()
		else:self.display_files()
			

#====================================================================================================================
#""" choosing files to be displayed""
#====================================================================================================================

	def display_files(self):
		
		if len(self.dict1)==1:
			input1 = raw_input(self.style.yellow("Do you want to have a look(y/n): "))

			count_len  = len(self.dict1[1])	

			if input1=="y" or input1=="Y":
				#=================================================================
				# if less than 20 items present
				#=================================================================									

				if count_len <= 20:
					self.less_items(self.dict1[1])

				#=================================================================
				# if more than 20 items present
				#=================================================================
	
				else:
					limit,ret = self.look_limit_setter()
				
					slno = 0; incre = 0; num = limit; run_me = "A"

					if limit==0 and ret==True:
						while incre < count_len:
							slno +=1
							print "%8d) %s"%(slno,self.dict1[1][incre])
							incre +=1

					elif limit>0 and ret==True:
						while incre < limit:
							slno +=1
							print "%8d) %s"%(slno,self.dict1[1][incre])
							incre = incre + 1

						while run_me == "A":
							continu = raw_input(self.style.blue("continue (y/n) : "))
					
							if continu=="y" or continu=="Y":

								limit = limit + num

								if limit > count_len:
									limit = count_len	
			
								while incre < limit:
									slno +=1
									print "%8d) %s"%(slno,self.dict1[1][incre])
									incre = incre + 1

									if incre == count_len:
										print
										run_me = "B"	
							else:
								run_me = "B"
					else:
						print
			else:
				print
				self.prompt.run_prompt()

		#=================================================================
		# if More than 1 list
		#=================================================================

		elif len(self.dict1)>1:
			while True:
				j = raw_input(self.style.yellow("Choose a list (1-n) or press 'n' if you do not want to continue: "))
	
				if j=="n" or j=="N":
					print
					self.prompt.run_prompt()

				elif j.isdigit() is True:
					j = int(j) 

					if j in self.dict1.keys():
						
						count_len  = len(self.dict1[j])	

						#=================================================================
						# if less than 20 items present
						#=================================================================									
						if count_len <= 20:
							self.less_items(self.dict1[j])
							print

						#=================================================================
						# if more than 20 items present
						#=================================================================
				
						else:
							limit,ret = self.look_limit_setter()
							
							slno = 0; incre = 0; num = limit; run_me = "A"

							if limit==0 and ret==True:
								while incre < count_len:
									slno +=1
									print "%8d) %s"%(slno,self.dict1[j][incre])
									incre +=1

							elif limit>0 and ret==True:
								while incre < limit:
									slno +=1
									print "%8d) %s"%(slno,self.dict1[j][incre])
									incre = incre + 1

								while run_me == "A":
									continu = raw_input(self.style.blue("continue (y/n) : "))
					
									if continu=="y" or continu=="Y":

										limit = limit + num

										if limit > count_len:
											limit = count_len	
			
										while incre < limit:
											slno +=1
											print "%8d) %s"%(slno,self.dict1[j][incre])
											incre = incre + 1

											if incre == count_len:
												run_me = "B"
												True	
									else:
										run_me = "B"
										True
							else:
								True

					else:
						print self.style.red("Sorry no such list is present...")
						print
						self.prompt.run_prompt()	
				else:
					print 	
	 	else:
			print self.style.errcode("\t no files found")

#======================================================================================================================================
# Search files based only on their sizes
#======================================================================================================================================

	def sized_file_finder(self,size,calculate):

		list1 = []		# defaultdic called from collections

		gs = False

		if size == 0:
			gs = False
		else:
			key = size.keys()[0]
			
			if len(size[key])==1:
				size_min = 0
				size_max = size[key][0]

			if len(size[key])==2:
				size_min = size[key][0]
				size_max = size[key][1]

			gs = True

		for(rootDir,subDir,files) in os.walk("/"):
			for filename in files:
				fullname = os.path.join(rootDir,filename)
				try:	
					if os.path.getsize(fullname)>=size_min and os.path.getsize(fullname)<=size_max:
						list1.append(fullname)
				except:
					h = ''	

		if len(list1)>0:
			print "%d files found" %len(list1)

			input1 = raw_input(self.style.yellow("Do you want to have a look(y/n): "))
			count_len  = len(list1)	

			if input1=="y" or input1=="Y":
				#=================================================================
				# if less than 20 items present
				#=================================================================									

				if count_len <= 20:
					
					slno = 0; incre = 0;

					while slno < len(list1):
						slno +=1
						print "%8d) %s "%(slno,list1[incre]),

						sizeme = os.path.getsize(list1[incre])
						if calculate =="KB":
							sizeme = Decimal(sizeme)/1024
						if calculate == "MB":
							sizeme = Decimal(sizeme)/(1024*1024)	
						if calculate == "GB":
							sizeme = Decimal(sizeme)/(1024*1024*1024)

						print "(%d %s)"%(sizeme,calculate)
						incre +=1

				#=================================================================
				# if more than 20 items present
				#=================================================================

				else:
					limit,ret = self.look_limit_setter()
				
					slno = 0; incre = 0; num = limit; run_me = "A"

					if limit==0 and ret==True:
						while incre < count_len:
							slno +=1
							print "%8d) %s "%(slno,list1[incre]),

							sizeme = os.path.getsize(list1[incre])
							if calculate =="KB":
								sizeme = Decimal(sizeme)/1024
							if calculate == "MB":
								sizeme = Decimal(sizeme)/(1024*1024)	
							if calculate == "GB":
								sizeme = Decimal(sizeme)/(1024*1024*1024)

							print "(%d %s)"%(sizeme,calculate)
							incre +=1

					elif limit>0 and ret==True:
						while incre < limit:
							slno +=1
							print "%8d) %s "%(slno,list1[incre]),

							sizeme = os.path.getsize(list1[incre])
							if calculate =="KB":
								sizeme = Decimal(sizeme)/1024
							if calculate == "MB":
								sizeme = Decimal(sizeme)/(1024*1024)	
							if calculate == "GB":
								sizeme = Decimal(sizeme)/(1024*1024*1024)

							print "(%d %s)"%(sizeme,calculate)
							incre = incre + 1

						while run_me == "A":
							continu = raw_input(self.style.blue("continue (y/n) : "))
					
							if continu=="y" or continu=="Y":

								limit = limit + num

								if limit > count_len:
									limit = count_len	
			
								while incre < limit:
									slno +=1
									print "%8d) %s "%(slno,list1[incre]),

									sizeme = os.path.getsize(list1[incre])
									if calculate =="KB":
										sizeme = Decimal(sizeme)/1024
									if calculate == "MB":
										sizeme = Decimal(sizeme)/(1024*1024)	
									if calculate == "GB":
										sizeme = Decimal(sizeme)/(1024*1024*1024)
			
									print "(%d %s)"%(sizeme,calculate)
									incre = incre + 1

									if incre == count_len:
										print
										run_me = "B"	
							else:
								run_me = "B"
					else:
						print
			else:
				print
				self.prompt.run_prompt()
		else:
			print self.style.errcode("\t No files found")
			print

#======================================================================================================================================
# Display files based on size 
#======================================================================================================================================

	def delete_file(self,args):		
		options = {
                           0:['-s','--search','Search and delete','del -s <filename1>,<filename2>,..','string','required'],
			   1:['-e','--ext','Search based on extension','del -e <.txt>,<.c>,..','string','required'],
			   2:['-n','--name','Search based on name','del -n <name1>,<name2>,..','string','required'],
			   3:['-a','--all','Delete all searched files','del -s <filename1>,<filename2>,.. -a','none','no'],	
			   4:['-h','--help','Help','del -h','none','no'],			
			   5:['?','/?','Help','del ?','none','no']  
			}

		note = """
			del [-s][--search] <filename1>,<filename2>,..
				Searches for the file in the system and deletes them
				according to the choice of the user. Filename is case
				sensitive.

			del [-e][--ext] <.txt>,<.c>,...

				Search for files based on the extension. This will search
				for the file on all partitions. Name of the file is not 
				required.

			del [-n][--name] <name1>,<name2>,...
				Search for all files based on the name. The names are
				case sensitive. It does not require extensions to be
				specified.

			del [-s][--search] <filename1>,<filename2>,.. [-a][--all]
			del [-e][--ext] <.txt>,<.c>,...... [-a][-all]
			del [-n][--name] <name1>,<name2>,...[-a][-all]
				This will delete all the searched files without asking
				for confirmation. (Avoid these as much as possible)

			Do not use -s switch with other switches except the -a switch
			"""
		
		optionList,optstatus = self.options.optionsCheck(options,args,note)

		delete_All = False; self.del_call = True

		if optstatus ==0 and optionList is not None:

			searchFun = 0

			if len(optionList.keys())==1:
				if optionList.keys()[0]=="-a" or optionList.keys()[0]=="-a":
					print self.style.errcode("Do not use -a/--all alone, use it with -s/-e/-n")
					print self.style.errcode("Use [?] [/?] [-h] [--help] for help\n")
					self.prompt.run_prompt()

			if "-s" in optionList.keys():
				if len(optionList.keys())==1:
					searchFun = 1
				
				elif len(optionList.keys())==2:
					if "--all" in optionList.keys() or "-a" in optionList.keys():
						searchFun = 1	
						print 'paty'
						delete_All = True
					else:
						print self.style.errcode("Do not use -s switch with other switches except the -a switch")
						print self.style.errcode("Use [?] [/?] [-h] [--help] for help\n")
						self.prompt.run_prompt()
				else:
					print self.style.errcode("Do not use -s switch with other switches except the -a switch")
					print self.style.errcode("Use [?] [/?] [-h] [--help] for help\n")
					self.prompt.run_prompt()								
			
			size = 0		

			if searchFun==1:
				print self.style.blue("\n\tSearching for files. Please Wait\n"+" "*4 + "="*40)
				self.search_function(optionList["-s"].split(","))
			else:
				if "--all" in optionList.keys() or "-a" in optionList.keys():
					delete_All = True

				fileList,dd = self.name_ext_filelister(optionList)

				if dd == 1:
					self.dict1.clear()
					print self.style.blue("\n\tSearching for files. Please Wait\n"+" "*4 + "="*40)
					self.search_file_ext(fileList,size)
					
				if dd ==2:
					self.dict1.clear()
					print self.style.blue("\n\tSearching for files. Please Wait\n"+" "*4 + "="*40)
					self.search_files_nm(fileList,size)
					
				if dd == 3:
					self.dict1.clear()
					print self.style.blue("\n\tSearching for files. Please Wait\n"+" "*4 + "="*40)
					self.search_function(fileList)

#====================================================================================================================
#""" choosing files to be displayed""
#======================================================================================================================================

	def display_del_files(self):

		viewed_till_no = 0

		#---------------------------------------------------------------------
		# if only one item was searched 
		#---------------------------------------------------------------------

		if len(self.dict1)==1:
			count = len(self.dict1[1]) 
				
			#---------------------------------------------------------------------
			# if the list contains less than 20 items
			#---------------------------------------------------------------------

			if count<=20:
				self.less_items(self.dict1[1])
				if self.del_confirmer() is True: 
					self.deleter(self.dict1[1])	   # del function				
					print  

			#---------------------------------------------------------------------
			# if the list contains more than 20 items
			#---------------------------------------------------------------------

			else:
				limit,ret = self.look_limit_setter()

				slno = 0 ; incre = 0 ; num = limit; run_me = "A"	
							
				if limit==0 and ret is True:
					while incre < count:
						slno +=1
						print "%8d) %s"%(slno,self.dict1[1][incre])
						incre = incre + 1

					if self.del_confirmer() is True: 
						self.deleter(self.dict1[1],incre)
						print 

				elif limit>0 and ret is True:									
			
					while incre < limit:
						slno +=1
						print "%8d) %s"%(slno,self.dict1[1][incre])
						incre = incre + 1

					while run_me == "A":
						continu = raw_input(self.style.blue("continue (y/n) : "))
					
						if continu=="y" or continu=="Y":

							limit = limit + num

							if limit > count:
								limit = count	
			
							while incre < limit:
								slno +=1
								print "%8d) %s"%(slno,self.dict1[1][incre])
								incre = incre + 1

								if incre == count:
									print	
						else:
							run_me = "B"
							if self.del_confirmer() is True: 
								if self.deleter(self.dict1[1],incre) is True:
									run_me = "A"
				else:print
				
		#---------------------------------------------------------------------
		# if multiple items are searched
		#---------------------------------------------------------------------

		elif len(self.dict1)>1:
			
			while 1:
				choose = raw_input(self.style.yellow("Choose a list (1-n) or press 'n' if you do not want to continue: "))
	
				if choose=="n" or choose=="N":
					print
					self.prompt.run_prompt()

				elif choose.isdigit() is True:
					choose = int(choose) 

					if choose in self.dict1.keys():

						count = len(self.dict1[choose])
						
						#---------------------------------------------------------------------
						# Block 1: if the list contains less than 20 items
						#---------------------------------------------------------------------

						if count<=20:
							self.less_items(self.dict1[choose])
							if self.del_confirmer() is True: 
								self.deleter(self.dict1[choose])
								print 
							

						#---------------------------------------------------------------------
						# Block 2: if the list contains more than 20 items
						#---------------------------------------------------------------------

						else:
							limit,ret = self.look_limit_setter()
							slno = 0 ; incre = 0 ; num = limit; run_me = "A"

							if limit==0 and ret is True:
								while incre < count:
									slno +=1
									print "%8d) %s"%(slno,self.dict1[choose][incre])
									incre = incre + 1

								if self.del_confirmer() is True: 
									self.deleter(self.dict1[choose],incre)
									print 

							elif limit>0 and ret is True:	

								while incre < limit:
									slno +=1
									print "%8d) %s"%(slno,self.dict1[choose][incre])
									incre = incre + 1

								while run_me == "A":
									continu = raw_input(self.style.blue("continue (y/n) : "))
								
									if continu=="y" or continu=="Y":

										limit = limit + num
			
										if limit > count:
											limit = count	
						
										while incre < limit:
											slno +=1
											print "%8d) %s"%(slno,self.dict1[choose][incre])
											incre = incre + 1

											if incre == count:
												print	
									else:
										run_me = "B"
										if self.del_confirmer() is True: 
											if self.deleter(self.dict1[choose],incre) is True:
												run_me = "A"
										else:1
							else:1

					else:
						print self.style.red("Sorry no such list is present...")
						print
						self.prompt.run_prompt()	
				else:
					print	
	 	else:
			print self.style.errcode("\t no files found")
		
#===========================================================================================
# show 20 or less items in delete list
#======================================================================================================================================

	def less_items(self,fileList):

		slno = 0 ; incre = 0; count = len(fileList)

		while slno < count:
			slno +=1
			print "%8d) %s"%(slno,fileList[incre])
			incre += 1	

#============================================================================================
# delete function limit setter
#======================================================================================================================================

	def look_limit_setter(self):

		look = raw_input(self.style.yellow("Do you really want to have a look (y/n): "))
			
		if look == "y" or look == "Y":

			note =" Setting Limit of files displayed will help in proper viewing \n of the file list. Otherwise all the files will be \n displayed at once."
			print self.style.blue(note)

			q = raw_input(self.style.yellow("Set limit of files displayed (y/n) : "))

			if q == "y" or q=="Y":
				limit = raw_input(self.style.yellow("Enter limit : "))

				if limit.isdigit() is True:
					limit = int(limit)

					return limit,True
				else:
					print self.style.red("Sorry its not a digit")	
					print
					self.prompt.run_prompt()
			else:return 0,True
		else:return 0,False
			
#==================================================================================================	
# delete confirmer	
#======================================================================================================================================

	def del_confirmer(self):
		
		del_confirm = raw_input(self.style.yellow("Do you want to delete any item from the list (y/n) :"))
						
		if del_confirm=="y" or del_confirm=="Y":return True
		else:
			if len(self.dict1.keys())>1:
				continu = raw_input(self.style.yellow("Do you want to continue with other lists (y/n) :"))
				if continu=="y" or continu=="Y":return 1
				else:
					print
					self.prompt.run_prompt()

#======================================================================================================
# delete selected items
#======================================================================================================================================

	def deleter(self,fileList,viewed_till_no = 20):

		note ="Please Enter the File Number of the files shown in the list.\n"
		note +="For multiple files to be deleted separate the numbers with a comma.\n"
		note +="Please Avoid spaces\n"	
	
		print self.style.blue(note)

		try:
			get_file_numbers = input(self.style.yellow("Enter the file numbers for shown files to be deleted :"))

			if type(get_file_numbers) is tuple:
				for i in get_file_numbers:
					if i > viewed_till_no: print self.style.red("Select the displayed files only")
					else:self.deleter_extended(i,fileList)	
			else:
				if get_file_numbers > viewed_till_no: print self.style.red("Select the displayed files only")
				else:self.deleter_extended(get_file_numbers,fileList)
		except:		
			print self.style.blue(note)			
					
		return True

#==========================================================================================================
# deleter extended
#======================================================================================================================================

	def deleter_extended(self,i,fileList):
		if (i-1 < 0) or (i-1) >= len(fileList):
			print self.style.red("%8d is not a Valid File Number")%i
		else:	
			try:
				os.remove(fileList[i-1])
				del fileList[i-1]
				print "%8d) %s " %(i,fileList[i-1]),
				print self.style.green("deleted")
			except:
				print "%8d) %s " %(i,fileList[i-1]),
				print self.style.red("cancelled")
			finally:
				return True
