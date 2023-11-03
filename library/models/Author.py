# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime, timedelta
from odoo import models, fields, api
class Author(models.Model):
    _name = 'books.author'
    _inherit = 'mail.thread'
    _description = 'books.author'

    name = fields.Char(string="Name", tracking=True)
    data_of_birth = fields.Date(string="Date Of Birth", tracking=True)
    image = fields.Image(string="Image", tracking=True)
    age = fields.Integer(string="Age", compute='_compute_age', tracking=True)
    salary = fields.Integer(string="Salary", tracking=True)
    email = fields.Char(string='Email', size=256, tracking=True)
    phone_number = fields.Char(string='Phone Number', size=20, tracking=True)
    book_ids = fields.Many2many('books.data', string="Books")
    color = fields.Integer(string="color", tracking=True)
    start_date = fields.Datetime(default=fields.Datetime.today)
    end_date = fields.Date(string="End Date", store=True,
                           Compute='_get_end_date_', inverse='_set_end_date', tracking=True)

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

    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.data_of_birth:
                rec.age = today.year - rec.data_of_birth.year
            else:
                rec.age = 0

    def action_in_consultation(self):

        for rec in self:
            rec.state = 'in_consulation'

    def action_done(self):

        for rec in self:
            rec.state = 'done'

    def action_cancel(self):

        for rec in self:
            rec.state = 'cancel'

    def action_draft(self):

        for rec in self:
            rec.state = 'draft'
