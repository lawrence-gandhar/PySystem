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

import sys,os
import commands
import Style
import Prompt


class Security:

	def __init__(self):

		self.style = Style.Style()
		self.prompt = Prompt.Prompt()

#=====================================================================================================
#	Shellcode String Generator
#=====================================================================================================

	def ShellcodeGenerator(self,file_d):

		if len(file_d)==0:
			print self.style.blue("\tUSAGE : shellcode <full path of the executable>\n")
		else:
			if not os.path.exists(file_d):
				print self.style.red('\t path not found\n')
				self.prompt.run_prompt()	
		
			comm = commands.getoutput("objdump -d "+file_d)

			tempf = open("temp.dump","w")
			tempf.write(comm)
			tempf.close()

			f = open("temp.dump","r")
			x = f.readlines()

			opcodes = ""
			for f1 in x:
				j = f1.split("\t")
				if len(j)>1:
					gg = j[1].replace(" ",'')
					opcodes += gg
			f.close()
		
			created_str = ''
			x = 0
			string = list(opcodes)
			count = 0
			while x<len(string):
				if x+1<len(string):created_str +="\\x"+string[x]+string[x+1]	
				else:created_str +="\\x"+string[x]
				count +=1
				x +=2 
	
			print self.style.yellow(self.style.bold(" "*3 + "%d Bytes of Shellcode created\n"%(count)))

			if count>0:
				print self.style.green(" "*3+"%s\n" %(created_str))
			os.remove("temp.dump")
