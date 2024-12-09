from tracemalloc import start
from csp import backtracking_search, dom_wdeg, forward_checking, mac, min_conflicts, mrv
from csp import CSP
import pandas as pd
import time


def make_constraints(course_map):

    def timetabling_constraints(A, a, B, b):

        """Check if the assignment (A=a, B=b) satisfies all constraints."""
        # Get the Course objects for A and B
        course_a = course_map[A]
        course_b = course_map[B]
        # print(course_a.course_name, course_b.course_name)
        # print(A, a, B, b)
        if A == B:
            return True  # Same variable, no conflict.
        
        # Parse the values for A and B
        day_a, slot_a = a
        day_b, slot_b = b

        if day_a == day_b and slot_a == slot_b:
            # print("Same day and slot")
            return False
        
        # Courses that both have labs cannot be on the same day
        if day_a == day_b and course_a.has_lab and course_b.has_lab:
            # print("Same day and both have labs")
            return False
        
        # Cases for overlapping slots
        if day_a == day_b and course_a.has_lab and slot_a == '9-3' and (slot_b == '9-12' or slot_b == '12-3'):
            # print("Same day and overlapping slots 1")
            return False
        
        if day_a == day_b and course_a.has_lab and slot_a == '12-6' and (slot_b == '12-3' or slot_b == '3-6'):
            # print("Same day and overlapping slots 2")
            return False
        
        if day_a == day_b and course_b.has_lab and slot_b == '9-3' and (slot_a == '9-12' or slot_a == '12-3'):
            # print("Same day and overlapping slots 3")
            return False

        if day_a == day_b and course_b.has_lab and slot_b == '12-6' and (slot_a == '12-3' or slot_a == '3-6'):
            return False

        # Constraint 3: Courses of the same semester on different days
        if course_a.semester == course_b.semester and day_a == day_b:
            # print("Same day and overlapping slots 4")
            return False

        # Constraint 5: Difficult courses need a gap of 2 days
        if course_a.difficult == True and course_b.difficult == True:
            # print("Difficult courses")
            if abs(day_a - day_b) < 2:
                return False

        # Constraint 6: Same teacher courses on different days
        if course_a.teacher == course_b.teacher and day_a == day_b:
            # print("Same teacher")
            return False

        return True
    return timetabling_constraints

class Course:
    def __init__(self, course_name, teacher, semester, difficult, has_lab):
        # Initialize the attributes
        self.course_name = course_name
        self.teacher = teacher
        self.semester = semester
        self.difficult = difficult
        self.has_lab = has_lab


    def display_course_info(self):
        print(f"Course: {self.course_name}")
        print(f"Teacher: {self.teacher}")
        print(f"Semester: {self.semester}")
        print(f"Difficult: {self.difficult}")
        print(f"Has Lab: {self.has_lab}")

def print_solution(solution):
    days = 1
    while days < 22:
        print (f"Day {days}")
        for key in solution:
            if solution[key][0] == days:
                print(key, solution[key])
                # solution3.pop(key)
        days += 1
        print("\n")

def check_solution(solution, course_map):
    days = 1
    previous_day_difficult = False  # Initialize as False, indicating no difficult course on the previous day.
    
    while days < 22:
        day_courses = []
        slots = []
        
        # Collect courses and their corresponding slots for the current day
        for key in solution:
            if solution[key][0] == days:
                day_courses.append(course_map[key])
                slots.append(solution[key][1])
        
        # Combine courses and slots into tuples
        course_slot_pairs = [(course, slot) for course, slot in zip(day_courses, slots)]
        
        if previous_day_difficult:
            for course, slot in course_slot_pairs:
                if course.difficult:
                    print("Difficult courses on consecutive days!")
                    return False  # Return false if there are difficult courses on consecutive days
        
        # Mark if any course in this day is difficult, to check for the next day
        previous_day_difficult = any(course.difficult for course, _ in course_slot_pairs)

        # Check for constraints within the same day
        for i in range(len(course_slot_pairs)):
            for j in range(i + 1, len(course_slot_pairs)):
                course_i, slot_i = course_slot_pairs[i]
                course_j, slot_j = course_slot_pairs[j]
                if slot_i == slot_j:
                    return False
            
                if course_i.teacher == course_j.teacher or course_i.semester == course_j.semester:
                    return False
                
                if course_i.difficult and course_j.difficult:
                    return False
        
        days += 1
    
    return True


# Read the data
data = pd.read_csv('h3-data.csv')
# print (data)

# Create a list to store the courses
courses = []

for index,row in data.iterrows():
    course = Course(row['Μάθημα'], row['Καθηγητής'], row['Εξάμηνο'], row['Δύσκολο (TRUE/FALSE)'], row['Εργαστήριο (TRUE/FALSE)'])
    courses.append(course)

