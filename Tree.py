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

import os
import sys
import Style

class Tree():

	def __init__(self,directory = ''):
		self.b1='--';self.tab='|';self.chr='b';		# variables
		
		self.style = Style.Style()		

		if len(directory)>0:
			if directory=="?" or directory=="/?":
				print self.style.blue("\tUSAGE : tree <directory_name>")
				print self.style.blue("\tCurrent working directory is shown below")
				self.directory = os.getcwd()
			else:		
				self.directory = directory	
		else:
			print self.style.blue("\tUSAGE : tree <directory_name>")
			print self.style.blue("\tCurrent working directory is shown below")
			self.directory = os.getcwd()
			
		try: 
			os.path.isdir(self.directory)
			self.chr = 'a'
		except:
			print self.style.errcode('\t path doesnot exists')		
			
		if self.chr=='a':		
			if os.path.exists(self.directory): 
				print self.style.yellow(self.directory)
				self.outer_dir(self.directory)
			else:
				print self.style.errcode('\t path doesnot exists')
		
	def outer_dir(self,directory):

		l1 = os.listdir(directory)

		temp = '';self.count_me_now = 0

		for i in range(len(l1)):
			for j in range(i,len(l1)-1):
				if os.path.isdir(os.path.join(directory,l1[i])):
					
					if not os.path.isdir(os.path.join(directory,l1[j])):
						temp = l1[i]
						l1[i] = l1[j]
						l1[j] = temp	
				
		for l in l1:
			#
			if not os.path.isdir(os.path.join(directory,l)):
				print " "*3+self.tab+self.b1+" "+l
			else:
				print " "*3+self.tab
				print " "*3+self.tab+self.b1+" "+self.style.green(l)
				self.inner_dir(os.path.join(directory,l)," "*3)
				print " "*3+self.tab		

	def inner_dir(self,directory,gap):
		gap = gap + " "*3

		h1 = " "*3 + self.tab + gap + self.tab + self.b1

		l1 = os.listdir(directory)

		temp = ''
		
		for i in range(len(l1)):
			
			if os.path.isdir(os.path.join(directory,l1[i])):
				if i+1 < len(l1):
					
					if not os.path.isdir(os.path.join(directory,l1[i+1])):
						temp = l1[i]
						l1[i] = l1[i+1]
						l1[i+1] = temp	
		for l in l1:
			
			if not os.path.isdir(os.path.join(directory,l)):
				print h1 + l
			else:
				print " "*3 + self.tab + gap + self.tab
				print h1 + self.style.green(l)				
				self.count_me_now +=1 
				self.inner_dir(os.path.join(directory,l),gap)
				
		
	

