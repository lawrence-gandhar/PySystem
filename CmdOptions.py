#**********************************************************************************************
#		Copyright 2014 Lawrence Gandhar

#		Licensed under the Apache License, Version 2.0 (the "License");
#		you may not use this file except in compliance with the License.
#		You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#		 Unless required by applicable law or agreed to in writing, software
#		 distributed under the License is distributed on an "AS IS" BASIS,
#		 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#		 See the License for the specific language governing permissions and
#		 limitations under the License.
#**********************************************************************************************

"""
#===========================================================================
#   				Documentation
#===========================================================================

Class CmdError is for throwing errors
it simply prints errors and exits

Class CmdOptions is for command line arguments
the arguments are put into a list and dictionary
on the basis of key value pairs for (switch and value).

Function Args_check() will check whether the arguments 
provided are valid or not if valid then ListAllArgs() 
function is called which will list all the arguments
into a list as said above.

the function Retlist() is the one which will be used to 
retrive the arguments one by one.   
 
I hope this module may help you and less is powerfull than the 
getopts or the optparser module.. 

=============================================================================
"""

import sys
import Style


class CmdError:
	
	def __init__(self):
		self.style = Style.Style()

	def args_type(self,args):
		return self.style.red("\n%s is not an argument, start it with '-' or '--'\n"%args)
	
	def no_args(self):
		return self.style.red("\nThis is the default mode. Welcome")

	def no_valid_args(self,args,count):
		if count<2:
			a = '\n%s is not a valid argument\n'%args
		else:
			a = '\n%s are not valid arguments\n'%args
		return self.style.red(a)

class CmdOptions:
	def __init__(self,vargs,args):
		
		self.l = []
		self.v = []
		self.d = {}
		self.wrong_args = []
		self.valid_args = vargs
		self.args = args

		self.b = CmdError()	
	
		if len(self.args)>0:
			if not self.args[0].startswith('-') or self.args[0].startswith("--"):
				print self.b.args_type(self.args[0])
			else:	
				self.Args_check()
	
				g,j = self.Valid_Args()	

				if j == False:
					print g
					del self.l[:]		
		else:
			print self.b.no_args()

	def  Args_check(self):
		if not self.args[len(self.args)-1].startswith('-') or self.args[len(self.args)-1].startswith("--"):
			if not self.args[len(self.args)-2].startswith('-') or self.args[len(self.args)-2].startswith("--"):
				print self.b.args_type(self.args[len(self.args)-1])
			else:
				self.ListAllArgs()
		else:
			self.ListAllArgs()


	def ListAllArgs(self):
		for args1 in range(len(self.args)):
			if self.args[args1].startswith("-") or self.args[args1].startswith("--"):
				self.l.append(self.args[args1])
			else:	
				self.l.remove(self.args[args1-1])				
				self.d[self.args[args1-1]] = self.args[args1]
				y = self.d.copy()
				self.d.clear()				
				self.l.append(y)

	def Valid_Args(self):
		for args1 in range(len(self.args)):
			if self.args[args1].startswith("-") or self.args[args1].startswith("--"):
				self.v.append(self.args[args1])

		n = " "
		count = 0
		for a in self.v:
			a = a.split("-")
			if a[1] not in self.valid_args:
				for temp_args in range(len(self.args)):
					if self.args[temp_args]==('-'+a[1]):
						del self.l[:]

				self.wrong_args.append(a[1])
				n = n +(' -'+a[1]);
				x = False
				count = count + 1
			else:
				x= True	
				
		return self.b.no_valid_args(n,count),x			 		

	def RetList(self):
		return self.l

	def WrongList(self):
		return self.wrong_args				
