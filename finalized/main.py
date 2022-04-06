
# run external files
from algorithm import create_solution, output_solution

filename = input('Input file name: ')

sol_students, sol_courses = create_solution(filename)

output_solution(sol_students, sol_courses, filename)