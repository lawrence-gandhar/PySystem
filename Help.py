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
#=======================================================================================
#       Help Class
#=======================================================================================

import sys,os
import Style

class Help:

        def __init__(self,g):

                self.help_cmd = g        
		
		self.text = ''     

                self.help_array = ["?","/?","help"]

		self.syscmds = {
				'tree' :'Graphically display the directory structure of a path. Default is /',
			  	'exit':'Exit the Program',
			  	'clear':'Clear the Screen',
			  	'dir':'List directory',
			  	'search':'Search for files',
			 	'advSearch':'Search for files based on extension and filename',
		      	 	'del':'Delete files'	
			 }     

		self.netcmds = {
			       	'PyFtp':'Ftp Server or Client',
			       	'PyTelnet':'Telnet',
			       	'PyServer':'Web Server'
                              }

		self.sectools = {
				'shellcode':'Shellcode String Generator'
				}

		self.cmds_list = {
				'System Tools':self.syscmds,
			     	#'Server and Client Tools':self.netcmds,
			     	'Security Tools':self.sectools
                            }

		self.style = Style.Style()                

                for x in self.help_array:
                        if self.help_cmd == x:       
				for g in self.cmds_list.keys():
					print self.help_banner(g,self.cmds_list[g])
		print

#=================================================================================================			
	
	def help_banner(self,heading,lists):
                text = self.style.blue(self.style.underline("\n\t"+heading +"\n"))

		f1 =lists.keys() 
		
		for f in f1:
			text += "\n"+self.style.yellow(self.style.bold(f))

			if len(f)<=12:
				space = 12 - len(f)

				text +=" "*space+"\t"+lists[f]
			else:
				text +="\t"+lists[f]

		return text

		
        
