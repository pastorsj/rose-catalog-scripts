"""
This module pulls data from https://prodweb.rose-hulman.edu/regweb-cgi/reg-sched.pl
To get the sections for a Rose-Hulman quarter


Created on Sep 24, 2014.
@author: rockwotj.
"""

from HTMLParser import HTMLParser

from ScheduleLookupParser.PageParser import PageParser

class SectionPageParser(PageParser):
	""" 
	A parser that pulls data off of the schedule pages at Rose and parses it into
	a python class (Section). Call the parse() method to get a list of all the sections.
	 """

	# The states of the FSM for the HTML_FiniteStateMachine
	START_STATE = 0
	START_ROW = 1
	FIND_CRN = 2
	FIND_TITLE = 3
	FIND_INSTR = 4
	FIND_SCHEDULE = 5
	END_ROW = 6

	def __init__(self, username, password):
		""" Creates a new SectionPageParser that pulls data off of the Rose-Hulman Schedule look-up page 
			Need to pass in a KERBEROS username and password to pull the data into the database.
		"""
		PageParser.__init__(self, username, password)

	def __get_schedule_html(self, termcode):
		""" PRIVATE: Gets the HTML data that is the courses offered for a given quarter """
		# use the __opener to fetch a URL
		args = "termcode=" + termcode + "&view=table&id1=&id4=*&bt4=Room&id5="

		html_string = self._opener.open(PageParser.url, data=args).read()

		# replace all of the '&' with '+' so that the parser works correctly.
		return html_string.replace("&", "+")

	def parse(self, termcode):
		""" The method that parses the schedule page and puts it into a list of Sections """
		html = self.__get_schedule_html(termcode)
		parser = SectionPageParser.HTML_FiniteStateMachine(self)
		parser.feed(html)
		return parser.sections

	class HTML_FiniteStateMachine(HTMLParser):
		""" Inner class to handle the actual parsing of the data in the schedule page """

		def __init__(self, schedule_page_parser):
			HTMLParser.__init__(self)
			self.__current_state = SectionPageParser.START_STATE
			self.__parent = schedule_page_parser
			self.__current_section = None
			self.sections = []
			self.__counter = 0

		def handle_starttag(self, tag, attrs):
			tag = tag.lower()
			if self.__current_state == SectionPageParser.START_STATE:
				if tag == "table":
					self.__counter += 1
				elif tag == "tr" and self.__counter == 2:
					self.__current_state = SectionPageParser.START_ROW
			elif self.__current_state == SectionPageParser.START_ROW:
				if tag == "a":
					self.__current_state = SectionPageParser.FIND_CRN
			elif self.__current_state == SectionPageParser.FIND_CRN:
				pass
			elif self.__current_state == SectionPageParser.FIND_TITLE:
				if tag == "a":
					self.__current_state = SectionPageParser.FIND_INSTR
			elif self.__current_state == SectionPageParser.FIND_INSTR:
				pass
			elif self.__current_state == SectionPageParser.FIND_SCHEDULE:
				if tag == "td":
					self.__counter += 1
			elif self.__current_state == SectionPageParser.END_ROW:
				pass
			else:
				pass

		def handle_data(self, data):
			# There was some kind of problem with the data cutting off after
			# a '&' so I changed them to '+' and am changing them back here
			data = data.replace('+', '&')
			if self.__current_state == SectionPageParser.START_STATE:
				pass
			elif self.__current_state == SectionPageParser.START_ROW:
				pass
			elif self.__current_state == SectionPageParser.FIND_CRN:
				index = data.rfind("-")
				self.__current_section = Section(course_id=data[:index], section_id=data)
				self.__current_state = SectionPageParser.FIND_TITLE
				self.__counter = 0
			elif self.__current_state == SectionPageParser.FIND_TITLE:
				self.__counter += 1
				if self.__counter == 2:
					self.__current_section.title = data
			elif self.__current_state == SectionPageParser.FIND_INSTR:
				self.__current_section.prof_id = data
				self.__current_state = SectionPageParser.FIND_SCHEDULE
				self.__counter = 0
			elif self.__current_state == SectionPageParser.FIND_SCHEDULE:
				if self.__counter == 4:
					if data.count("/") == 0:
						self.__current_section.time = data
						self.__current_section.location = data
						self.__current_state = SectionPageParser.END_ROW
					else:
						data = data.split(":")
						times = []
						rooms = []
						for d in data:
							index = d.rfind("/")
							times.append(d[:index])
							rooms.append(d[index + 1:])
						self.__current_section.time = ":".join(times)
						self.__current_section.location = ":".join(rooms)
						self.__current_state = SectionPageParser.END_ROW
			elif self.__current_state == SectionPageParser.END_ROW:
				pass
			else:
				pass

		def handle_endtag(self, tag):
			tag = tag.lower()
			if self.__current_state == SectionPageParser.START_STATE:
				pass
			else:
				if tag == "tr" and self.__current_section != None:
					self.sections.append(self.__current_section)
					# print self.sections[-1]  # UNCOMMENT HERE TO SEE THE CLASSES APPEAR AS THEY ARE PARSED
					self.__current_section = None
					self.__current_state = SectionPageParser.START_ROW

class Section:
	"""   The is the data structure for a class section at Rose Hulman.
		  Below are the fields of the struct:			
			course_id: The course_id section_id number		Example: CSSE120
			section_id: Number & Section of a course_id	 	Example: CSSE120-01
			title: Course Title								Example: Introduction to Software Development
			prof_id: The usr name of a prof. delimiter: &	Example: boutell 
			time: hour(s) and days of the class				Example: MTR/8:W/5-7
			location: Which room the class is in	   		Example: O257:O159	  """

	def __init__(self, course_id, section_id, Title="", prof_id="", time="", location=""):
		self.course_id = course_id
		self.section_id = section_id
		self.title = Title
		self.prof_id = prof_id
		self.time = time
		self.location = location

	def __str__(self):
		# loop through the values of __dict__ calling str? Avast, it is not in order then...
		return """
------ SECTION ------
course_id: {0}
section_id: {1}
title: {2}
prof_id: {3}
time: {4}
Location: {5}
		""".format(str(self.course_id), str(self.section_id),
				   str(self.title), str(self.prof_id),
				   str(self.time), str(self.location)).strip()

def run(username, password, termcode):
	""" Collects all of the sections from Rose catalog search and prints them. """
	parser = SectionPageParser(username, password)
	print "Started Parsing " + termcode + " Section Information for " + username
	try:
		sections = parser.parse(termcode)
	except:
		print "Invalid credentials to Schedule page (or the parser broke)"
		return
	for Section in sections:
		print Section
