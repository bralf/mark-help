# mark-help

### Some python code and shell scripts to aid with Moodle/Engage preprocessing.

## Important files:

- preprocess.sh preprocesses the folder containing the submission folders and creates a file, partIDs.txt, which contains a list of all the participant IDs. It also creates a new folder, 2-Flat which is a flattened folder of all the submissions.
- make-mark-sheets.py, using partIDs.txt, creates an Excel workbook, grades.xlsx, which contains a template marking sheet and a copy of the template for each participant
- the folder 1-Unmarked currently contains some (fake) example submissions to show functionality.

## Version 0.1 instructions:

1. Download submission folders and gradesheet (in csv format) from Moodle/Engage
2. Put the submission folders in a folder called “1-Unmarked”
3. Run preprocess.sh
4. Make sure the parameters are correct in make-mark-sheet.py
5. Run make-mark-sheet.py
6. Manually copy the csv master sheet into a new sheet and add the INDIRECT links (ask me for advice on how to do this).
7. Mark!
8. Upload the master sheet to Moodle/Engage

## TODO:

- Adapt the python code to write the master sheet too.
- Write a single .sh script which performs everything at once.
