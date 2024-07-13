from datetime import datetime
from tabulate import tabulate
from itertools import permutations


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
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                course_info = line.split(", ")
                crn = str(course_info[0])
                code = course_info[1]
                section = course_info[2]
                days = course_info[3].split()
                start_time = course_info[4]
                end_time = course_info[5]
                section_type = course_info[6]
                tutorials = []
                if len(course_info) > 7:
                    tutorials = course_info[7].split()
                course = {
                    "crn": crn,
                    "code": code,
                    "section": section,
                    "days": days,
                    "start_time": start_time,
                    "end_time": end_time,
                    "section_type": section_type,
                    "tutorials": tutorials
                }
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
    
# Read courses from file
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
    
# Print the courses and their tutorials
for course in courses:
    print(course)
    if course.tutorials:
        print("Tutorials:")
        for tutorial in course.tutorials:
            print(tutorial)
    print()
    
    # Create a 2D array table with empty cells
    table = [["" for _ in range(6)] for _ in range(13)]
    
    # Keep track of courses added to the table
    added_courses = set()
    
    # Populate the table with course information
    for course in courses:
        if course.code not in added_courses:
            for day in course.days.split():
                col = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5}[day]
                start_hour = course.start_time.hour
                start_slot = start_hour - 8 if start_hour < 12 else start_hour - 9
                end_hour = course.end_time.hour
                end_slot = end_hour - 8 if end_hour < 12 else end_hour - 9
    
                for i in range(start_slot, end_slot):
                    if table[i][col]:
                        # If a course is already scheduled, check the previous day for availability
                        if col > 1 and not table[i][col-1]:
                            table[i][col-1] = course.code
                    else:
                        table[i][col] = course.code
            added_courses.add(course.code)
    
    # Add the time slots to the first column
    time_slots = ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM",
                  "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM"]
    for i, time_slot in enumerate(time_slots):
        table[i][0] = time_slot
    
    # Add the days to the first row
    table[0][1] = "Monday"
    table[0][2] = "Tuesday"
    table[0][3] = "Wednesday"
    table[0][4] = "Thursday"
    table[0][5] = "Friday"
    
    # Print the populated table
    print(tabulate(table, headers="firstrow", tablefmt="grid"))



# Generate all possible schedule combinations
all_schedules = []

# Helper function to generate schedule combinations recursively
def generate_schedules(current_schedule, remaining_courses):
    if not remaining_courses:
        # Base case: No more courses to add, schedule is complete
        all_schedules.append(current_schedule)
        return

    current_course = remaining_courses[0]
    remaining_courses = remaining_courses[1:]

    # Try adding the current course to the schedule
    if is_schedule_valid(current_schedule, current_course):
        updated_schedule = Schedule()
        for course in current_schedule.courses:
            updated_schedule.add_course(course)
        updated_schedule.add_course(current_course)
        generate_schedules(updated_schedule, remaining_courses)

    # Skip the current course and proceed to the next one
    generate_schedules(current_schedule, remaining_courses)

# Helper function to check if a course conflicts with existing courses in the schedule
def is_schedule_valid(schedule, course):
    for existing_course in schedule.courses:
        if courses_conflict(existing_course, course):
            return False
    return True

# Helper function to check if two courses conflict in terms of days and times
def courses_conflict(course1, course2):
    if course1.days == course2.days:
        if course1.start_time < course2.end_time and course1.end_time > course2.start_time:
            return True
    return False

# Create an initial empty schedule
initial_schedule = Schedule()

# Generate all possible schedule combinations
generate_schedules(initial_schedule, courses)

# Create a table to store the schedules
table = []

# Add the header row with days of the week
header_row = ["Time"]
for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
    header_row.append(day)
table.append(header_row)

# Add rows for each timeslot
timeslots = ["8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM"]
for timeslot in timeslots:
    row = [timeslot]
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        course_names = []
        for schedule in all_schedules:
            for course in schedule.courses:
                if course.days == day and course.start_time.strftime("%I:%M %p") == timeslot:
                    course_names.append(f"{course.code} {course.section}")
        row.append(", ".join(course_names))
    table.append(row)

# Print the table
print(tabulate(table, headers="firstrow", tablefmt="grid"))


# Define the courses
courses = [
    ("35574", "SYSC3110", "Wed", "Fri", "A", "13:05", "14:25", "Tutorials: }"),
    ("35577", "SYSC3120", "Wed", "Fri", "A", "11:35", "12:55", "Tutorials: }"),
    ("35585", "SYSC3310", "Mon", "Wed", "A", "18:05", "19:25", "Tutorials: }"),
    ("35586", "SYSC3310", "Mon", "Wed", "B", "08:35", "09:55", "Tutorials: }"),
    ("35613", "SYSC4001", "Tue", "Thu", "A", "13:05", "14:25", "Tutorials: }"),
    ("35617", "SYSC4001", "Tue", "Thu", "B", "10:05", "11:25", "Tutorials: }"),
    ("32357", "ECOR2050", "Mon", "Wed", "A", "10:05", "11:25", "Tutorials: }"),
    ("32358", "ECOR2050", "Tue", "Thu", "B", "08:35", "09:55", "Tutorials: }")
]

# Generate all possible permutations of the courses
course_permutations = permutations(courses)

# List to store valid schedules
valid_schedules = []

# Iterate through each permutation
for permutation in course_permutations:
    schedule = []  # List to store the current schedule

    # Iterate through each course in the permutation
    for course in permutation:
        # Check for conflicts with courses already scheduled
        if all(not (course[2] == scheduled_course[2] and
                    (course[6] <= scheduled_course[5] or course[5] >= scheduled_course[6]))
               for scheduled_course in schedule):
            schedule.append(course)  # Add the course to the schedule

    # If all courses can be scheduled without conflicts, add the schedule to the list
    if len(schedule) == len(courses):
        valid_schedules.append(schedule)

# Generate tables for each valid schedule
for i, schedule in enumerate(valid_schedules):
    table = [["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]]

    # Iterate through each time slot
    for j in range(8, 21):
        row = [f"{j}:00 AM" if j < 12 else f"{j-12}:00 PM"]

        # Iterate through each day
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
            # Find the course scheduled for the current time slot and day
            scheduled_course = next((course[1] for course in schedule
                                     if course[2] == day and course[5] == f"{j:02d}:00"), "")

            row.append(scheduled_course)

        table.append(row)

    print(f"Schedule {i+1}:")
    print(tabulate(table, headers="firstrow", tablefmt="grid"))
    print()
