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

import More_Functions
import Help
import Style
import sys

class Prompt:

	def __init__(self):
			
		self.style = Style.Style()
		self.prompt_text = "PySystem"

        def run_prompt(self):
                while 1:
		 	self.j = raw_input(self.style.red(self.prompt_text+ " >> "))
		 				
                 	self.help_text = Help.Help(self.j)
                 	self.more_funct = More_Functions.More_Functions(self.j,0)

	def cmd_prompt(self,text = ''):
		if len(text)>0:
			full_prompt = self.style.red(self.prompt_text)+self.style.bold(self.style.blue(" ("+ text +")"))+self.style.red(" >> ")
		else:
			full_prompt = self.style.red(self.prompt_text+" >> ")

		self.j = raw_input(full_prompt)	
		self.more_funct = More_Functions.More_Functions(self.j,1)
		return self.j
