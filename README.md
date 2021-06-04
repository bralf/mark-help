# mark-help

### Some python code and shell scripts to aid with Moodle/Engage preprocessing.

## Important files:

- preprocess.sh preprocesses the folder containing the submission folders and creates a file, partIDs.txt, which contains a list of all the participant IDs. It also creates a new folder, 2-Flat which is a flattened folder of all the submissions.
- make-mark-sheets.py, using partIDs.txt, creates an Excel workbook, grades.xlsx, which contains a template master gradesheet, an analysis sheet with question-by-question statistics and a copy of the template for each participant.
- the folder 1-Unmarked currently contains some (fake) example submissions to show functionality.
- the spreadsheet master.csv currently is an example master sheet, corresponding to 1-Unmarked, to show functionality.

## Version 0.4 instructions:

1. Download submission folders and gradesheet (in csv format) from Moodle/Engage.
2. Put the submission folders in a folder called “1-Unmarked".
3. Run "./preprocess.sh" in the terminal.
4. Make sure the parameters are correct in make-mark-sheet.py.
5. Make sure the master csv file is named "master.csv". It is advised to delete non-submissions from here and sort by Participant ID.
5. Run "python make-mark-sheet.py" in the terminal.
7. Mark, entering grades and feedback into the sheet corresponding to each student ID.
9. Copy and past the mark and feedback columns from the 'master' sheet of "grades.xlxs" to "master.csv".
10. Upload the "master.csv" to Moodle/Engage.

## TODO:

- Tweak endlessly...
