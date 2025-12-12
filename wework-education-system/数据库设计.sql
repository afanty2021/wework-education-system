-- 基于企业微信的轻量级教务系统数据库设计
-- 适用于小型培训机构

-- 创建数据库
CREATE DATABASE IF NOT EXISTS edu_wework DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE edu_wework;

-- ===================================
-- 基础数据表
-- ===================================

-- 1. 系统配置表
CREATE TABLE sys_config (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    config_desc VARCHAR(200) COMMENT '配置说明',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '系统配置表';

-- 初始化系统配置
INSERT INTO sys_config (config_key, config_value, config_desc) VALUES
('wework_corp_id', '', '企业微信企业ID'),
('wework_corp_secret', '', '企业微信应用Secret'),
('wework_agent_id', '1000001', '企业微信应用ID'),
('class_remind_minutes', '30', '课前提醒分钟数'),
('allow_leave_hours', '2', '允许提前请假小时数');

-- 2. 操作日志表（简化版）
CREATE TABLE operation_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(64) NOT NULL COMMENT '操作人企微ID',
    user_name VARCHAR(50) NOT NULL COMMENT '操作人姓名',
    module VARCHAR(50) NOT NULL COMMENT '操作模块',
    operation VARCHAR(100) NOT NULL COMMENT '操作类型',
    content TEXT COMMENT '操作内容',
    ip_address VARCHAR(50) COMMENT 'IP地址',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_time (user_id, created_at)
) COMMENT '操作日志表';

-- ===================================
-- 用户权限表（简化版）
-- ===================================

-- 3. 角色表
CREATE TABLE role (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    role_code VARCHAR(50) NOT NULL UNIQUE COMMENT '角色编码',
    role_name VARCHAR(50) NOT NULL COMMENT '角色名称',
    description VARCHAR(200) COMMENT '角色描述',
    sort_order INT DEFAULT 0 COMMENT '排序',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用 0禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) COMMENT '角色表';

-- 初始化角色数据
INSERT INTO role (role_code, role_name, description, sort_order) VALUES
('SUPER_ADMIN', '超级管理员', '系统管理员，拥有所有权限', 1),
('ADMIN', '管理员', '校区管理员，拥有大部分权限', 2),
('TEACHER', '教师', '普通教师，拥有教学相关权限', 3),
('ASSISTANT', '助教', '助教，协助教师管理', 4);

-- 4. 用户表（同步自企业微信）
CREATE TABLE user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(64) NOT NULL UNIQUE COMMENT '企微用户ID',
    username VARCHAR(50) COMMENT '用户名',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    mobile VARCHAR(20) COMMENT '手机号',
    email VARCHAR(100) COMMENT '邮箱',
    avatar VARCHAR(500) COMMENT '头像URL',
    position VARCHAR(100) COMMENT '职位',
    department VARCHAR(100) COMMENT '部门',
    role_id BIGINT COMMENT '角色ID',
    status TINYINT DEFAULT 1 COMMENT '状态：1正常 0禁用',
    last_login_time TIMESTAMP NULL COMMENT '最后登录时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES role(id),
    INDEX idx_user_id (user_id),
    INDEX idx_mobile (mobile)
) COMMENT '用户表';

-- 5. 学员表
CREATE TABLE student (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_no VARCHAR(20) UNIQUE NOT NULL COMMENT '学员编号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    nickname VARCHAR(50) COMMENT '小名',
    gender TINYINT COMMENT '性别：0未知 1男 2女',
    birthday DATE COMMENT '生日',
    mobile VARCHAR(20) COMMENT '手机号',
    address VARCHAR(200) COMMENT '地址',
    school VARCHAR(100) COMMENT '学校',
    grade VARCHAR(20) COMMENT '年级',
    parent_name VARCHAR(50) COMMENT '主要家长姓名',
    parent_mobile VARCHAR(20) COMMENT '家长手机号',
    parent_wxid VARCHAR(64) COMMENT '家长企微ID',
    parent_relation VARCHAR(20) DEFAULT '妈妈' COMMENT '与家长关系',
    emergency_contact VARCHAR(50) COMMENT '紧急联系人',
    emergency_phone VARCHAR(20) COMMENT '紧急联系电话',
    join_date DATE COMMENT '入学日期',
    remark TEXT COMMENT '备注',
    status TINYINT DEFAULT 1 COMMENT '状态：1在读 0已退学',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_mobile (mobile),
    INDEX idx_parent_wxid (parent_wxid),
    INDEX idx_status (status)
) COMMENT '学员表';

