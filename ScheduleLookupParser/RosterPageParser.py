'''
This module pulls data from https://prodweb.rose-hulman.edu/regweb-cgi/reg-sched.pl
To get the information on a single section's roster.

Created on Dec 4, 2014
@author: rockwotj
'''
import re

from ScheduleLookupParser.PageParser import PageParser


class RosterPageParser(PageParser):
    """ 
    A parser that pulls data off of the section pages at Rose and parses it into
    a python class (roster). Call the parse(course_id) method to get a information about a single roster.
     """

    def __init__(self, username, password):
        """ Creates a new RosterPageParser that pulls data off of the Rose-Hulman Schedule look-up page 
            Need to pass in a KERBEROS username and password to pull the data.
        """
        PageParser.__init__(self, username, password)

    def __get_schedule_html(self, course_id, termcode):
        """ PRIVATE: Gets the HTML data that is the courses offered for a given quarter """
        # use the _opener to fetch a URL
        args = "?type=Roster&termcode=" + termcode + "&view=tgrid&id=" + course_id
        html_string = self._opener.open(PageParser.url + args).read()
        return html_string

    def parse(self, course_id, termcode):
        """ Parses all of the information from a section's schedule lookup page into a roster class """
        html_string = self.__get_schedule_html(course_id, termcode)
        search = re.search('^<TR><TD><A HREF=".*?">(.*?)</A></TD><TD>.*?</TD><TD>.*?</TD><TD><A HREF=".*?">(.*?)<',
                           html_string, re.MULTILINE)
        course = search.group(1)
        professor = search.group(2)
        students = re.findall('^<TR><TD><A HREF=".*?">(.*?)</A></TD>', html_string, re.MULTILINE)[1:]
        roster = Roster(course, professor, students)
        return roster


class Roster:
    """ The is the data structure for a class section at Rose Hulman.
            Below are the fields of the struct:            
            course_id: The course id              Example: CSSE483-02
            professor: The professor's username   Example: boutell
            students: The enrolled students       Example: [barnesgl, brandegs, calleggr, ...]
    """

    def __init__(self, course_id, professor, students=[]):
        self.course_id = course_id
        self.professor = professor
        self.students = students

    def __str__(self):
        return """
------ ROSTER ------
course_id: {0}
professor: {1}
students: {2}
        """.format(str(self.course_id), str(self.professor),
                   str(self.students)).strip()


def run(username, password, termcode, target_id):
    """ Prints the roster for a specific class at Rose-Hulman"""
    parser = RosterPageParser(username, password)
    print "Started Parsing " + termcode + " Roster Information about " + target_id + " for " + username
    try:
        roster = parser.parse(target_id, termcode)
    except:
        print "Invalid credentials to Roster page (or the parser broke)"
        return
    print roster
