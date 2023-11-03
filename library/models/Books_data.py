# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class Books_data(models.Model):
    _name = 'books.data'
    _description = 'books.dat'

    name = fields.Char(string="Tittle", tracking=True)
    price = fields.Float(string="Price")
    image = fields.Image(string="Book Cover")

    language = fields.Selection([('en', 'English'), ('ar', 'Arabic'), ('fr', 'French'), ('es', 'Spanish'), ('de', 'German'), ],
                                string='Language')
    description = fields.Text(string="Description")
    number_of_pages = fields.Integer(string="pages Book")
    author_ids = fields.Many2many('books.author', string="Author Name")
    copy_ids = fields.One2many('book.copies', 'book_id', string='Copies')
    copy_count = fields.Integer(string='Copy Count', compute='_compute_copy_count')
    start_date = fields.Datetime(default=fields.Datetime.today)
    end_date = fields.Date(string="End Date", store=True,
                           Compute='_get_end_date_', inverse='_set_end_date')
    color = fields.Integer(string="color")
    priority = fields.Selection([('0', 'normal'), ('1', 'low'),
                                 ('2', 'high'),
                                 ('3', 'very high')], string='priority')
    category_ids = fields.Many2one('books.category', string="Category Book")
    vergion = fields.Char(string="Vergion")
    ispn = fields.Char(string="Isbn")
    invoice = fields.Char(string="Invoice")

    @api.depends('copy_ids')
    def _compute_copy_count(self):
        '''
        compute_copy_count: Method decorated with @api.depends('copy_ids').
        This method calculates the value of
         the copy_count field.
         It iterates over each record and sets the copy_count field to the length of the copy_ids field.
        '''
        for book in self:
            # book.copy_count = len(book.copy_ids)
            book.copy_count = str(len(book.copy_ids))

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
       
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                continue

            r.duration = (r.end_date - r.start_date).days + 1







