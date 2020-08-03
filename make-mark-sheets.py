import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell, xl_cell_to_rowcol, xl_range
import csv

# Assignment dependent data
participant_path = 'PartIDs.txt' #Participant IDs
questions = ([1.1,5],[1.2,6],[2.1,4],[2.2,5]) #Questions and marks
codes = ([0,0,"Question not attempted or totally wrong"], #Code, percent awarded, description
         [1,25,"Partial credit, still wrong"],
         [2,50,"Pass mark, question understood"],
         [3,75,"Silly mistake"],
         [4,100,"All correct"])

# Parameters
sheet_tl = '$A$1' #Top left corner of the grades
codes_tl = '$J$2' #Top left corner of the mark codes box.

# Creates the workbook
workbook = xlsxwriter.Workbook('grades.xlsx')

# Adds a master sheet
master = workbook.add_worksheet('master')
with open('master.csv', 'r') as f:
    reader = csv.reader(f)
    for r, row in enumerate(reader):
        for c, col in enumerate(row):
            master.write(r, c, col)


# Creates a template sheet and a sheet for each participant
template = workbook.add_worksheet('template')
participants = []
with open(participant_path) as inputfile:
    for line in inputfile:
        participants.append(int(line.strip()))

worksheets = []
for i in participants:
    worksheets.append(workbook.add_worksheet(str(i)))

for worksheet in workbook.worksheets():

    if worksheet.get_name() == 'master':
        continue

    (trow,lcol) = xl_cell_to_rowcol(sheet_tl)
    # Adds column headings to each sheet
    worksheet.write(trow, lcol, "Question")
    worksheet.write(trow, lcol+1, "Code")
    worksheet.write(trow, lcol+2, "Marks")
    worksheet.write(trow, lcol+4, "Max")
    worksheet.write(trow, lcol+5, "Feedback")
    worksheet.write(trow, lcol+6, "Formatted Feedback")

    # Adds mark codes lookup information
    (codes_row, codes_col) = xl_cell_to_rowcol(codes_tl)
    codes_br = xl_rowcol_to_cell(codes_row+len(codes), codes_col+1, row_abs=True, col_abs=True)
    worksheet.write(codes_row, codes_col, "Code")
    worksheet.write(codes_row, codes_col + 1, "%")
    codes_row += 1
    for code, percent, comment in (codes):
        col = codes_col
        worksheet.write(codes_row, col, code)
        col += 1
        worksheet.write(codes_row, col, percent)
        col += 1
        worksheet.write(codes_row, col, comment)
        codes_row += 1

    # Adds question rows
    row = trow+1
    for question, max in (questions):
        q_cell = xl_rowcol_to_cell(row, lcol)
        code_cell = xl_rowcol_to_cell(row, lcol+1)
        mark_cell = xl_rowcol_to_cell(row, lcol+2)
        max_cell = xl_rowcol_to_cell(row, lcol+4)
        fb_cell = xl_rowcol_to_cell(row, lcol + 5)
        worksheet.write(row, lcol, question)
        worksheet.write_formula(row,2, f'=VLOOKUP({code_cell},{codes_tl}:{codes_br},2,FALSE)/100*{max_cell}')
        worksheet.write(row, lcol+3, "/")
        worksheet.write(row, lcol+4, max)
        worksheet.write_formula(row, lcol+6, f'=_xlfn.CONCAT("Q",{q_cell},": ",{mark_cell},"/",{max_cell}," ",{fb_cell},"<br>")')
        row += 1

    # Add Totals
    mark_range = xl_range(trow+1,lcol+2,row-1,lcol+2)
    st_cell = xl_rowcol_to_cell (row, lcol+2)
    mod_cell = xl_rowcol_to_cell (row+1, lcol+2)
    fb_range = xl_range(trow+1, lcol+6, row-1, lcol+6)
    row+=1
    worksheet.write(row, lcol, 'Subtotal')
    worksheet.write_formula(row, lcol+2, f'=SUM({mark_range})')
    row+=1
    worksheet.write(row, lcol, 'Modifier')
    worksheet.write(row, lcol+2, 0)
    row+=1
    worksheet.write(row, lcol, 'Total')
    worksheet.write_formula(row, lcol+2, f'=_xlfn.CEILING.MATH({st_cell}+{mod_cell})')
    worksheet.write(row-1,lcol+6, 'Total Feedback')
    worksheet.write_formula(row,lcol+6,f'=_xlfn.CONCAT({fb_range})')


workbook.close()