-- 6. 课程表
CREATE TABLE course (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    course_code VARCHAR(20) UNIQUE NOT NULL COMMENT '课程编码',
    name VARCHAR(100) NOT NULL COMMENT '课程名称',
    category VARCHAR(50) COMMENT '课程分类',
    description TEXT COMMENT '课程描述',
    duration INT DEFAULT 60 COMMENT '单次课时长(分钟)',
    max_students INT DEFAULT 30 COMMENT '最大人数',
    min_age INT COMMENT '最小年龄',
    max_age INT COMMENT '最大年龄',
    price DECIMAL(10,2) COMMENT '单次课价格',
    total_price DECIMAL(10,2) COMMENT '课程总价',
    color VARCHAR(10) DEFAULT '#409EFF' COMMENT '显示颜色',
    cover_url VARCHAR(500) COMMENT '封面图',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用 0禁用',
    sort_order INT DEFAULT 0 COMMENT '排序',
    created_by BIGINT COMMENT '创建人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_status (status)
) COMMENT '课程表';

-- 7. 教室表
CREATE TABLE classroom (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    room_no VARCHAR(20) UNIQUE NOT NULL COMMENT '教室编号',
    name VARCHAR(50) NOT NULL COMMENT '教室名称',
    floor VARCHAR(10) COMMENT '楼层',
    area INT COMMENT '面积(平方米)',
    capacity INT DEFAULT 30 COMMENT '容纳人数',
    equipment TEXT COMMENT '设备说明',
    status TINYINT DEFAULT 1 COMMENT '状态：1正常 0维修',
    remark TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status)
) COMMENT '教室表';

-- 8. 班级表
CREATE TABLE class_group (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    class_no VARCHAR(20) UNIQUE NOT NULL COMMENT '班级编号',
    name VARCHAR(100) NOT NULL COMMENT '班级名称',
    course_id BIGINT NOT NULL COMMENT '课程ID',
    teacher_id BIGINT COMMENT '主讲教师ID',
    assistant_ids TEXT COMMENT '助教ID列表(逗号分隔)',
    classroom_id BIGINT COMMENT '默认教室',
    max_students INT DEFAULT 30 COMMENT '最大人数',
    current_students INT DEFAULT 0 COMMENT '当前人数',
    start_date DATE COMMENT '开课日期',
    end_date DATE COMMENT '结课日期',
    schedule_type TINYINT DEFAULT 1 COMMENT '排课类型：1固定 2灵活',
    schedule_desc TEXT COMMENT '上课安排描述',
    status TINYINT DEFAULT 1 COMMENT '状态：1正常 2暂停 3结束',
    remark TEXT COMMENT '备注',
    created_by BIGINT COMMENT '创建人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES course(id),
    FOREIGN KEY (teacher_id) REFERENCES user(id),
    FOREIGN KEY (classroom_id) REFERENCES classroom(id),
    INDEX idx_course_id (course_id),
    INDEX idx_teacher_id (teacher_id),
    INDEX idx_status (status)
) COMMENT '班级表';