# for course in courses:
#     course.display_course_info()

# Map course names to Course objects for easy reference
course_map = {course.course_name: course for course in courses}
# for course in course_map:
#     print(course, ':', course_map[course].teacher)

variables = [course.course_name for course in courses]

# Mapping of slot numbers to their hour ranges for 3-hour slots
simple_slot = {1: '9-12', 2: '12-3', 3: '3-6'}

# Mapping of starting slots to their hour ranges for 6-hour slots
lab_slot = {1: '9-3', 2: '12-6'}

domains = {
        course.course_name: (
        [
            (day, simple_slot[slot]) for day in range(1, 22) for slot in range(1, 4)
        ] if not(course.has_lab) else
        [
            (day, lab_slot[slot]) for day in range(1, 22) for slot in range(1, 3)
        ]
    )
    for course in courses
}

# for domain in domains:  
#     print(domain, ':', domains[domain])

neighbors = {
    course.course_name: [other.course_name for other in courses if course != other]
    for course in courses
}

constraints = make_constraints(course_map)
# Create the CSP object

# Mac method
timetabling = CSP(variables, domains, neighbors, constraints)
start_time = time.time()
mac_mrv = backtracking_search(timetabling,select_unassigned_variable=mrv, inference=mac)
end_time = time.time()
elapsed_time = end_time - start_time
print("-----------------------------------------")
print('Expanded:', timetabling.expanded)    
print('Checks:', timetabling.checks)
print("Time taken for mac and mrv: ", elapsed_time, "seconds")
print("Solution with mac and mrv")
print_solution(mac_mrv)
if check_solution(mac_mrv, course_map):
    print("Solution using mac and mrv is valid")
print("-----------------------------------------")
print("\n\n")

timetabling = CSP(variables, domains, neighbors, constraints)
start_time = time.time()
mac_dom_wdeg = backtracking_search(timetabling,select_unassigned_variable=dom_wdeg, inference=mac)
end_time = time.time()
elapsed_time = end_time - start_time
print("-----------------------------------------")
print('Expanded:', timetabling.expanded)    
print('Checks:', timetabling.checks)
print("Time taken for mac and dom_wdeg: ", elapsed_time, "seconds")
print("Solution with mac and dom_wdeg")
print_solution(mac_dom_wdeg)
if check_solution(mac_dom_wdeg, course_map):
    print("Solution using mac and dom_wdeg is valid")
print("-----------------------------------------")
print("\n\n")

# Forward checking method
timetabling = CSP(variables, domains, neighbors, constraints)
start_time = time.time()
fc_mrv = backtracking_search(timetabling,select_unassigned_variable=mrv, inference=forward_checking)
end_time = time.time()
elapsed_time = end_time - start_time
print("-----------------------------------------")
print('Expanded:', timetabling.expanded)    
print('Checks:', timetabling.checks)
print("Time taken for forward checking and mrv: ", elapsed_time, "seconds")
print("Solution with forward checking and mrv")
print_solution(fc_mrv)
if check_solution(fc_mrv, course_map):
    print("Solution using forward checking and mrv is valid")
print("-----------------------------------------")
print("\n\n")

timetabling = CSP(variables, domains, neighbors, constraints)
start_time = time.time()
fc_dom_wdeg = backtracking_search(timetabling,select_unassigned_variable=dom_wdeg, inference=forward_checking)
end_time = time.time()
elapsed_time = end_time - start_time
print("-----------------------------------------")
print('Expanded:', timetabling.expanded)    
print('Checks:', timetabling.checks)
print("Time taken for forward checking and dom_wdeg: ", elapsed_time, "seconds")
print("Solution with forward checking and dom_wdeg")
print_solution(fc_dom_wdeg)
if check_solution(fc_dom_wdeg, course_map):
    print("Solution using forward checking and dom_wdeg is valid")
print("-----------------------------------------")
print("\n\n")

# Min conflicts method
timetabling = CSP(variables, domains, neighbors, constraints)
start_time = time.time()
min_conflicts_sol = min_conflicts(timetabling)
end_time = time.time()
elapsed_time = end_time - start_time
print('Expanded:', timetabling.expanded)
print("-----------------------------------------")
print('Expanded:', timetabling.expanded)    
print('Checks:', timetabling.checks)
print("Time taken for min_conflicts: ", elapsed_time, "seconds")
print("Solution with min_conflicts")
print_solution(min_conflicts_sol)
if check_solution(min_conflicts_sol, course_map):
    print("Solution using min_conflicts is valid")
print("-----------------------------------------")
print("\n\n")