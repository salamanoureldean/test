import itertools
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

    def add_tutorial(self, tutorial):
        self.tutorials.append(tutorial)

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

            # Find the course that matches the section_tie
            matching_courses = [course for course in courses if course.section_tie == section_tie]

            for matching_course in matching_courses:
                matching_course.add_tutorial(tutorial)




class Schedule:
    def __init__(self):
        self.courses = []

    def add_course(self, course):
            for existing_course in self.courses:
                if course.days == existing_course.days and course.start_time < existing_course.end_time and course.end_time > existing_course.start_time:
                    return False  # Time conflict, return False
    
                if course.code == existing_course.code:
                    return False  # Duplicate section, return False
    
            self.courses.append(course)
            return True


    def calculate_rank(self):
        # Implement your ranking criteria here
        return 0  # Replace with the actual ranking calculation

    def __repr__(self):
        return ', '.join([str(course) for course in self.courses])



    
def generate_schedules(courses):
    schedules = []

    # Start with an empty schedule
    initial_schedule = Schedule()

    # Generate schedules recursively
    generate_schedules_recursive(initial_schedule, courses, schedules)

    return schedules

def generate_schedules_recursive(schedule, remaining_courses, schedules):
    # Base case: No more courses to add
    if not remaining_courses:
        schedules.append(schedule)
        return

    # Iterate over the remaining courses
    for i, course in enumerate(remaining_courses):
        # Check if a course with the same code already exists in the schedule
        if any(existing_course.code == course.code for existing_course in schedule.courses):
            continue

        # Create a new schedule by adding the course
        new_schedule = Schedule()
        new_schedule.courses = schedule.courses.copy()
        if new_schedule.add_course(course):
            # Remove the added course from the remaining courses
            remaining_courses_copy = remaining_courses.copy()
            remaining_courses_copy.pop(i)

            # Generate schedules recursively with the remaining courses
            generate_schedules_recursive(new_schedule, remaining_courses_copy, schedules)
        
        # Print the tutorials for debugging
        print("Tutorials for current schedule:", [tutorial.__print_string() for tutorial in new_schedule.courses[-1].tutorials])



# Assuming the course and tutorial files are in CSV format
course_file_path = 'courses.txt'
tutorial_file_path = 'tutorials_scrape.txt'

# Read courses from file
courses = read_courses_from_file(course_file_path)

# Read tutorials from file
read_tutorials_from_file(tutorial_file_path, courses)

# Print courses and tutorials for debugging
print("Courses:")
for course in courses:
    print(course)
print("Tutorials:")
for course in courses:
    print(course.tutorials)

# Generate schedules
schedules = generate_schedules(courses)

# Sort the schedules based on ranking criteria
sorted_schedules = sorted(schedules, key=lambda s: s.calculate_rank())

# Print the schedules
for schedule in sorted_schedules:
    print(schedule)