-- 9. 班级学员关联表
CREATE TABLE class_student (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    class_id BIGINT NOT NULL COMMENT '班级ID',
    student_id BIGINT NOT NULL COMMENT '学员ID',
    join_date DATE NOT NULL COMMENT '加入日期',
    leave_date DATE COMMENT '退出日期',
    status TINYINT DEFAULT 1 COMMENT '状态：1正常 0已退出',
    remark VARCHAR(200) COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_class_student (class_id, student_id, status),
    FOREIGN KEY (class_id) REFERENCES class_group(id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    INDEX idx_student_id (student_id),
    INDEX idx_status (status)
) COMMENT '班级学员关联表';

-- ===================================
-- 课程安排相关表
-- ===================================

-- 10. 课程安排表（简化版）
CREATE TABLE class_schedule (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    class_id BIGINT NOT NULL COMMENT '班级ID',
    course_id BIGINT NOT NULL COMMENT '课程ID',
    teacher_id BIGINT NOT NULL COMMENT '教师ID',
    assistant_id BIGINT COMMENT '助教ID',
    classroom_id BIGINT NOT NULL COMMENT '教室ID',
    start_time DATETIME NOT NULL COMMENT '开始时间',
    end_time DATETIME NOT NULL COMMENT '结束时间',
    week_day TINYINT COMMENT '星期几(0-6)',
    is_recurring TINYINT DEFAULT 0 COMMENT '是否重复课程：0否 1是',
    title VARCHAR(100) COMMENT '课程主题',
    content TEXT COMMENT '课程内容',
    materials TEXT COMMENT '所需材料',
    status TINYINT DEFAULT 1 COMMENT '状态：1正常 2取消 3结束',
    cancel_reason VARCHAR(200) COMMENT '取消原因',
    created_by BIGINT COMMENT '创建人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES class_group(id),
    FOREIGN KEY (course_id) REFERENCES course(id),
    FOREIGN KEY (teacher_id) REFERENCES user(id),
    FOREIGN KEY (assistant_id) REFERENCES user(id),
    FOREIGN KEY (classroom_id) REFERENCES classroom(id),
    INDEX idx_teacher_time (teacher_id, start_time),
    INDEX idx_classroom_time (classroom_id, start_time),
    INDEX idx_class_time (class_id, start_time),
    INDEX idx_date (DATE(start_time))
) COMMENT '课程安排表';

-- 11. 考勤记录表
CREATE TABLE attendance (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    schedule_id BIGINT NOT NULL COMMENT '课程安排ID',
    student_id BIGINT NOT NULL COMMENT '学员ID',
    status TINYINT NOT NULL COMMENT '出勤状态：1出勤 2请假 3旷课 4补课',
    check_time DATETIME COMMENT '签到时间',
    check_by BIGINT COMMENT '签到人',
    leave_reason TEXT COMMENT '请假原因',
    leave_hours DECIMAL(4,1) COMMENT '请假时长',
    remark TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES class_schedule(id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (check_by) REFERENCES user(id),
    UNIQUE KEY uk_schedule_student (schedule_id, student_id),
    INDEX idx_student_date (student_id, DATE(created_at)),
    INDEX idx_status (status)
) COMMENT '考勤记录表';

-- 12. 作业表
CREATE TABLE homework (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    schedule_id BIGINT NOT NULL COMMENT '课程安排ID',
    class_id BIGINT NOT NULL COMMENT '班级ID',
    title VARCHAR(200) NOT NULL COMMENT '作业标题',
    content TEXT COMMENT '作业内容',
    attachments TEXT COMMENT '附件(JSON格式)',
    deadline DATETIME COMMENT '截止时间',
    created_by BIGINT NOT NULL COMMENT '布置人ID',
    submit_count INT DEFAULT 0 COMMENT '提交人数',
    status TINYINT DEFAULT 1 COMMENT '状态：1进行中 2已截止',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES class_schedule(id),
    FOREIGN KEY (class_id) REFERENCES class_group(id),
    FOREIGN KEY (created_by) REFERENCES user(id),
    INDEX idx_class_id (class_id),
    INDEX idx_deadline (deadline)
) COMMENT '作业表';

-- 13. 作业提交表
CREATE TABLE homework_submit (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    homework_id BIGINT NOT NULL COMMENT '作业ID',
    student_id BIGINT NOT NULL COMMENT '学员ID',
    content TEXT COMMENT '作业内容',
    attachments TEXT COMMENT '附件(JSON格式)',
    score DECIMAL(5,2) COMMENT '得分',
    comment TEXT COMMENT '评语',
    submitted_at DATETIME COMMENT '提交时间',
    graded_by BIGINT COMMENT '批改人',
    graded_at DATETIME COMMENT '批改时间',
    status TINYINT DEFAULT 1 COMMENT '状态：1已提交 2已批改 3需重做',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (homework_id) REFERENCES homework(id),
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (graded_by) REFERENCES user(id),
    UNIQUE KEY uk_homework_student (homework_id, student_id),
    INDEX idx_student_id (student_id)
) COMMENT '作业提交表';

-- ===================================
-- 消息通知相关表
-- ===================================

-- 14. 消息模板表
CREATE TABLE message_template (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '模板编码',
    name VARCHAR(100) NOT NULL COMMENT '模板名称',
    title VARCHAR(200) NOT NULL COMMENT '消息标题',
    content TEXT NOT NULL COMMENT '消息内容',
    type TINYINT NOT NULL COMMENT '消息类型：1系统 2上课 3作业 4通知',
    status TINYINT DEFAULT 1 COMMENT '状态：1启用 0禁用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT '消息模板表';

-- 初始化消息模板
INSERT INTO message_template (code, name, title, content, type) VALUES
('CLASS_REMIND', '上课提醒', '上课提醒', '您有节课即将开始\n课程：{{courseName}}\n时间：{{startTime}}\n教室：{{classroom}}\n请提前做好准备', 2),
('HOMEWORK_NOTIFY', '作业通知', '新作业通知', '{{teacherName}}老师布置了新作业\n作业：{{title}}\n截止时间：{{deadline}}\n请及时完成', 3),
('STUDENT_ABSENT', '学员缺勤', '缺勤通知', '学员{{studentName}}今日未到课\n课程：{{courseName}}\n时间：{{classTime}}\n请及时联系家长', 4);

-- 15. 消息记录表
CREATE TABLE message_record (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    receiver_id VARCHAR(64) NOT NULL COMMENT '接收人企微ID',
    receiver_name VARCHAR(50) COMMENT '接收人姓名',
    template_id BIGINT COMMENT '模板ID',
    title VARCHAR(200) NOT NULL COMMENT '消息标题',
    content TEXT NOT NULL COMMENT '消息内容',
    url VARCHAR(500) COMMENT '跳转链接',
    type TINYINT NOT NULL COMMENT '消息类型：1系统 2上课 3作业 4通知',
    business_id BIGINT COMMENT '业务ID',
    business_type VARCHAR(50) COMMENT '业务类型',
    send_status TINYINT DEFAULT 0 COMMENT '发送状态：0待发送 1成功 2失败',
    send_time DATETIME COMMENT '发送时间',
    error_msg TEXT COMMENT '错误信息',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (template_id) REFERENCES message_template(id),
    INDEX idx_receiver_id (receiver_id),
    INDEX idx_send_status (send_status),
    INDEX idx_business (business_type, business_id)
) COMMENT '消息记录表';

-- 16. 请假申请表
CREATE TABLE leave_apply (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    student_id BIGINT NOT NULL COMMENT '学员ID',
    schedule_id BIGINT COMMENT '课程安排ID（单次请假）',
    start_date DATE COMMENT '开始日期（批量请假）',
    end_date DATE COMMENT '结束日期（批量请假）',
    leave_type TINYINT DEFAULT 1 COMMENT '请假类型：1事假 2病假',
    reason TEXT NOT NULL COMMENT '请假原因',
    apply_by VARCHAR(64) COMMENT '申请人企微ID',
    status TINYINT DEFAULT 1 COMMENT '状态：1待审批 2已批准 3已拒绝',
    approve_by VARCHAR(64) COMMENT '审批人企微ID',
    approve_time DATETIME COMMENT '审批时间',
    approve_remark VARCHAR(500) COMMENT '审批备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (schedule_id) REFERENCES class_schedule(id),
    INDEX idx_student_id (student_id),
    INDEX idx_status (status),
    INDEX idx_date_range (start_date, end_date)
) COMMENT '请假申请表';

-- ===================================
-- 教师培训相关表（扩展功能）
-- ===================================

-- 17. 培训课程表
CREATE TABLE training_course (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL COMMENT '培训标题',
    description TEXT COMMENT '培训描述',
    trainer VARCHAR(100) COMMENT '培训师',
    duration INT COMMENT '培训时长(分钟)',
    training_type TINYINT COMMENT '培训类型：1线上 2线下',
    start_time DATETIME COMMENT '开始时间',
    end_time DATETIME COMMENT '结束时间',
    location VARCHAR(200) COMMENT '培训地点',
    max_participants INT DEFAULT 50 COMMENT '最大人数',
    current_participants INT DEFAULT 0 COMMENT '当前人数',
    status TINYINT DEFAULT 1 COMMENT '状态：1报名中 2进行中 3已结束',
    created_by BIGINT COMMENT '创建人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_start_time (start_time)
) COMMENT '培训课程表';

-- 18. 培训报名表
CREATE TABLE training_enroll (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    training_id BIGINT NOT NULL COMMENT '培训ID',
    user_id VARCHAR(64) NOT NULL COMMENT '参训人企微ID',
    enroll_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
    status TINYINT DEFAULT 1 COMMENT '状态：1已报名 2已参加 3缺席',
    score DECIMAL(5,2) COMMENT '考核得分',
    feedback TEXT COMMENT '培训反馈',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (training_id) REFERENCES training_course(id),
    UNIQUE KEY uk_training_user (training_id, user_id),
    INDEX idx_user_id (user_id)
) COMMENT '培训报名表';

-- ===================================
-- 视图定义（简化查询）
-- ===================================

-- 19. 今日课程视图
CREATE VIEW v_today_schedule AS
SELECT
    cs.id,
    cs.title,
    c.name AS course_name,
    cg.name AS class_name,
    u.name AS teacher_name,
    cr.name AS classroom_name,
    cs.start_time,
    cs.end_time,
    cs.status,
    COUNT(cs2.student_id) AS student_count
FROM class_schedule cs
LEFT JOIN course c ON cs.course_id = c.id
LEFT JOIN class_group cg ON cs.class_id = cg.id
LEFT JOIN user u ON cs.teacher_id = u.id
LEFT JOIN classroom cr ON cs.classroom_id = cr.id
LEFT JOIN (
    SELECT cs.id, cs2.student_id
    FROM class_schedule cs
    JOIN class_student cs2 ON cs.class_id = cs2.class_id
    WHERE cs2.status = 1
) cs2 ON cs.id = cs2.id
WHERE DATE(cs.start_time) = CURDATE()
GROUP BY cs.id;

-- 20. 教师工作统计视图
CREATE VIEW v_teacher_stats AS
SELECT
    u.id AS teacher_id,
    u.name AS teacher_name,
    COUNT(DISTINCT cs.class_id) AS class_count,
    COUNT(DISTINCT cs.student_id) AS student_count,
    COUNT(cs.id) AS schedule_count,
    SUM(CASE WHEN a.status = 1 THEN 1 ELSE 0 END) AS attendance_count
FROM user u
LEFT JOIN class_schedule cs ON u.id = cs.teacher_id AND cs.status = 1
LEFT JOIN attendance a ON cs.id = a.schedule_id
WHERE u.role_id IN (SELECT id FROM role WHERE role_code IN ('TEACHER', 'ASSISTANT'))
    AND u.status = 1
GROUP BY u.id;

-- ===================================
-- 触发器（自动维护统计数据）
-- ===================================

-- 21. 班级学员数更新触发器
DELIMITER $$
CREATE TRIGGER tr_class_student_insert
AFTER INSERT ON class_student
FOR EACH ROW
BEGIN
    UPDATE class_group
    SET current_students = current_students + 1
    WHERE id = NEW.class_id;
END$$

CREATE TRIGGER tr_class_student_delete
AFTER UPDATE ON class_student
FOR EACH ROW
BEGIN
    IF NEW.status = 0 AND OLD.status = 1 THEN
        UPDATE class_group
        SET current_students = current_students - 1
        WHERE id = NEW.class_id;
    END IF;
END$$
DELIMITER ;

-- ===================================
-- 存储过程（常用业务逻辑）
-- ===================================

-- 22. 批量创建课程安排
DELIMITER $$
CREATE PROCEDURE sp_create_batch_schedule(
    IN p_class_id BIGINT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_week_days VARCHAR(20), -- 逗号分隔的星期几：1,3,5
    IN p_start_time TIME,
    IN p_end_time TIME,
    IN p_classroom_id BIGINT,
    IN p_created_by BIGINT
)
BEGIN
    DECLARE v_current_date DATE;
    DECLARE v_week_day TINYINT;
    DECLARE v_schedule_id BIGINT;

    SET v_current_date = p_start_date;

    WHILE v_current_date <= p_end_date DO
        SET v_week_day = DAYOFWEEK(v_current_date) - 1; -- 转换为0-6

        IF FIND_IN_SET(v_week_day, p_week_days) > 0 THEN
            -- 插入课程安排
            INSERT INTO class_schedule (
                class_id,
                course_id,
                teacher_id,
                classroom_id,
                start_time,
                end_time,
                week_day,
                is_recurring,
                status,
                created_by
            )
            SELECT
                p_class_id,
                course_id,
                teacher_id,
                p_classroom_id,
                CONCAT(v_current_date, ' ', p_start_time),
                CONCAT(v_current_date, ' ', p_end_time),
                v_week_day,
                1,
                1,
                p_created_by
            FROM class_group
            WHERE id = p_class_id;
        END IF;

        SET v_current_date = DATE_ADD(v_current_date, INTERVAL 1 DAY);
    END WHILE;
END$$
DELIMITER ;

-- ===================================
-- 索引优化
-- ===================================

-- 创建复合索引提高查询性能
CREATE INDEX idx_schedule_teacher_class_time ON class_schedule(teacher_id, class_id, start_time);
CREATE INDEX idx_attendance_student_date ON class_schedule(student_id, DATE(start_time));
CREATE INDEX idx_homework_class_deadline ON homework(class_id, deadline);
CREATE INDEX idx_class_student_class ON class_student(class_id, student_id, status);

-- ===================================
-- 初始数据
-- ===================================

-- 插入默认管理员
INSERT INTO user (user_id, username, name, mobile, role_id, status) VALUES
('admin', 'admin', '系统管理员', '13800000000', 1, 1);

-- 插入示例课程
INSERT INTO course (course_code, name, category, duration, max_students, min_age, max_age, price, color, created_by) VALUES
('ART001', '儿童绘画基础', '艺术', 90, 15, 4, 6, 150.00, '#FF6B6B', 1),
('PIANO001', '钢琴入门', '音乐', 60, 10, 5, 8, 200.00, '#4ECDC4', 1),
('DANCE001', '少儿舞蹈', '舞蹈', 60, 20, 4, 7, 120.00, '#95E77E', 1);

-- 插入示例教室
INSERT INTO classroom (room_no, name, floor, capacity, equipment) VALUES
('101', '绘画教室1', '1F', 15, '画架、画板、水彩笔、素描纸'),
('201', '音乐教室1', '2F', 10, '钢琴、电子琴、音响设备'),
('301', '舞蹈教室1', '3F', 20, '把杆、镜子、音响设备');

-- ===================================
-- 数据库维护建议
-- ===================================

/*
定期维护任务：
1. 每周执行OPTIMIZE TABLE优化表
2. 每月清理3个月前的操作日志
3. 每学期结束后归档历史数据
4. 定期备份数据库

备份策略：
- 每日全量备份
- 实时binlog备份
- 异地备份存储
*/

-- 清理日志的存储过程
DELIMITER $$
CREATE PROCEDURE sp_cleanup_logs(IN p_days INT)
BEGIN
    DELETE FROM operation_log WHERE created_at < DATE_SUB(NOW(), INTERVAL p_days DAY);
    DELETE FROM message_record WHERE created_at < DATE_SUB(NOW(), INTERVAL p_days DAY);
END$$
DELIMITER ;