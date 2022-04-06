
import get_input

def initialize_dataframes(filename: str):
    global df_students, df_courses
    df_students, df_courses = get_input.get_input(filename)

def baseSelectorCourses(course: str, column: str):
    row = df_courses[df_courses['Course ID'] == course]
    x = list(row[column])
    return x[0]
    
def getCreditsForCourse(course: str) -> int:
    return baseSelectorCourses(course, 'Credits')

def getMinStudentsForCourse(course: str) ->int:
    return baseSelectorCourses(course, 'Min Students')

def getMaxStudentsForCourse(course: str) -> int:
    return baseSelectorCourses(course, 'Max Students')

def getTimeSlotForCourse(course: str) -> int:
    return baseSelectorCourses(course, 'Time Slot')

def getAllCourses():
    return list(df_courses['Course ID'].values)

def getNumberOfStudentInCourse(dictionary, course: str)-> int:
    return len(dictionary[course])

def baseSelectorStudent(student: str, column: str):
    row = df_students[df_students['Student ID'] == student]
    return list(row[column])[0]

def getCreditsRequiredForStudent(student: str) -> int:
    return baseSelectorStudent(student, 'Credits Required')

def getListOfPreferedCourses(student: str) -> list:
    row = df_students[df_students['Student ID'] == student]
    return list(row.iloc[0].values[2:])
    
def getAllStudents():
    return list(df_students['Student ID'].values)

def getTotalCreditsForStudent(solution: dict, student: str) -> int:
    amount = 0
    for course in solution[student]:
        amount += getCreditsForCourse(course)
    return amount

def getFirstUnenrolledCourse(student, courses):
    pref = getListOfPreferedCourses(student)
    for elem in pref:
        if elem not in courses:
            return elem
    return None

