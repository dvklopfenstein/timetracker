"""Generate a Microsoft Word document containing a table of data"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

##from os import remove
#from os.path import exists
##from os.path import basename
##from os.path import join
##from os.path import abspath
##from os.path import dirname
##from os.path import normpath
##https://python-docx.readthedocs.io/en/latest/
from docx import Document
#from docx.shared import Inches
#from datetime import timedelta
#from datetime import datetime
#from logging import debug
#from csv import reader
#
#from timetracker.utils import orange
#from timetracker.consts import DIRTRK
from timetracker.timetext import get_data_formatted
##from timetracker.cfg.utils import get_username


class WordDoc:
    """Generate a Microsoft Word document containing a table of data"""

    def __init__(self, timedata):
        self.tdata = timedata
        self.ttext = get_data_formatted(timedata)

    def write_doc(self, fout_docx):
        """Write a report into a Microsoft Word document"""
        document = Document()

        document.add_heading('Document Title', 0)

        p = document.add_paragraph('A plain paragraph having some ')
        p.add_run('bold').bold = True
        p.add_run(' and some ')
        p.add_run('italic.').italic = True

        document.add_heading('Heading, level 1', level=1)
        document.add_paragraph('Intense quote', style='Intense Quote')

        document.add_paragraph(
            'first item in unordered list', style='List Bullet'
        )
        document.add_paragraph(
            'first item in ordered list', style='List Number'
        )

        #document.add_picture('monty-truth.png', width=Inches(1.25))

        self.add_table(document)
        document.add_page_break()

        document.save(fout_docx)
        print(f'  WROTE: {fout_docx}')

    def add_table(self, doc):
        """Add a table containing timetracking data to a Word document"""
        records = (
            (3, '101', 'Spam'),
            (7, '422', 'Eggs'),
            (4, '631', 'Spam, spam, eggs, and spam')
        )
        table = doc.add_table(rows=1, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Qty'
        hdr_cells[1].text = 'Id'
        hdr_cells[2].text = 'Desc'
        for qty, idval, desc in records:
            row_cells = table.add_row().cells
            row_cells[0].text = str(qty)
            row_cells[1].text = idval
            row_cells[2].text = desc



# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
