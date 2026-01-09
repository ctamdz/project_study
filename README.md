# Enmasys Project Study

Module quản lý Project Study cho Odoo 17.0

## 📋 Mô tả

Module này giúp quản lý các Study trong dự án với các tính năng:
- Tạo và quản lý các Study
- Theo dõi trạng thái (To Do, In Progress, Review, Done)
- Gán người phụ trách, deadline, tags
- Hỗ trợ cấu trúc phân cấp (Parent/Child Studies)
- Tích hợp chatter để theo dõi hoạt động
- Gửi email tự động khi được giao study
- Báo cáo và phân tích dữ liệu

## 🛠️ Yêu cầu

- **Odoo version**: 17.0
- **Dependencies**: `project` module

## 📂 Cấu trúc Module

```text
project_study/
├── __init__.py
├── __manifest__.py
├── data/
│   └── mail_template_data.xml          # Email template
├── models/
│   ├── __init__.py
│   └── study.py                        # Model chính
├── report/
│   ├── __init__.py
│   └── study_report.py                 # SQL View cho báo cáo
├── security/
│   ├── ir.model.access.csv             # Quyền truy cập
│   └── project_study_security.xml      # Security groups & rules
├── static/
│   └── description/
│       └── icon.png                    # Icon của module
└── views/
    ├── study_menus.xml                 # Menu items
    ├── study_report_views.xml          # Views cho báo cáo
    └── study_views.xml                 # Views chính
```

## 📊 Models

### 1. Project Study (`project.study`)
Model chính để quản lý Study với các trường:

| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `name` | Char | Tên của study (bắt buộc) |
| `user_id` | Many2one | Người được giao |
| `date_start` | Date | Ngày bắt đầu |
| `date_end` | Date | Ngày kết thúc |
| `date_deadline` | Date | Deadline |
| `state` | Selection | Trạng thái (todo/in_progress/review/done) |
| `tag_ids` | Many2many | Các tags |
| `parent_id` | Many2one | Study cha |
| `child_ids` | One2many | Các sub-studies |
| `description` | Html | Mô tả chi tiết |

### 2. Project Study Tag (`project.study.tag`)
Model để lưu tags cho Study:

| Trường | Kiểu | Mô tả |
|--------|------|-------|
| `name` | Char | Tên tag |
| `color` | Integer | Màu sắc |

### 3. Study Report (`report.project.study`)
SQL View để phân tích dữ liệu Study.

## 👥 Phân quyền

### Groups

| Group | Mô tả | Quyền |
|-------|-------|-------|
| Project Study User | Người dùng thông thường | Xem, tạo, sửa record của mình |
| Project Study Manager | Quản lý | Full quyền (CRUD) tất cả records |

### Record Rules
- **Manager**: Xem tất cả records
- **User**: Chỉ xem records mình tạo hoặc được giao
- **Multi-company**: Hỗ trợ multi-company

## 🖥️ Views

Module cung cấp các loại views:

1. **List View (Tree)**: Hiển thị danh sách studies với multi-edit
2. **Form View**: Form chi tiết với chatter
3. **Kanban View**: Hiển thị theo trạng thái với drag & drop
4. **Graph View**: Biểu đồ cột số lượng study theo user
5. **Pivot View**: Bảng phân tích theo user và state
6. **Search View**: Bộ lọc và group by

## 📧 Tính năng Email

- Tự động gửi email thông báo khi:
  - Tạo study mới và giao cho người khác
  - Thay đổi người được giao
- Người được giao tự động trở thành follower

## 🚀 Cài đặt

1. Copy thư mục `project_study` vào thư mục `addons` của Odoo
2. Restart Odoo server
3. Vào **Apps** → Cập nhật danh sách ứng dụng
4. Tìm kiếm "Enmasys Project Study"
5. Click **Install**

## 📝 Hướng dẫn sử dụng

### Tạo Study mới
1. Vào menu **Project Study** → **Studies**
2. Click nút **New**
3. Điền thông tin: Tên, Người phụ trách, Deadline, Tags...
4. Click **Save**

### Quản lý trạng thái
- Sử dụng **Kanban view** để kéo thả study giữa các trạng thái
- Hoặc click vào statusbar trong **Form view** để đổi trạng thái

### Xem báo cáo
1. Vào menu **Project** → **Reporting** → **Study Analysis**
2. Sử dụng Graph view hoặc Pivot view để phân tích

## 📄 License

LGPL-3



---

**Version**: 17.0.1.0.0
