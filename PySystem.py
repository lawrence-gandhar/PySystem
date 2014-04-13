#!/usr/bin/env python
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
import pwd
import socket
import CmdOptions
import Style
import Prompt
import fcntl
import struct

#=======================================================================================
#	PySystem Class
#=======================================================================================

class PySystem:
	
	def __init__(self,cmd):
		
		self.cmdopts = cmd
		
		self.opts = CmdOptions.CmdOptions('hbc',sys.argv[1:])

		self.prompt = Prompt.Prompt()

		self.style = Style.Style()
				
		if len(self.opts.RetList())>0:
			self.main_args = self.opts.RetList()					
			
			self.q = ''
			for self.x in self.main_args:
				if self.x in ["-h","--h"]:
					self.q += 'a'
				if self.x in ["-b","--b"]:
					self.q += 'b'
				if self.x in ["-c","--c"]:
					self.q +='c'
			
			if self.q.find("c")==-1:

				if self.q.find("a")==-1:
					self.H_banner()

				if self.q.find("b")==-1:
					self.B_banner()

			self.prompt.run_prompt()			

		elif len(self.opts.WrongList())<1:
                        self.banner()
			self.prompt.run_prompt()
	
#==========================================================================================
#	Banner Functions
#==========================================================================================

	def help_banner(self):						# Help / Usage
		print "\n" + self.style.blue("USAGE") +""" 	
%s
./PySystem.py [-h][-b][-c] 

-h		Do not display help
-b		Do not display banner, Autor's name and System details
-c		Do not display any of the above

help, /?, ?	Show available commands
"""%self.designer('-',40)
	
	def banner(self):						# main banner
		print "\n"+ self.designer('=',85)
                print "\t"*4 + self.style.red("PySystem Ver 1.0")
                print self.designer('=',85)

                self.author()
                print self.style.blue('\nSYSTEM DETAILS')
                print self.designer('-',40)
                self.sys_details()
                self.designer('=',80)
                self.help_banner()

	def B_banner(self):						# -b banner
		print "\n"+ self.designer('=',85)
                print "\t"*4 + self.style.red("PySystem Ver 1.0")
                print self.designer('=',85)

                self.author()
                print self.style.blue('\nSYSTEM DETAILS')
                print self.designer('-',40)
                self.sys_details()

	def H_banner(self):							# -h banner
		self.designer('=',80)
                self.help_banner()

	def author(self):						
		print self.style.red("Author : Lawrence Gandhar")	

	def designer(self,sym,num):
		return sym*num

	def ip_addr(self,ifname='eth0'):
	    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    ip = socket.inet_ntoa(fcntl.ioctl(sock.fileno(),0x00008915,struct.pack('30s','eth0'))[20:24]) 
	    netmask = socket.inet_ntoa(fcntl.ioctl(sock.fileno(),0x0000891B,struct.pack('30s','eth0'))[20:24])	
	    return ip,netmask


	def sys_details(self):
		os_details = os.uname()
		ip,netmask = self.ip_addr('eth0')

		print 'IP Address	 : %s' %ip
		print 'Netmask	 	 : %s' %netmask

		print 'Host		 : %s' %socket.gethostname()		
		print 'Operating System : %s' %os_details[0]
		print 'Release          : %s' %os_details[3]
		print 'Version          : %s' %os_details[2]
		print 'Machine Type     : %s' %os_details[4]
		
#=======================================================================================
#	Main Execution Code	
#=======================================================================================
try:
	if __name__=="__main__":
	
		uid = os.getuid()
		user = pwd.getpwuid(uid).pw_name

		if user!="root":
			print 'Run the script as root'
		else:
			system = PySystem(sys.argv[1:])

except KeyboardInterrupt:
	print "\n"
	print "\r\tPySystem is Exiting. Thank you...\n"
	sys.exit(0);
