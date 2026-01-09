# -*- coding: utf-8 -*-

from odoo import models, fields, tools


class StudyReport(models.Model):
    """
    Model báo cáo cho Study Analysis
    Đây là SQL View để phân tích dữ liệu Study
    """
    _name = 'report.project.study'
    _description = 'Study Analysis Report'
    _auto = False
    _order = 'user_id'

    name = fields.Char(string='Name', readonly=True)
    user_id = fields.Many2one('res.users', string='Assigned To', readonly=True)
    state = fields.Selection([
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ], string='State', readonly=True)
    date_start = fields.Date(string='Start Date', readonly=True)
    date_deadline = fields.Date(string='Deadline', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    
    # Field để đếm số lượng
    study_count = fields.Integer(string='# of Studies', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    s.id,
                    s.name,
                    s.user_id,
                    s.state,
                    s.date_start,
                    s.date_deadline,
                    s.company_id,
                    1 as study_count
                FROM project_study s
                WHERE s.active = true
            )
        """ % self._table)
