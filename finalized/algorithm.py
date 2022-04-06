# import libraries
import pandas as pd
import random
from collections import defaultdict
from typing import Iterable, List, Set, Iterator

# import extra functions
from get_functions import *

def assign_students_by_preference():
    """Generate a first try of a solution based on preference lists.
    """
    # Keep track of students that need to be distributed
    to_be_distributed = getAllStudents()
    random.shuffle(to_be_distributed)
    to_be_distributed.sort(key=student_sort_function)

    # Get dict of iterators of preferred courses
    preferences = dict((s_id, iter(getListOfPreferedCourses(s_id))) for s_id in to_be_distributed) 

    # Every student gets their most preferred courses if available
    while to_be_distributed:
        s_id = to_be_distributed[0]

        available_course = next_preferred_course(s_id, preferences[s_id])

        if available_course: # If there is an available course, use it
            add_student_course(s_id, available_course)

            if credits_needed(s_id) <= 0: to_be_distributed.remove(s_id) # Get rid of student with enough credits

        else: # If there is no available course, move the student
            to_be_distributed.remove(s_id)
            not_enough_credits.append(s_id)

# Fix all students
def assign_students(students_left: List[str], underfilled_courses: List[str]):
    
    while students_left:
        s_id = students_left.pop(0)

        if underfilled_courses: # some courses are underfilled
            
            for c_id in underfilled_courses:
                if c_id not in sol_students[s_id]: # find first underfilled course
                    
                    add_student_course(s_id, c_id) # add student to the course
                    
                    if credits_needed(s_id) > 0: # student still needs credits
                        students_left.append(s_id)
                        
                    if getMinStudentsForCourse(c_id) <= len(sol_courses[c_id]): # Course has enough students
                        underfilled_courses.remove(c_id)
                    break
        else: # all courses are filled
            
            for c_id in sol_courses.keys():
                # find first course that is not full
                if is_available(c_id, s_id):
                    add_student_course(s_id, c_id)
                    break
            
            if credits_needed(s_id) > 0: # Student still needs credits
                students_left.append(s_id)
        

# While there still are underfilled courses, fix this
def fix_underfilled_courses():
    """Make sure all courses have enough students.
    """
    while not_enough_students:
        removed_course = not_enough_students.pop(0) # Pick the course to remove
        new_students = sol_courses[removed_course] # Find the students in this course
        for s_id in new_students: remove_student_course(s_id, removed_course) # Delete connections between students/course
        delete_course(removed_course) # Remove the course from the solution

        not_enough_credits = list(st for st in new_students if getCreditsRequiredForStudent(st) < sum_credits(sol_students[st]))
        assign_students(not_enough_credits, not_enough_students)
        fix_overloaded_students()

def get_timeslots(courses: Iterable[str]) -> Set[int]:
    """Return the timeslots for the given courses.
    """
    return set(getTimeSlotForCourse(c_id) for c_id in courses)

def sum_credits(courses: Iterable[str]) -> int:
    """Return the total amount of credits for the given courses.
    """
    if courses:
        return sum(getCreditsForCourse(course) for course in courses)
    else: 
        return 0

def next_preferred_course(s_id: str, preferences: Iterator[str]) -> str:
    """Return the next course in the preffered list that is available, otherwise None.
    """
    next_course = next(preferences, None)
    if next_course:
        if is_available(next_course, s_id):
            return next_course
        else:
            return next_preferred_course(s_id, preferences)
    else:
        return None

def add_student_course(s_id: str, c_id: str) -> None:
    """Add a student to a course and the course to the students list.
    """
    sol_students[s_id].append(c_id)
    sol_courses[c_id].append(s_id)

def remove_student_course(s_id: str, c_id: str) -> None:
    """Remove a student-course pair.
    """
    sol_students[s_id].remove(c_id)
    sol_courses[c_id].remove(s_id)
    
def credits_assigned(s_id) -> int:
    """Return the amount of assigned credits for the student.
    """
    return sum_credits(sol_students[s_id])
    
def credits_needed(s_id: str) -> int:
    """Return how many credits a student still needs.
    """
    return getCreditsRequiredForStudent(s_id) - credits_assigned(s_id)

def delete_course(c_id: str) -> None:
    """Delete a course from the solutions.
    """
    for s_id in sol_courses[c_id]: # remove the course from the students' lists
        sol_students[s_id].remove(c_id)
    
    del sol_courses[c_id] # remove the course from the course list

