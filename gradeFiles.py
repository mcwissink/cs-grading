'''
File name: createGradeFiles.py
Author: Mark Wisink
Python Version: 3.7
Purpose: Automatically creates grade/feedback files for students from the csv grade file
'''
import argparse
import csv
import io

parser = argparse.ArgumentParser(description='Creates feed back files for students based on csv')
parser.add_argument(
    'lab',
    metavar='L',
    help='the lab number'
)
parser.add_argument(
    'csv_path',
    metavar='P',
    help='the path to the csv, expected column format: (student, error, location, points, feedback)'
)
parser.add_argument(
    '--m',
    dest='success_message',
    default='Great job!',
    help='A message to display to successful students'
)
parser.add_argument(
    '--d',
    dest='delete_files',
    action='store_true',
    help='Delete the grade files associated with the lab number'
)

args = parser.parse_args()

# This function has to be modified to find the correct directory
def get_gradefile(student):
    return './' + student + '/Grades/lab' + args.lab + '.txt'

if (args.delete_files):
    exit()

def deduct_points(str_points):
    if str_points == '':
        return 0
    try:
        return int(str_points)
    except ValueError:
        print(ValueError)
        return 0

print('Opening', args.csv_path)
students = {}
# Parse each row of the csv and sort them into a dictionary of students
with open(args.csv_path, 'r', newline='', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        student = row['student']
        if student == '':
            print('Invalid student', row)
            exit()
        if (student in students):
            students[student].append(row)
        else:
            students[student] = [row]

print('\nGrades')
for student in students:
    grade = 100
    grade_file = None
    try:
        grade_file = open(get_gradefile(student), 'w')
    except:
        continue

    # Write the errors
    grade_file.write('Lab ' + args.lab + '\n\nErrors\n')
    errors = ''
    for row in students[student]:
        # Deduct the points from the grade
        grade -= deduct_points(row['points'])
        if row['error'] != '':
            location = row['location'] + ' : ' if row['location'] else ''
            errors += location + row['error'] + '\n'
    if errors == '':
        errors = 'none\n'
    grade_file.write(errors)

    # Write the feedback
    grade_file.write('\nFeedback\n')
    feedback = ''
    for row in students[student]:
        if row['feedback'] != '':
            feedback += row['feedback'] + '\n'
    if grade == 100:
        feedback += args.success_message + '\n'
    elif feedback == '':
        feedback = 'none\n'
    grade_file.write(feedback)

    # Write the final grade
    grade_file.write('\nGrade\n' + str(grade) + '%\n')
    grade_file.close()
    print(student, grade)
