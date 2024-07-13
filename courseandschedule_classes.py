import requests
import json
from datetime import datetime
import time

class Course:
    def __init__(self, crn: str, code: str, section: str, days: str, start_time: datetime, section_tie: str, end_time: datetime, tutorials=None):
        self.crn = crn
        self.code = code
        self.section = section
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.tutorials = []
        self.section_tie = section_tie

    def __repr__(self):
        course_string = self.__print_string()
        tutorial_string = "Tutorials: {"
        for tutorial in self.tutorials:
            tutorial_string += tutorial.__print_string() + ", "

        course_string += ", " + tutorial_string.strip()
        course_string = course_string[0:len(course_string) - 1] + "}"
        return course_string

    def add_tutorial(self, tutorials):
        self.tutorials = tutorials

    def __print_string(self):
        return f"{self.crn} {self.code} {self.days} {self.section} {self.start_time.strftime('%H:%M')} {self.end_time.strftime('%H:%M')}"

def read_courses_from_file(file_path):
    courses = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines[1:]:
            course_data = line.strip().split(', ')
            crn, code, section, days, start_time, end_time, section_tie = course_data
            
            start_time = datetime.strptime(start_time, "%H:%M")
            end_time = datetime.strptime(end_time, "%H:%M")
            
            course = Course(crn, code, section, days, start_time, section_tie, end_time)
            courses.append(course)
    
    return courses

def read_tutorials_from_file(file_path, courses):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
        for line in lines[1:]:
            tutorial_data = line.strip().split(', ')
            crn, code, section, days, start_time, end_time, section_tie = tutorial_data
            
            start_time = datetime.strptime(start_time, "%H:%M")
            end_time = datetime.strptime(end_time, "%H:%M")
            
            tutorial = Course(crn, code, section, days, start_time, section_tie, end_time)
            
            for course in courses:
                if course.section_tie == section_tie:
                    course.add_tutorial(tutorial)

class Schedule:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
        self.courses.append(course)

    def get_schedule_info(self):
        schedule_info = []
        for course in self.courses:
            course_info = "Course:"
            course_info += f"\n - Course Code: {course.code}"
            course_info += f"\n - Course Section: {course.section}"
            course_info += f"\n - Meeting time: {course.start_time.strftime('%H:%M')} - {course.end_time.strftime('%H:%M')}"
            course_info += f"\n - Days: {course.days}"
            schedule_info.append(course_info)
        return schedule_info
    
# Example usage
course_file_path = "courses.txt"
tutorial_file_path = "tutorials_scrape.txt"

courses = read_courses_from_file(course_file_path)
read_tutorials_from_file(tutorial_file_path, courses)

# Print the courses and their tutorials
for course in courses:
    print(course)
    if course.tutorials:
        print("Tutorials:")
        for tutorial in course.tutorials:
            print(tutorial)
    print()

"""from datetime import datetime

# Read the contents of the notepad files
with open("file1.txt", "r") as file1:
    file1_contents = file1.read()

with open("file2.txt", "r") as file2:
    file2_contents = file2.read()

# Process file 1 data
courses_scrape = course_scrape.split("\n")
courses = []

for line in file1_lines[1:]:  # Skip the header line
    if line.strip():  # Skip empty lines
        fields = line.split(", ")
        crn = fields[0].strip()
        code = fields[1].strip()
        section = fields[2].strip()
        days = fields[3].strip()
        start_time = datetime.strptime(fields[4].strip(), "%H:%M")
        end_time = datetime.strptime(fields[5].strip(), "%H:%M")
        section_tie = fields[6].strip()

        # Create a Course object
        course = Course(crn, code, section, days, start_time, end_time, section_tie)
        courses.append(course)

# Process file 2 data
tutorials = tutorials_scraping.split("\n")

for line in tutorials_scraping[1:]:  # Skip the header line
    if line.strip():  # Skip empty lines
        fields = line.split(", ")
        crn = fields[0].strip()
        code = fields[1].strip()
        section = fields[2].strip()
        days = fields[3].strip()
        start_time = datetime.strptime(fields[4].strip(), "%H:%M")
        end_time = datetime.strptime(fields[5].strip(), "%H:%M")
        section_tie = fields[6].strip()

        # Create a Course object
        course = Course(crn, code, section, days, start_time, end_time, section_tie)
        courses.append(course)

# Add the courses to a Schedule object if needed
schedule = Schedule()
for course in courses:
    schedule.add_course(course)

# Get schedule information
schedule_info = schedule.get_schedule_info()
for course_info in schedule_info:
    print(course_info)
"""