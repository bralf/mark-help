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
(trow, lcol) = (0,0) #Top left corner of the grades
(trow_codes, lcol_codes)= (1,9) #Top left corner of the mark codes box.

#Creates a list of participants witb submissions
participants = []
with open(participant_path) as inputfile:
    for line in inputfile:
        participants.append(line.strip())
par_num = len(participants)

# Creates the workbook
workbook = xlsxwriter.Workbook('grades.xlsx')

#Formatting
bold = workbook.add_format({'bold': 1})

# Creates a master sheet
master = workbook.add_worksheet('master')

# Creates a template sheet
template = workbook.add_worksheet('template')

# Creates a sheet for each participant
worksheets = []
for p in participants:
    worksheets.append(workbook.add_worksheet(p))

total_cell    = xl_rowcol_to_cell(len(questions)+4,lcol+2)
total_fb_cell = xl_rowcol_to_cell(len(questions)+4,lcol+6)

# Writes master sheet
with open('master.csv', 'r') as f:
    reader = csv.reader(f)
    for r, row in enumerate(reader):
        r1 = xl_rowcol_to_cell(r,1)
        master.write_formula(r,0,f'=RIGHT({r1},4)')
        for c, col in enumerate(row):
            if (r == 0):
                master.write(r, c+1, col,bold)
            elif col.isdigit():
                master.write(r, c+1,int(col))
            else:
                master.write(r, c+1, col)
        if ((row[1][0:9] == "Submitted") | (row[1][0:5] == "Draft")):
            id = xl_rowcol_to_cell(r,0)
            master.write_formula(r,3,f'=INDIRECT({id} & \"!{total_cell}\")')
            master.write_formula(r,8,f'=INDIRECT({id} & \"!{total_fb_cell}\")')
    master.write('A1',"ID",bold)

#Writes template and participant sheets
for worksheet in workbook.worksheets():

    if worksheet.get_name() == 'master':
        continue

    # Adds column headings to each sheet
    worksheet.write(trow, lcol,   "Question",bold)
    worksheet.write(trow, lcol+1, "Code",bold)
    worksheet.write(trow, lcol+2, "Marks",bold)
    worksheet.write(trow, lcol+4, "Max",bold)
    worksheet.write(trow, lcol+5, "Feedback",bold)
    worksheet.write(trow, lcol+6, "Formatted Feedback",bold)

    # Adds mark codes lookup information
    (codes_row,codes_col) = (trow_codes,lcol_codes)
    codes_br = xl_rowcol_to_cell(codes_row+len(codes), codes_col+1, row_abs=True, col_abs=True)
    worksheet.write(codes_row, codes_col, "Code",bold)
    worksheet.write(codes_row, codes_col + 1, "%",bold)
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
        codes_range = xl_range(trow_codes,lcol_codes,trow_codes+len(codes), lcol_codes+1)
        worksheet.write(row, lcol, question)
        worksheet.write_formula(row,2, f'=ROUND(VLOOKUP({code_cell},{codes_range},2,FALSE)/100*{max_cell},0)')
        worksheet.write(row, lcol+3, "/")
        worksheet.write(row, lcol+4, max)
        worksheet.write_formula(row, lcol+6, f'=_xlfn.CONCAT("Q",{q_cell},": ",{mark_cell},"/",{max_cell}," ",{fb_cell},"<br>")')
        row += 1

    # Add Totals
    mark_range = xl_range(trow+1,lcol+2,row-1,lcol+2)
    st_cell = xl_rowcol_to_cell (row+1, lcol+2)
    mod_cell = xl_rowcol_to_cell (row+2, lcol+2)
    fb_range = xl_range(trow+1, lcol+6, row-1, lcol+6)
    row+=1
    worksheet.write(row, lcol, 'Subtotal',bold)
    worksheet.write_formula(row, lcol+2, f'=SUM({mark_range})')
    row+=1
    worksheet.write(row, lcol, 'Modifier',bold)
    worksheet.write(row, lcol+2, 0)
    row+=1
    worksheet.write(row, lcol, 'Total',bold)
    worksheet.write_formula(row, lcol+2, f'=_xlfn.CEILING.MATH({st_cell}+{mod_cell})')
    worksheet.write(row-1,lcol+6, 'Total Feedback',bold)
    worksheet.write_formula(row,lcol+6,f'=_xlfn.CONCAT({fb_range})')

workbook.close()
