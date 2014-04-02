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
#============================================================================
#		More Function Class
#============================================================================

import os,sys
import Tree
import Prompt
import FileSystem,Security

class More_Functions:

        def __init__(self,args,status):

		self.commandList = ['tree','exit','clear','dir','search',
			'advSearch','del','shellcode'
		]
		
		x = args.split(' ')

		self.prompt = Prompt.Prompt()
		self.file = FileSystem.FileSystem()
		self.security = Security.Security()
		
		self.args = ['']

		if status == 0:
			if len(x)>1:
				for g in self.commandList:
					if x[0] == g:
						self.args2 = x[1:]
						self.args = x[0] 
			else:
				self.args = x[0]	
				self.args2 = ['']

		if status == 1:
			self.args = ['']

#===================================================================================			

                if self.args =="exit":
                        print '\r\tPySystem is Exiting. Thank you...\n'
                	sys.exit()

                if self.args =="clear":
        		os.system("clear")   

		if self.args =="tree":
                        self.tree(self.args2[0])             

		if self.args =="dir":
			self.dir_listing(self.args2[0])

		if self.args =="search":
			self.search(self.args2[0])
			
		if self.args =="advSearch":
			self.file.adv_Search(self.args2)

		if self.args =="del":
			self.file.delete_file(self.args2)

		if self.args =="shellcode":
			self.shellcode(self.args2[0])

#===================================================================================

	def tree(self,args):
		if len(args)>0:
			path = args
		else:
			path = self.prompt.cmd_prompt('tree')
		Tree.Tree(path)	
	

	def dir_listing(self,args):
		if len(args)>0:
			path = args
		else:
			path = self.prompt.cmd_prompt('dir')
		self.file.dir_traversal(path)


	def search(self,args):
		if len(args)>0:
			path = args		
		else:
			path = self.prompt.cmd_prompt("search")
		self.file.file_searcher(path)

	def shellcode(self,args):
		if len(args)>0:
			path = args
		else:
			path = self.prompt.cmd_prompt('shellcode')
		self.security.ShellcodeGenerator(path)	
