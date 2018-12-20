#!/usr/bin/python3
'''
File name: createGradeFiles.py
Author: Mark Wisink
Python Version: 3.7
Purpose: Automatically creates grade/feedback files for students from the csv grade file
'''
import argparse
import collections
import statistics
import glob
import csv
import io
import os

parser = argparse.ArgumentParser(description='Creates grade files for students based on csv')
parser.add_argument(
    'lab',
    metavar='L',
    help='the lab number'
)
parser.add_argument(
    'csv_path',
    metavar='P',
    default='~/Grading.csv'
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
parser.add_argument(
    '--s',
    dest='section_list_path',
    default=os.path.dirname(os.path.realpath(__file__)) + '/SectionList.txt',
    help='The section list file - it will default to SectionList.txt in the same directory as gradeFile.py'
)

args = parser.parse_args()

# This function might have to be modified to find the correct directory
def get_gradefile(student):
    # print(os.getcwd() + student + '/Grades/lab' + args.lab + '.txt')
    return os.getcwd() + '/' + student + '/Grades/lab' + args.lab + '.txt'

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

print('Compiling Sections')
sections = [collections.OrderedDict()]
# Ensure you have a SectionList.csv file in the same directory as the gradeFiles.py
# This SectionList file should list students in each section where each columns represents a section
with open(args.section_list_path, 'r', newline='') as section_list:
    current_section = 0
    students = section_list.readlines()
    for student in students:
        sanitized_student = student.strip()
        if sanitized_student == '':
            sections.append(collections.OrderedDict())
            current_section += 1
        else:
            sections[current_section][sanitized_student] = 'missing'

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

# Create the grade file for students
# Store all the grades in an array for calculating things
grades = {}
for student in students:
    grade = 100
    grade_file = None
    try:
        grade_file = open(get_gradefile(student), 'w')
    except:
        print('Couldn\'t find directory for', student)
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
    # Add the grade to the sections list
    for section in sections:
        if student in section.keys():
            section[student] = grade
            # Might be bad storing grade twice... But we need it for calculations
            grades[student] = grade

# Print the grades so we can copy and paste them into the Google sheets document
print('\nGrades')
for section in sections:
    print('\nSection', sections.index(section) + 1)
    for grade in section.values():
        print(grade)

# Create the grade report summary
max_score = max(grades.values())
med_score = statistics.median(grades.values())
min_score = min(grades.values())
max_student = None
med_student = None
min_student = None
# Find the max, med, and min students
for student in students:
    if grades[student] == max_score && max_student is None:
        max_student = student
        continue
    if grades[student] == med_score && med_student is None:
        med_student = student
        continue
    if grades[student] == min_score && min_student is None:
        min_student = student
        continue

def get_report(outfile, student, score):
    student_report = score + ': ' + student + '\nGRADE: ' + grades[student] + '\nFEEDBACK: '
    errors = ''
    for row in students[student]:
        if row['error'] != '':
            location = row['location'] + ' : ' if row['location'] else ''
            errors += location + row['error'] + '\n'
    if errors == '':
        errors = 'none\n'
    outfile.write(student_report + errors + '\nCODE:\n')
    # Get all the files the student wrote
    student_dir = os.getcwd() + '/' + student + '/[lL]ab0?' + args.lab + '/'
    h_files = glob.glob(student_dir + '*.h')
    cpp_files = glob.glob(student_dir + '*.cpp')
    for fname in h_files + cpp_files:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

divider = '\n\n============================================================\n\n'
with open('~/grade' + args.lab + 'report.txt', 'w') as report_file:
    report_file.write(get_report(report_file, max_student, 'MAX'))
    report_file.write(divider)
    report_file.write(get_report(report_file, med_student, 'MEDIAN'))
    report_file.write(divider)
    report_file.write(get_report(report_file, min_student, 'MIN'))
