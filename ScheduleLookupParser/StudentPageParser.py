'''
This module pulls data from https://prodweb.rose-hulman.edu/regweb-cgi/reg-sched.pl
To get the information on a single Student's quarter schedule.

Created on Dec 4, 2014
@author: rockwotj
'''
import re

from ScheduleLookupParser.PageParser import PageParser


class StudentPageParser(PageParser):
    """ 
    A parser that pulls data off of the schedule pages at Rose and parses it into
    a python class (Student). Call the parse(user_id) method to get a information about a single Student.
     """

    def __init__(self, username, password):
        """ Creates a new SectionPageParser that pulls data off of the Rose-Hulman Schedule look-up page 
            Need to pass in a KERBEROS username and password to pull the data.
        """
        PageParser.__init__(self, username, password)

    def __get_schedule_html(self, username, termcode):
        """ PRIVATE: Gets the HTML data that is the courses offered for a given quarter """
        # use the __opener to fetch a URL
        args = "termcode=" + termcode + "&view=table&id1=" + username + "&bt1=ID%2FUsername&id4=&id5="
        html_string = self._opener.open(PageParser.url, data=args).read()
        return html_string

    def parse(self, username, termcode):
        """ Parses all of the information from a student's schedule lookup page into a student class """
        html_string = self.__get_schedule_html(username, termcode)
        name = re.search("Name: (.*?)<", html_string).group(1)
        username = re.search("Username: (.*?)<", html_string).group(1)
        major = re.search("Major: (.*?)<", html_string).group(1)
        year = re.search("Year: (.*?)<", html_string).group(1)
        courses = re.findall('<TR><TD><A HREF=".*?">(.*?)</A></TD>', html_string)
        return Student(username, name, major, year, courses)


class Student:
    """ The is the data structure for a Student at Rose Hulman.
            Below are the fields of the struct:            
            username: The Student's kerberos username        Example: rockwotj
            name: The Student's name                         Example: Tyler Jon Rockwood
            major: The Student's major                       Example: CS/SE
            year: The Student's year at Rose                 Example: Y3 
            courses: The courses the user is enrolled in     Example: [CSSE332-01, CSSE374-01, CSSE403-01, CSSE483-02]
    """

    def __init__(self, username, name, major, year, courses):
        self.username = username
        self.name = name
        self.major = major
        self.year = year
        self.courses = courses

    def __str__(self):
        return """
------ STUDENT ------
username: {0}
name: {1}
major: {2}
year: {3}
courses: {4}
        """.format(str(self.username), str(self.name),
                   str(self.major), str(self.year),
                   str(self.courses)).strip()


def run(username, password, termcode, target_id):
    """ Prints the information for a student for a given quarter """
    parser = StudentPageParser(username, password)
    print "Started Parsing " + termcode + " Student Information about " + target_id + " for " + username
    try:
        student = parser.parse(target_id, termcode)
    except:
        print "Invalid credentials to Student page (or the parser broke)"
        return
    print student
