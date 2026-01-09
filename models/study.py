# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectStudyTag(models.Model):
    """
    Model để lưu Tags cho Study
    Mỗi tag có tên và màu sắc
    
    Ví dụ: "Urgent", "Research", "Development"
    """
    _name = 'project.study.tag'
    _description = 'Project Study Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')


class ProjectStudy(models.Model):
    """
    Model chính để quản lý Study
    
    Các trường chính:
    - name: Tên của study
    - user_id: Người được giao (Assigned To)
    - date_start, date_end, date_deadline: Các ngày quan trọng
    - state: Trạng thái (To Do, In Progress, Review, Done)
    - tag_ids: Các tags
    - parent_id: Study cha (để tạo cấu trúc phân cấp)
    """
    _name = 'project.study'
    _description = 'Project Study'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Kế thừa để có chatter và activities
    _order = 'id desc'  # Sắp xếp mới nhất lên đầu

    # ===== CÁC TRƯỜNG CƠ BẢN =====
    name = fields.Char(
        string='Name', 
        required=True, 
        tracking=True  # Theo dõi thay đổi trong chatter
    )
    
    user_id = fields.Many2one(
        'res.users', 
        string='Assigned To', 
        default=lambda self: self.env.user,  # Mặc định là user hiện tại
        tracking=True
    )
    
    # ===== CÁC TRƯỜNG NGÀY =====
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    date_deadline = fields.Date(string='Deadline', tracking=True)
    
    # ===== TRẠNG THÁI =====
    state = fields.Selection([
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'Review'),
        ('done', 'Done'),
    ], string='State', default='todo', tracking=True, group_expand='_group_expand_states')
    
    # ===== QUAN HỆ =====
    tag_ids = fields.Many2many(
        'project.study.tag', 
        string='Tags'
    )
    
    parent_id = fields.Many2one(
        'project.study', 
        string='Parent', 
        index=True  # Tạo index để query nhanh hơn
    )
    
    child_ids = fields.One2many(
        'project.study', 
        'parent_id', 
        string='Sub-studies'
    )
    
    # ===== CÁC TRƯỜNG KHÁC =====
    description = fields.Html(string='Description')
    active = fields.Boolean(default=True)  # Để archive/unarchive
    company_id = fields.Many2one(
        'res.company', 
        string='Company', 
        default=lambda self: self.env.company
    )
    color = fields.Integer(string='Color')  # Cho kanban view

    # ===== FIELD CHO GRAPH VIEW =====
    study_count = fields.Integer(
        string='Study Count', 
        default=1, 
        store=True
    )

    @api.model
    def _group_expand_states(self, states, domain, order):
        """
        Hàm này đảm bảo tất cả các state đều hiển thị trong kanban view
        ngay cả khi không có record nào ở state đó
        """
        return [key for key, val in type(self).state.selection]

    # ===== OVERRIDE CREATE & WRITE ĐỂ GỬI EMAIL =====
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create để gửi email thông báo khi tạo study mới
        và giao cho người khác
        """
        studies = super().create(vals_list)
        # Gửi email cho người được giao (trừ người tạo)
        self._study_message_auto_subscribe_notify({
            study: study.user_id 
            for study in studies 
            if study.user_id and study.user_id != self.env.user
        })
        return studies

    def write(self, vals):
        """
        Override write để gửi email khi thay đổi người được giao
        """
        # Lưu lại user_id cũ trước khi thay đổi
        old_user_ids = {study.id: study.user_id for study in self}
        result = super().write(vals)
        
        # Nếu user_id thay đổi, gửi email cho người mới được giao
        if 'user_id' in vals:
            users_to_notify = {}
            for study in self:
                old_user = old_user_ids.get(study.id)
                new_user = study.user_id
                # Chỉ gửi email nếu:
                # - Có người mới được giao
                # - Người mới khác người cũ
                # - Người mới không phải là người đang thực hiện thao tác
                if new_user and new_user != old_user and new_user != self.env.user:
                    users_to_notify[study] = new_user
            
            if users_to_notify:
                self._study_message_auto_subscribe_notify(users_to_notify)
        
        return result

    def _study_message_auto_subscribe_notify(self, users_per_study):
        """
        Gửi email thông báo khi được giao study
        
        :param users_per_study: dict {study_record: user_record}
        """
        if self.env.context.get('mail_auto_subscribe_no_notify'):
            return
        
        # Lấy template ID
        template_id = self.env['ir.model.data']._xmlid_to_res_id(
            'project_study.study_message_user_assigned', 
            raise_if_not_found=False
        )
        if not template_id:
            return
        
        # Lấy tên model để hiển thị trong email
        study_model_description = self.env['ir.model']._get(self._name).display_name
        
        for study, user in users_per_study.items():
            if not user:
                continue
            
            # Chuẩn bị dữ liệu cho template
            values = {
                'object': study,
                'model_description': study_model_description,
                'access_link': study._notify_get_action_link('view'),
                'assignee_name': user.sudo().name,
            }
            
            # Render template
            assignation_msg = self.env['ir.qweb']._render(
                'project_study.study_message_user_assigned', 
                values, 
                minimal_qcontext=True
            )
            assignation_msg = self.env['mail.render.mixin']._replace_local_links(assignation_msg)
            
            # Gửi email thông báo
            study.message_notify(
                subject=_('You have been assigned to %s', study.display_name),
                body=assignation_msg,
                partner_ids=user.partner_id.ids,
                record_name=study.display_name,
                email_layout_xmlid='mail.mail_notification_layout',
                model_description=study_model_description,
                mail_auto_delete=False,
            )

    def _message_auto_subscribe_followers(self, updated_values, default_subtype_ids):
        """
        Tự động thêm người được giao làm follower
        """
        if 'user_id' not in updated_values:
            return []
        
        new_followers = []
        user_id = updated_values.get('user_id')
        if user_id:
            user = self.env['res.users'].browse(user_id)
            if user.partner_id:
                new_followers.append((user.partner_id.id, default_subtype_ids, False))
        
        return new_followers
