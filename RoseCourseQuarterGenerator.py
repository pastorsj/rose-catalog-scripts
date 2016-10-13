# Get a list of everyone enrolled
# Call student page parser on all terms from 2010->current term with all students enrolled
# Once each term has been parsed, insert into json file

import json

from ScheduleLookupParser import SectionPageParser

username = 'pastorsj'
password = 'L5xpsQ922ewcpk'
term = "201720"


def main():
    time_converter = create_time_dict()
    terms = [201720]
    for term in terms:
        file = open('dat/Course_' + str(term) + '.json', 'r')
        courses = SectionPageParser.parse(username, password, str(term))
        parse_courses_into_json(courses, str(term), time_converter)

def parse_courses_into_json(courses, term, time_converter):
    json_data = []
    for Section in courses:
        data = {}
        data['Name'] = Section.section_id
        data['Type'] = 'Course'
        data['CRN'] = '9999'
        data['CreditHours'] = '4'
        data['Description'] = Section.title
        data['MeetTimes'] = convert_meeting_times(Section.time, time_converter)
        data['Instructor'] = str(Section.prof_id).upper()
        json_data.append(data)
    json_data = json.dumps(json_data, indent=4)
    write_to_file('new_dat/Course_' + term + '.dat', json_data)


def write_to_file(fname, data):
    file = open(fname, 'w')
    file.write(data)
    file.close()


def convert_meeting_times(meeting_time, time_converter):
    if str(meeting_time).upper() == "TBA":
        print "When does this print? ======="
        return meeting_time
    times = meeting_time.split(':')
    meeting_time_result = ""
    for course in times:
        a = course.split('/')[0]
        b = course.split('/')[1]
        time_array = b.split('-')
        begin = time_array[0]
        end = ''
        if len(time_array) > 1:
            end = time_array[1]
        elif len(begin) == 1:
            end = str(int(begin) + 1)
        time_converted_begin = time_converter.get(begin, begin)
        time_converted_end = time_converter.get('-' + end, end if begin == 'TBA' else '-' + end)
        meeting = a + " " + time_converted_begin + time_converted_end
        meeting_time_result += meeting + " "
    return meeting_time_result.rstrip()


def create_time_dict():
    return {
        '1': '0805',
        '-2': '-0855',
        '2': '0900',
        '-3': '-0950',
        '3': '0955',
        '-4': '-1045',
        '4': '1050',
        '-5': '-1140',
        '5': '1145',
        '-6': '-1235',
        '6': '1240',
        '-7': '-1340',
        '7': '1345',
        '-8': '-1425',
        '8': '1430',
        '-9': '-1520',
        '9': '1525',
        '-10': '-1515',
        '10': '1520'
    }


if __name__ == "__main__":
    main()
