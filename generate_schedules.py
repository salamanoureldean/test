def generate_schedules(courses, current_schedule, conflicts, all_schedules):
    if len(current_schedule) == len(courses):
        all_schedules.append(current_schedule)
        return

    for course in courses:
        if course not in current_schedule:
            has_conflict = False
            for scheduled_course in current_schedule:
                if course.crn in conflicts.get(scheduled_course.crn, []):
                    has_conflict = True
                    break

            if not has_conflict:
                updated_schedule = current_schedule + [course]
                generate_schedules(courses, updated_schedule, conflicts, all_schedules)


# Usage example
courses = [...]  # List of Course objects
conflicts = {...}  # Dictionary of course conflicts

all_schedules = []
generate_schedules(courses, [], conflicts, all_schedules)

# Print all generated schedules
for schedule in all_schedules:
    for course in schedule:
        print(course)
    print()
