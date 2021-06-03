import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell, xl_cell_to_rowcol, xl_range
import csv

# Assignment dependent data
questions = ([1.1,5],[1.2,6],[2.1,4],[2.2,5])
marking_codes = ([0,0,"Question not attempted or totally wrong"], # Code, percent awarded, description
         [1,25,"Partial credit, still wrong"],
         [2,50,"Pass mark, question understood"],
         [3,75,"Silly mistake"],
         [4,100,"All correct"])

class Assignment:
    def __init__(self,p_path='PartIDs.txt', m_path='master.csv',qs=questions,m_codes=marking_codes):
        self.participant_path = p_path
        self.master_path = m_path
        self.questions = qs
        self.marking_codes = m_codes

#Creates a list of participants witb submissions
        
    def genPartList(self):
        participants = []
        with open(self.participant_path) as inputfile:
            for line in inputfile:
                participants.append(line.strip())
        self.par_num   = len(participants)
        self.id_length = len(participants[0])
        return participants
    
#Creates a workbook with a master sheet, template sheet and sheets for each participant

    def create_workbook(self,participants):
        workbook = xlsxwriter.Workbook('grades.xlsx')
        self.master = workbook.add_worksheet('master')
        self.template = workbook.add_worksheet('template')
        self.worksheets = []
        for p in participants:
            self.worksheets.append(workbook.add_worksheet(p))
        self.bold = workbook.add_format({'bold': 1})    
        return workbook

    # Writes the master sheet

    def write_master(self,workbook,lcol):
        total_cell    = xl_rowcol_to_cell(len(self.questions)+4,lcol+2)
        total_fb_cell = xl_rowcol_to_cell(len(self.questions)+4,lcol+6)
        with open(self.master_path, 'r') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                r1 = xl_rowcol_to_cell(r,1)
                self.master.write_formula(r,0,f'=RIGHT({r1},{self.id_length})')
                for c, col in enumerate(row):
                    if (r == 0):
                        self.master.write(r, c+1, col,self.bold)
                    elif col.isdigit():
                        self.master.write(r, c+1,int(col))
                    else:
                        self.master.write(r, c+1, col)
                if ((row[1][0:9] == "Submitted") | (row[1][0:5] == "Draft")):
                    id = xl_rowcol_to_cell(r,0)
                    self.master.write_formula(r,3,f'=INDIRECT({id} & \"!{total_cell}\")')
                    self.master.write_formula(r,8,f'=INDIRECT({id} & \"!{total_fb_cell}\")')
        self.master.write('A1',"ID",self.bold)
        return workbook

    def write_grade_sheets(self,workbook,trow,lcol,trow_codes,lcol_codes):
        for worksheet in workbook.worksheets():

            if worksheet.get_name() == 'master':
                continue

            # Adds column headings to each sheet
            worksheet.write(trow, lcol,   "Question",self.bold)
            worksheet.write(trow, lcol+1, "Code",self.bold)
            worksheet.write(trow, lcol+2, "Marks",self.bold)
            worksheet.write(trow, lcol+4, "Max",self.bold)
            worksheet.write(trow, lcol+5, "Feedback",self.bold)
            worksheet.write(trow, lcol+6, "Formatted Feedback",self.bold)

            # Adds mark codes lookup information
            (codes_row,codes_col) = (trow_codes,lcol_codes)
            codes_br = xl_rowcol_to_cell(codes_row+len(self.marking_codes), codes_col+1, row_abs=True, col_abs=True)
            worksheet.write(codes_row, codes_col, "Code",self.bold)
            worksheet.write(codes_row, codes_col + 1, "%",self.bold)
            codes_row += 1
            for code, percent, comment in (self.marking_codes):
                col = codes_col
                worksheet.write(codes_row, col, code)
                col += 1
                worksheet.write(codes_row, col, percent)
                col += 1
                worksheet.write(codes_row, col, comment)
                codes_row += 1

            # Adds question rows
            row = trow+1
            for question, max in (self.questions):
                q_cell = xl_rowcol_to_cell(row, lcol)
                code_cell = xl_rowcol_to_cell(row, lcol+1)
                mark_cell = xl_rowcol_to_cell(row, lcol+2)
                max_cell = xl_rowcol_to_cell(row, lcol+4)
                fb_cell = xl_rowcol_to_cell(row, lcol + 5)
                codes_range = xl_range(trow_codes,lcol_codes,trow_codes+len(self.marking_codes), lcol_codes+1)
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
            worksheet.write(row, lcol, 'Subtotal',self.bold)
            worksheet.write_formula(row, lcol+2, f'=SUM({mark_range})')
            row+=1
            worksheet.write(row, lcol, 'Modifier',self.bold)
            worksheet.write(row, lcol+2, 0)
            row+=1
            worksheet.write(row, lcol, 'Total',self.bold)
            worksheet.write_formula(row, lcol+2, f'=_xlfn.CEILING.MATH({st_cell}+{mod_cell})')
            worksheet.write(row-1,lcol+6, 'Total Feedback',self.bold)
            worksheet.write_formula(row,lcol+6,f'=_xlfn.CONCAT({fb_range})')
        return workbook

def main ():
    assignment = Assignment()
    participants = assignment.genPartList()
    (trow, lcol) = (0,0) #Top left corner of the grades
    (trow_codes, lcol_codes) = (1,9) #Top left corner of the mark codes box.
    workbook = assignment.create_workbook(participants)
    workbook = assignment.write_master(workbook,lcol)
    workbook = assignment.write_grade_sheets(workbook,trow,lcol,trow_codes,lcol_codes)
    workbook.close()

if __name__ == "__main__":
    main()
