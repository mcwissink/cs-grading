# cs-grading
Useful scripts for grading CS 112 labs at Calvin College

## Basic Setup and Usage
Clone this repository into your calvin cs home directory. This repository contains the basic grading scripts

buildGrading.sh is the main script for compiling all the labs together so they can be processed in one place

In a terminal 
```bash
# Go to the 112 directory
cd /home/cs/112/current

# Run the grading script for lab 1
~/cs-grading/buildGrading.sh 1

# See the output file
cat ~/Documents/gradelab1/output.txt
```

For labs that involve spreadsheets, this script will also copy those files into the output directory.
buildGrading also has additional feature for other use cases

-i [usernames]: buildGrading will only run on those student submissions
-e [usernames]: buildGrading will skip these student submissions

For example, If student abc123's and def456's projects fail to compile and cause buildGrading to fail, the script can be run as follows
```bash
~/cs-grading/buildGrading.sh 1 -e abc123 def456
```

## Grading
Grading is done using Excel. By following the format provided by exampleGrading.csv, gradeFiles.py can do most of the work.

Before running the gradeFiles.py, you need to create a SectionList.txt (example found in exampleSectionList.txt) file which stores the order of the students in Moodle. This way, you can just go down the list of scores and enter them into moodle without having to find which student you are entering a score for. Unless there is a way to sort the Moodle list by firstname lastname, this seems to be the best solution.
```bash
# Go to the 112 directory
cd /home/cs/112/current

# Run the script
python3 ~/cs-grading/gradeFiles 1 /path/to/grading.csv
```

Enter the grading output into moodle

## Other
If there are any questions, enhancements, or requests, submit a pull request or create an issue
