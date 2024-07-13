#class models a course
#Salama Nour El Dean
from datetime import datetime

class Course:
    def __init__(self, crn: str, code: str, section: str, days: str, start_time: datetime, end_time: datetime, course_tie: str, tutorials = [])-> None:
        self.crn = crn
        self.code = code
        self.section = section
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.course_tie = course_tie
        self.tutorials = tutorials
        
        def __repr__(self) -> str:
            course_string = self.__print_string()
            tutorial_string = "Tutorials: {"
            for tutorial in self.tutorials:
                tutorial_string += tutorial.__print_string() + ", "
                
            course_string += ", " + tutorial_string.strip()
            course_string = course_string[0:len(course_string) - 1] + "}"
            return course_string
        
        def add_tutorial(self, tutorials: list) -> None:
            self.tutorials = tutorials
            
        def __print_string(self):
            #return str(self.crn) + " " + str(self.code) + " " + str(self.days) +\
                   #" " + str(self.section) + " " + self.start_time.strftime("%H:%M")\
                  # + " " + self.end_time.strftime("%H:%M")
            return f"{self.crn} {self.code} {self.days} {self.section} {self.start_time.strftime('%H:%M')} {self.end_time.strftime('%H:%M')}"
        
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
            course_info += f"\n  - Days: {course.days}"
            schedule_info.append(course_info)
        return schedule_info
    