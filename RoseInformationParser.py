# Get a list of everyone enrolled
# Call student page parser on all terms from 2010->current term with all students enrolled
# Once each term has been parsed, insert into json file

import json
from ScheduleLookupParser import SectionPageParser

username = 'pastorsj'
password = ''

def main():
    time_converter = create_time_dict()
    terms = [201010, 201020, 201030, 201040, 201110, 201120, 201130, 201140, 201210, 201220, 201230, 201240, 201310, 201320, 201330, 201340, 201410, 201420, 201430, 201440, 201510, 201520, 201530, 201540, 201610, 201620]
    for term in terms:
        file = open('dat/Course_' + str(term) + '.json', 'r')
        file_contents = file.read()
        contents_dict = json.loads(file_contents)
        courses = SectionPageParser.parse(username, password, str(term))
        parse_courses_into_json(courses, str(term), contents_dict, time_converter)

def parse_courses_into_json(courses, term, contents_dict, time_converter):
    json_data = []
    for Section in courses:
        data = {}
        for course in contents_dict:
            if course['Name'] == Section.section_id:
                data = course
                break
        data['Description'] = Section.title
        print "INITIAL MEETING TIME STRING: " + Section.time
        if 'MeetTimes' in course:
            if course['MeetTimes'] is None:
                data['MeetTimes'] = 'TBA'
            elif course['MeetTimes'] != 'null' or course['MeetTimes'].strip() != '-':
                data['MeetTimes'] = course['MeetTimes']
            else:
                print 'Incompatible format: ' + course['MeetTimes']
                raise
        else:
            data['MeetTimes'] = convert_meeting_times(Section.time, time_converter)
        print 'FINAL MEETING TIME STRING: ' + str(data['MeetTimes'])
        print "================================="
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
