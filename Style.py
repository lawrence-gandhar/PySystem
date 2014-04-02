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

class Style:
	
	def __init__(self):

		self.esc 	= '\x1b'

		self.reset 	= '[0m'

		self.end 	= self.esc + self.reset

#==================================================================
#	font style
#==================================================================	
	
		self.font_bold 		='[1m'
		self.font_italics	='[3m'
		self.font_underline	='[4m'
		self.font_strike	='[9m'

#===================================================================
#	font color
#===================================================================
	
		self.black_color	='[30m'
		self.red_color		='[31m'
		self.green_color	='[32m'
		self.yellow_color	='[33m'
		self.blue_color		='[34m'
		self.white_color	='[37m'
	
#===================================================================
#	functions for font color
#===================================================================

	def red(self,args):
		return self.esc + self.red_color + args + self.end
	
	def yellow(self,args):
		return self.esc + self.yellow_color + args + self.end
	
	def green(self,args):
		return self.esc + self.green_color + args + self.end	

	def blue(self,args):
		return self.esc + self.blue_color + args + self.end

	def black(self,args):
                return self.esc + self.black_color + args + self.end

	def white(self,args):
                return self.esc + self.white_color + args + self.end

#====================================================================
#	functions for font style
#====================================================================

	def bold(self,args):
                return self.esc + self.font_bold + args + self.end

	def italics(self,args):
                return self.esc + self.font_italics + args + self.end

	def underline(self,args):
                return self.esc + self.font_underline + args + self.end

	def strike(self,args):
                return self.esc + self.font_strike + args + self.end

#=======================================================================
#	function for error code
#=======================================================================

	def errcode(self,args):
		return self.red(args)