def is_available(c_id: str, s_id: str) -> bool:
    """Return whether the course is available for the student.
    """
    return getTimeSlotForCourse(c_id) not in get_timeslots(sol_students[s_id]) and len(sol_courses[c_id]) < getMaxStudentsForCourse(c_id)

def fix_overloaded_students() -> None:
    """Remove the last course in a students list that is not needed for their credits.
    """
    for s_id in sol_students.keys():
        index = len(sol_students[s_id])-1
        needed = credits_needed(s_id)
        while needed < 0 and index >= 0:
            if getCreditsForCourse(sol_students[s_id][index]) <= -needed:
                remove_student_course(s_id, sol_students[s_id][index])
                needed = credits_needed(s_id)
            index -= 1

def get_not_enough_credits():
    """Return a list of students who do not have enough credits.
    """
    return [s_id for s_id in getAllStudents() if credits_needed(s_id) > 0]

def get_not_enough_students():
    """Return a list of courses which do not have enough students.
    """
    return list(filter(lambda c_id: len(sol_courses[c_id]) < getMinStudentsForCourse(c_id), sol_courses.keys()))

def student_sort_function(s_id):
    """Return the score to sort a student by;
    the lowest score will be sorted first.
    """
    return -getCreditsRequiredForStudent(s_id)

def create_solution(filename: str):
    """Create a full solution.
    """
    global sol_students, sol_courses, not_enough_students, not_enough_credits
    
    initialize_dataframes(filename)

    # initialize all variables
    sol_students = defaultdict(list)
    sol_courses = defaultdict(list)
    not_enough_credits = get_not_enough_credits()
    not_enough_students = get_not_enough_students()
    
    # begin the algorithm
    assign_students_by_preference()

    fix_overloaded_students()
    
    not_enough_credits = get_not_enough_credits()
    not_enough_students = get_not_enough_students()
    
    assign_students(not_enough_credits, not_enough_students)
    
    fix_overloaded_students()
    fix_underfilled_courses()
    
    # return the solution in dictionary form
    return dict(sol_students), dict(sol_courses)
def HappinessList(n:int) :
    """Creates a list which we will use to give the happiness values. [8, .., 1] by default but you can change this to be anything"""
    return [8-i for i in range(n)]

def HappinessMeter(solution) -> int:
    """Calculates the total happiness for a given solution in dictionary form (dictionary with courses as the keys)"""
    key_list = list(solution)
    TotalHappiness = 0
    for i in range(len(solution)):
        HappinessCounter = 0
        for j in range(len(solution[key_list[i]])):
            index = np.where(df_students["Student ID"] == solution[key_list[i]][j])[0][0]
            if list(np.where(df_students.loc[index] == key_list[i])[0]) == []:
                points = -1  #-1 by default, but we can change this
            else:
                pointscolumn = min(np.where(df_students.loc[index] == key_list[i])[0])
                points = HappinessList(len(df_students.loc[0])-2)[pointscolumn-2]
            HappinessCounter = HappinessCounter + points
        
        TotalHappiness = TotalHappiness + HappinessCounter
    return   TotalHappiness
        
Happystats = []
best_crs = sol_courses #simply for the sake of having an innitial comparison point

for i in range(10):  #Loops and keeps the best 
    print(i)
    #make a new solution
    sol_students = defaultdict(list)
    sol_courses = defaultdict(list)
    not_enough_credits = get_not_enough_credits()
    not_enough_students = get_not_enough_students()
    sol_students, sol_courses = create_solution()
    #grade the solution
    happy = HappinessMeter(sol_courses)
    Happystats += [happy]
    #store the best solution
    if happy > HappinessMeter(best_crs):
        best_crs = sol_courses
        best_stu = sol_students
        
#I dont want to change the names and cause problems, so lets rename them back
sol_courses = best_crs 
sol_students = best_stu

def output_solution(sol_students, sol_courses, filename: str = 'algorithm'):
    """Write the solution dictionaries (students, courses) to an Excel file.
    """

    df_courses = pd.DataFrame(dict([(c_id, pd.Series(students)) for c_id, students in sol_courses.items()]))
    df_students = pd.DataFrame(dict([(s_id, pd.Series(courses)) for s_id, courses in sol_students.items()]))

    with pd.ExcelWriter(f'./data/{filename}_output.xlsx') as writer:
        df_courses.to_excel(writer, sheet_name='Courses', index=False)
        df_students.transpose().to_excel(writer, sheet_name='Students')
