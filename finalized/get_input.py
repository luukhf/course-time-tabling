import pandas as pd

def get_input(filename: str):
    """Return dataframes of the students and courses from the file 'filename'.
    """

    df_students_original = pd.read_excel(f'./data/{filename}.xls', sheet_name='studenten')
    df_courses_original = pd.read_excel(f'./data/{filename}.xls', sheet_name='assignments')
    df_students = df_students_original.copy()
    df_courses = df_courses_original.copy()


    # CLEANING STUDENTS

    df_students.loc[0][2:] = list(map(str, range(8))) # Set column labels with happiness course preference number
    df_students.columns = df_students.iloc[0]

    df_students = df_students.drop(0) # Drop the labels of the first column
    df_students = df_students.reset_index(drop=True) # Reset the index of the first column with integer index

    clean_empty_students = df_students['Student ID'].isnull() | df_students['Credits Required'].isnull() 
    df_students = df_students[~clean_empty_students] # Detect missing values in the columns 'Student ID' and 'Credits Required'

    df_students.reset_index(drop=True) # Reset the index of the first column with integer index

    credits_num = pd.to_numeric(df_students['Credits Required']) # Convert the credits to a numeric type
    df_students['Credits Required'] = credits_num


    # CLEANING COURSES
    df_courses.columns = df_courses.iloc[0]
    df_courses = df_courses.drop(0) # Set correct column labels
    df_courses = df_courses.reset_index(drop=True) 

    clean_empty_courses = df_courses['Course ID'].isnull() # Remove empty rows
    df_courses = df_courses[~clean_empty_courses]

    df_courses.reset_index(drop = True)

    df_courses['Min Students'] = pd.to_numeric(df_courses['Min Students'])
    df_courses['Max Students'] = pd.to_numeric(df_courses['Max Students'])
    df_courses['Time Slot'] = pd.to_numeric(df_courses['Time Slot'])
    df_courses['Credits'] = pd.to_numeric(df_courses['Credits'])


    return df_students, df_courses

