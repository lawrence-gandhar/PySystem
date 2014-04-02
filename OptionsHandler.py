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
#	OptionsHandler Class
#==============================================================================

"""
this class handles all the arguments passed as switches in the statements or
commands.

the only required function to be called by other scripts is the optionsCheck()

"""


import Style

class OptionsHandler:

	def __init__(self):
		self.style = Style.Style()

#==============================================================================================

	def optionsCheck(self,lists,args,note):
		g = []; wrong_list = []; options = {}; rList = {}
		error_raised = False
		gs = False

		for x in args:
			if x == "/?" or x == "?" or x == "-h" or x == "--help":
				if len(args)>1:
					print self.style.red("\tDo not use other switches with Help switch")
					gs = True
				else:
					self.optionsDisplay(lists,note)					
					gs = True

		if gs == False:
			
			for f in range(len(lists.keys())):
				g.append(lists[f][0]);	g.append(lists[f][1])
				
				rList[lists[f][0]] = lists[f][5]	# rlist[-e] = "Required"
				rList[lists[f][1]] = lists[f][5]	# this is to check for values required or not by the switch

			i = 0

			while i < len(args):
				if args[i] in g:
					if self.checkRequired(args[i],rList) is True:	# if required field is set to yes
						if (i+1) < len(args):
							if args[i+1].startswith("-") or args[i+1].startswith("--"):
								print "%s has an invalid value %s" %(args[i],args[i+1])
								error_raised = True
								i += 1
							else:
								if self.ValuePresent(args[i+1]) is False:
									print "%s has a null value" %(args[i])
									error_raised = True
									i += 1
								else:
									options[args[i]] = args[i+1]
									i += 2
						else:
							print "%s values missing" %(args[i])
							error_raised = True
							i += 1 	

					else:				# if required field is set to no
						options[args[i]] = ''
						i +=1	
				else:

					wrong_list.append(args[i])
					i +=1
			optStatus = 1		

			if error_raised is True:
				self.optionsDisplay(lists,'')
				print
			else:
				if len(wrong_list)>0:
				
					if wrong_list[0]=='':
						print self.style.red("\n no switches provided. Atleast use one.. \n")

						self.optionsDisplay(lists,'')
						print
					else:
						wrong_str =""

						for wrong_options in wrong_list:
							wrong_str += wrong_options + " "

						print self.style.red("\n invalid switches ( %s) provided \n" %(wrong_str))

						self.optionsDisplay(lists,'')
						print

					optStatus = 1  	# option has errors
					options.clear()

				else:
					optStatus = 0   # option has no errors

		if gs == True:
			optStatus = 1  	# option has errors
			options.clear()	

		return options,optStatus

#============================================================================

	def optionUsage(self,usage): 
		print " "*2+self.style.bold(usage)	

#===========================================================================

	def optionsDisplay(self,lists,note):
		f = lists.keys()
		
		heading = " "*2+self.style.blue(self.style.bold("Options"))
		heading += " "*15+self.style.blue(self.style.bold("Description"))
		heading += " "*20+self.style.blue(self.style.bold("Usage")) 
		heading += " "*30+self.style.blue(self.style.bold("Required"))
		print heading
		print "_"*110+"\n"		

		for g in f:
			x = lists[g]

			space1 = 15 - (len(x[0])+len(x[1])+2)
			space2 = 30 - len(x[2])
			space3 = 45 - len(x[3])
			
			if x[5]=="required":
				req = "Yes"
			if x[5]=="no":
				req = "No"

			print "["+x[0]+"] ["+x[1]+"]"+" "*space1+x[2]+" "*space2+x[3]+" "*space3+req
		 
		self.show_help_details(note)
		#print

#=========================================================================================

	def checkRequired(self,args,rList):
		f = rList.keys()
		for g in f:
			if args == g:
				if rList[g]=="required":
					return True
					break
				else:
					return False	

#=========================================================================================

	def ValuePresent(self,args):
		f = False

		if len(args)>0:
			f = True
		return f	

#============================================================================================================================
	
	def show_help_details(self,note):
		if len(note)>0:
			print self.style.green(self.style.bold(self.style.underline("\nExamples & Notes")))	
			note = note.replace("\t"," ")
			print note
			
