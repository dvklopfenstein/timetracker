"""Local project configuration parser for timetracking"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

##from os import remove
#from os.path import exists
##from os.path import basename
##from os.path import join
##from os.path import abspath
##from os.path import dirname
##from os.path import normpath
#from collections import namedtuple
##https://python-docx.readthedocs.io/en/latest/
from docx import Document
from docx.shared import Inches
#from datetime import timedelta
#from datetime import datetime
#from logging import debug
#from csv import reader
#
#from timetracker.utils import orange
##from timetracker.consts import DIRTRK
#from timetracker.consts import FMTDT
##from timetracker.cfg.utils import get_username


class GenWordDoc:
    """Generate a Microsoft Word document containing a table of data"""

    def __init__(self, timedata):
        self.data = timedata

    def get_data_formatted(self):
        """Get timetracker data formatted for a report"""

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

        records = (
            (3, '101', 'Spam'),
            (7, '422', 'Eggs'),
            (4, '631', 'Spam, spam, eggs, and spam')
        )

        table = document.add_table(rows=1, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Qty'
        hdr_cells[1].text = 'Id'
        hdr_cells[2].text = 'Desc'
        for qty, idval, desc in records:
            row_cells = table.add_row().cells
            row_cells[0].text = str(qty)
            row_cells[1].text = idval
            row_cells[2].text = desc

        document.add_page_break()

        document.save(fout_docx)
        print(f'  WROTE: {fout_docx}')


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
