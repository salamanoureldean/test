import requests
import json
import course
import time



def scrape_data(term,year,courseCodes):

    lst = []

    for courseCode in courseCodes:
        courseCode = courseCode.replace(" ","-")

        scraper = requests.get(f'https://api.brethan.net/term/{term}/{year}/courseCode/{courseCode}')

        time.sleep(0.5)

        #print(r.status_code)
        b = json.loads(scraper.text)
        print(b)
        for c in b["data"]:
            temp = course.Course()
            temp.crn = c["crn"]
            temp.courseCode = c["courseCode"]
            temp.courseSection = c["section"]
            # "courseName": "Systems and Simulation", "courseType": "Lecture", "instructor": "Howard Schwartz", "meetingInfo":
            temp.courseName = c["courseName"]
            temp.courseType = c["courseType"]
            temp.instructor = c["instructor"]
            temp.meetingInfo = c["meetingInfo"]
            temp.alsoRegister = c["alsoRegister"]

            if temp.alsoRegister is None:
                temp.alsoRegister = ""

            lst.append(temp)

    return lst



def scrape_data_chat(term, year, courseCodes):
    schedule = Schedule()  # Create a Schedule object

    for courseCode in courseCodes:
        courseCode = courseCode.replace(" ", "-")

        scraper = requests.get(f'https://api.brethan.net/term/{term}/{year}/courseCode/{courseCode}')

        time.sleep(0.5)

        # print(r.status_code)
        b = json.loads(scraper.text)
        print(b)
        for c in b["data"]:
            temp = Course()
            temp.crn = c["crn"]
            temp.code = c["courseCode"]
            temp.section = c["section"]
            temp.days = c["meetingInfo"]["days"]
            temp.start_time = datetime.strptime(c["meetingInfo"]["time"].split(" - ")[0], "%H:%M")
            temp.end_time = datetime.strptime(c["meetingInfo"]["time"].split(" - ")[1], "%H:%M")
            temp.course_tie = c["courseType"]
            temp.tutorials = []  # You can modify this if tutorials are available

            schedule.add_course(temp)  # Add the course to the schedule

    return schedule

term = "fall"  # Specify the term (e.g., "fall", "winter", "spring")
year = "2023"  # Specify the year
courseCodes = ["SYSC 3110", "SYSC 3120", "SYSC 3310", "SYSC 4001", "ECOR 2050", "COMP 2804"]  # Specify the course codes

schedule = scrape_data(term, year, courseCodes)

# Print the schedule information
schedule_info = schedule.get_schedule_info()
for course_info in schedule_info:
    print(course_info)


