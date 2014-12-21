'''
Created on Dec 12, 2014
@author: rockwotj
'''
import urllib2

class PageParser:
    """ The super class for all of the Course Catalog parsers """

    url = "https://prodweb.rose-hulman.edu/regweb-cgi/reg-sched.pl"

    def __init__(self, username, password):
        """ Creates a new PageParser that pulls data off of the Rose-Hulman Schedule look-up page 
            Need to pass in a KERBEROS username and password to pull the data into the database.
        """
        # create a password manager
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

        # add the password for the URL
        password_mgr.add_password(None, PageParser.url, username, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)

        # create private class variable "__opener" (OpenerDirector instance)
        self._opener = urllib2.build_opener(handler)