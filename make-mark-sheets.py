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
    def __init__(self,p_path='PartIDs.txt', m_path='master.csv',qs=questions,m_codes=marking_codes,trow=0,lcol=0,trow_codes=1,lcol_codes=9):
        self.participant_path = p_path
        self.master_path = m_path
        self.questions = qs
        self.marking_codes = m_codes
        self.trow = trow
        self.lcol = lcol
        self.trow_codes = trow_codes
        self.lcol_codes = lcol_codes

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
        self.workbook = xlsxwriter.Workbook('grades.xlsx')
        self.master = self.workbook.add_worksheet('master')
        self.analysis = self.workbook.add_worksheet('analysis')
        self.template = self.workbook.add_worksheet('template')
        self.worksheets = []
        for p in participants:
            self.worksheets.append(self.workbook.add_worksheet(p))
        self.bold = self.workbook.add_format({'bold': 1})    

    def write_master(self):
        (trow,lcol) = (self.trow,self.lcol)
        total_cell    = xl_rowcol_to_cell(trow+len(self.questions)+4,lcol+2)
        total_fb_cell = xl_rowcol_to_cell(trow+len(self.questions)+4,lcol+6)
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

    def write_column_headings(self,worksheet,headings):
        (trow,lcol) = (self.trow,self.lcol)
        bold = self.bold
        for n,heading in enumerate(headings):
            worksheet.write(trow,lcol+n,heading,bold)

    def write_codes_info(self,worksheet):
            (trow,lcol) = (self.trow,self.lcol)
            (codes_row,codes_col) = (self.trow_codes,self.lcol_codes)
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

    def write_question_rows(self,worksheet):
        (trow,lcol) = (self.trow,self.lcol)
        (trow_codes,lcol_codes) = (self.trow_codes,self.lcol_codes) 
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

    def write_totals(self,worksheet):
        (trow,lcol) = (self.trow,self.lcol)
        row = trow+1+len(self.questions)
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

    def write_analysis(self,participants):
        q_len = len(self.questions)
        p_len = len(participants)
        analysis = self.analysis
        bold = self.bold
        (trow,lcol) = (self.trow,self.lcol)
        self.write_column_headings(analysis,["ID"]+["Q"+str(q[0]) for q in (self.questions)]+["Total"])
        for r,part in enumerate(participants):
            analysis.write(r+1,lcol,part)
            for c in range(1,q_len+1):
                id = xl_rowcol_to_cell(r+1,0)
                q_cell = xl_rowcol_to_cell(c,2)
                analysis.write_formula(r+1,c,f'=INDIRECT({id} & \"!{q_cell}\")')
            q_range = xl_range(r+1,lcol+1,r+1,lcol+q_len)   
            analysis.write(r+1,lcol+q_len+1,f'=SUM({q_range})')    
        row = p_len+2    
        analysis.write(row,lcol,"Mean",bold)
        analysis.write(row+1,lcol,"Median",bold)
        analysis.write(row+2,lcol,"Mode",bold)
        analysis.write(row+3,lcol,"St. Dev",bold)
        for c in range(1,q_len+2):
            score_range = xl_range(trow+1,c,trow+p_len,c)
            analysis.write_formula(row,c,f'=AVERAGE({score_range})')
            analysis.write_formula(row+1,c,f'=MEDIAN({score_range})')
            analysis.write_formula(row+2,c,f'=_xlfn.MODE.SNGL({score_range})')
            analysis.write_formula(row+3,c,f'=STDEV({score_range})')
       

    def write_grade_sheets(self,worksheet):
        self.write_column_headings(worksheet,["Question","Code","Marks","","Max","Feedback","Formatted Feedback"])
        self.write_codes_info(worksheet)
        self.write_question_rows(worksheet)
        self.write_totals(worksheet)

def main ():
    assignment = Assignment()
    participants = assignment.genPartList()
    assignment.create_workbook(participants)
    assignment.write_master()
    assignment.write_analysis(participants)
    for worksheet in assignment.workbook.worksheets():
        if (worksheet.get_name() == 'master' or worksheet.get_name() == 'analysis'):
                continue
        assignment.write_grade_sheets(worksheet)
    assignment.workbook.close()

if __name__ == "__main__":
    main()
