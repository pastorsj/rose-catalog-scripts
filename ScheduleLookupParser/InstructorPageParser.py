'''
This module pulls data from https://prodweb.rose-hulman.edu/regweb-cgi/reg-sched.pl
To get the information on a single instructor's quarter schedule.

Created on Dec 4, 2014
@author: rockwotj
'''
import re

from ScheduleLookupParser.PageParser import PageParser


class InstructorPageParser(PageParser):
    """ 
    A parser that pulls data off of the schedule pages at Rose and parses it into
    a python class (instructor). Call the parse(user_id) method to get a information about a single instructor.
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
        """ Parses all of the information from a professor's schedule lookup page into an instructor class """
        html_string = self.__get_schedule_html(username, termcode)
        name = re.search("Name: (.*?)<", html_string).group(1)
        username = re.search("Username: (.*?)<", html_string).group(1)
        dept = re.search("Dept: (.*?)<", html_string).group(1)
        office = re.search("Room: (.*?)<", html_string).group(1)
        phone = re.search("Phone: (.*?)<", html_string).group(1)
        mailbox = re.search("Campus Mail: (.*?)<", html_string).group(1)
        courses = re.findall('<TR><TD><A HREF=".*?">(.*?)</A></TD>', html_string)
        return Instructor(username, name, dept, office, phone, mailbox, courses)


class Instructor:
    """ The is the data structure for a class section at Rose Hulman.
            Below are the fields of the struct:            
            username: The student's kerberos username          Example: boutell
            name: The professor's name                         Example: Matthew R Boutell
            dept: The instructor's department                  Example: Computer Science & Software Engineering
            office: The instructor's office                    Example: Moench F222
            phone: The instructor's phone number               Example: 877-8534
            mailbox: The instructors CM box                    Example: CM 4005 
            courses: Courses being taught by the professor     Example: [CSSE463-01, CSSE483-01, CSSE483-02, CSSE491-02, CSSE491-06, CSSE495-02]
    """

    def __init__(self, username, name, dept, office, phone, mailbox, courses):
        self.username = username
        self.name = name
        self.dept = dept
        self.office = office
        self.phone = phone
        self.mailbox = mailbox
        self.courses = courses

    def __str__(self):
        return """
------ INSTRUCTOR ------
username: {0}
name: {1}
dept: {2}
office: {3}
phone: {4}
mailbox: {5}
courses: {6}
        """.format(str(self.username), str(self.name),
                   str(self.dept), str(self.office),
                   str(self.phone), str(self.mailbox),
                   str(self.courses)).strip()


def run(username, password, termcode, target_id):
    parser = InstructorPageParser(username, password)
    print "Started Parsing " + termcode + " Instructor Information about " + target_id + " for " + username
    try:
        instructor = parser.parse(target_id, termcode)
    except:
        print "Invalid credentials to Instructor page (or the parser broke)"
        return
    print instructor
