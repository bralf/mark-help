# mark-help

### Some python code and shell scripts to aid with Moodle/Engage preprocessing.

## Important files:

- preprocess.sh preprocesses the folder containing the submission folders and creates a file, partIDs.txt, which contains a list of all the participant IDs. It also creates a new folder, 2-Flat which is a flattened folder of all the submissions.
- make-mark-sheets.py, using partIDs.txt, creates an Excel workbook, grades.xlsx, which contains a template master gradesheet, an analysis sheet with question-by-question statistics and a copy of the template for each participant.
- the folder 1-Unmarked currently contains some (fake) example submissions to show functionality.
- the spreadsheet master.csv currently is an example master sheet, corresponding to 1-Unmarked, to show functionality.

## Version 0.4 instructions:

**Requirements:**

- Python 3.X
- xlxswriter package for Python (can be installed with pip or conda): https://anaconda.org/anaconda/xlsxwriter
- The ability to run bash scripts (.sh files).

**Instructions:**

1. Download submission folders and gradesheet (in csv format) from Moodle/Engage.
2. Put the submission folders in a folder called “1-Unmarked".
3. Make sure the master csv file that you downloaded from Moodle/Engage is named "master.csv", and in the same folder that "1-Unmarked is in. It is advised to delete rows with non-submissions from here and sort the spreadsheet by Participant ID.
4. Run "./preprocess.sh" in the terminal.
5. You should now have a folder "2-Flat" containing all the pdfs, with filenames prefixed with the participant ID, and "PartIDs.txt" which is a text file listing all the participant IDs.
6. Make sure the parameters are correct in make-mark-sheet.py, in particular the question numbers saved to the "questions" variable near the top of the .py file (these might be obtainable from a previous run of the unit, if applicable).
7. Run "python make-mark-sheet.py" in the terminal. 
8. Mark, entering grades and feedback into the sheet corresponding to each student ID.
9. Copy and past the mark and feedback columns from the 'master' sheet of "grades.xlxs" to "master.csv".
10. Upload the "master.csv" to Moodle/Engage.

## TODO:

- Tweak endlessly...
