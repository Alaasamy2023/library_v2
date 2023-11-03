# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, date
from odoo import models, fields, api

class Borrows(models.Model):
    _name = 'books.borrows'
    _description = 'books.borrows'

    name = fields.Many2one('res.partner', string="Name")
    book_id = fields.Many2one('books.data', string='Book')
    start_borrow = fields.Datetime(string="Start Borrow")
    email = fields.Char(string='Email Borrower', size=256, related='name.email', readonly=True)
    phone_number = fields.Char(string="Phone Number", related='name.phone', readonly=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('running', 'Running'),
                              ('delayed', 'Delayed'),
                              ('ended', 'Ended'),
                              ], default="draft", string='state')
    end_borrow = fields.Datetime(string="End Borrow", store=True,  Compute='_get_end_date_', inverse='_set_end_date')

    # end_borrow = fields.Datetime(string="End Borrow",  Compute='_get_end_date_', store=True,)


    daily_price = fields.Float(string="Day Price", related='book_id.price')

    # daily_price = fields.Float(string="Day Price")
    #
    #
    color = fields.Integer()
    duration = fields.Integer()
    received_date = fields.Datetime()
    delay_duration = fields.Float(string="Delay Duration", readonly=True)
    # delay_penalties = fields.Many2one('delay.penalities', string="Delay Penalties")
    borrows_duration = fields.Float(string="Borrows Duration")
    sub_total = fields.Integer(compute='_compute_sub_s_total', store=True)
    # total_money = fields.Float(compute='_compute_total', store=True, string="Total Money")

    #
    # sub_total = fields.Integer( store=True)
    total_money = fields.Float(store=True, string="Total Money")
    book_copy_id = fields.Many2one('book.copies', string="Copies")
    partner_id = fields.Many2one('res.partner', string='Partner')
    place = fields.Char(related="book_copy_id.place")











    # @api.onchange('start_borrow', 'end_borrow')
    # def states_test(self):
    #     # when sdate <= today <= edate state=running else state=draft
    #     sdate = self.start_borrow
    #     edate = self.end_borrow
    #     today = datetime.now()
    #     if sdate and edate:
    #         if sdate <= today <= edate:
    #             self.state = 'running'
    #         else:
    #             self.state = 'draft'
    #     else:
    #         self.state = 'draft'

    # account end_borrow using  start_borrow + borrows_duration
    @api.onchange('borrows_duration')
    def _onchange_borrows_duration(self):
        #
        if self.borrows_duration and self.start_borrow:
            start_date = fields.Datetime.from_string(self.start_borrow)
            new_end_date = start_date + timedelta(days=self.borrows_duration)
            self.end_borrow = new_end_date















    # account borrows_duration using  start_borrow + end_borrow
    @api.onchange('start_borrow', 'end_borrow')
    def _onchange_da_tes(self):
        '''
                to calculate period of borrows Duration based on start deta and end date

       لحساب فترة الاقتراض المدة على أساس تاريخ البدء وتاريخ الانتهاء
       after save
        '''
        if self.start_borrow and self.end_borrow:
            delta = self.end_borrow - self.start_borrow
            if delta.days < 0:
                nod = 0
            else:
                nod = delta.days
            self.borrows_duration = nod
        else:
            self.borrows_duration = 0

























# account borrows_duration using  start_borrow + end_borrow   outo
        @api.depends('start_borrow', 'duration')
        def _get_end_date_(self):
            '''
                    to calculate period of borrows Duration based on start deta and end date

           لحساب فترة الاقتراض المدة على أساس تاريخ البدء وتاريخ الانتهاء
outomatic
            '''
            for r in self:
                if not (r.start_borrow and r.duration):
                    r.end_borrow = r.start_borrow
                    continue
                duration = timedelta(days=r.duration, seconds=-1)
                r.end_borrow = r.start_borrow + duration











# account end_borrow using  start_borrow + duration   outo
    def _set_end_date(self):
        for r in self:
            if not (r.start_borrow and r.duration):
                continue

            r.duration = (r.end_borrow - r.start_borrow).days + 1
















    def action_ended(self):

        """
         Perform the action of change the borrow to the 'ended' state.
       """
        self.received_date = datetime.now().strftime('%Y-%m-%d')
        self.state = 'ended'
        self.book_copy_id.state = 'available'






 # Only  copies   of selected books  are    available
    @api.onchange('book_id')
    def _onchange_book_id(self):
        '''  Perform a search to find available copies of the selected book
            Return a domain filter to restrict the available options for the book_copy_id field
        '''
        book_copies = self.env['book.copies'].search(
            [("book_id", "=", self.book_id.id), ('state', '=', 'available')]).ids
        return {'domain': {'book_copy_id': [('id', 'in', book_copies)]}}












    @api.onchange('end_borrow', 'received_date')
    def onchange_dates(self):
        '''
        to calculate delay_duration based on end_borrow and received_date
         delay_duration = received_date - end_borrow

 لحساب Delay_duration بناءً على end_borrow وReceive_date
          تأخير_مدة = تاريخ الاستلام - نهاية_الاقتراض

        '''
        if self.end_borrow and self.received_date:
            delta = self.received_date - self.end_borrow
            if delta.days < 0:
                nod = 0
            else:
                nod = delta.days
            self.delay_duration = nod
        else:
            self.delay_duration = 0




























@api.depends('daily_price', 'borrows_duration')
def _compute_sub_s_total(self):
    '''
    to calculate sub_total based on (daily_price) and (borrows_duration)
    daily_price * borrows_duration =sub_total

   لحساب الإجمالي الفرعي على أساس (سعر_اليوم) و (مدة_الاقتراض)
     daily_price * اقتراض_المدة =sub_total

    '''
    for rec in self:
        sub_total = 0.0
        if rec.borrows_duration and rec.daily_price:
            sub_total = rec.borrows_duration * rec.daily_price
        rec.sub_total = sub_total


