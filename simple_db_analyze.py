#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版数据库结构分析工具
"""

import re
import json
from collections import defaultdict

def analyze_sql_file(file_path):
    """分析SQL文件，提取表结构信息"""

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 找到实际的数据库（跳过mysql系统数据库）
    db_match = re.search(r'Current Database: `([^`]+)`', content)
    database_name = db_match.group(1) if db_match else "Unknown"

    # 查找所有CREATE TABLE语句
    create_table_pattern = r'CREATE TABLE(?:\s+IF NOT EXISTS)?\s+`([^`]+)`\s*\((.*?)\)\s*ENGINE=(\w+)'

    tables = re.findall(create_table_pattern, content, re.IGNORECASE | re.DOTALL)

    db_structure = {
        'database': database_name,
        'total_tables': len(tables),
        'tables': {}
    }

    # 分析每个表
    for table_name, table_content, engine in tables:
        table_info = {
            'name': table_name,
            'engine': engine,
            'columns': [],
            'primary_keys': [],
            'indexes': [],
            'comment': None,
            'purpose': get_table_purpose(table_name)
        }

        # 提取表注释
        comment_match = re.search(r'COMMENT=\'([^\']*)\'', table_content.split(')')[-1])
        if comment_match:
            table_info['comment'] = comment_match.group(1)

        # 分割字段定义
        # 处理括号内的内容（如ENUM、SET等类型）
        field_defs = split_field_definitions(table_content)

        for field_def in field_defs:
            field_def = field_def.strip()
            if not field_def:
                continue

            # 解析主键
            if field_def.upper().startswith('PRIMARY KEY'):
                pk_match = re.search(r'PRIMARY KEY\s*\(`?([^`)]+)`?\)', field_def, re.IGNORECASE)
                if pk_match:
                    table_info['primary_keys'].append(pk_match.group(1))
                continue

            # 解析索引
            if field_def.upper().startswith(('KEY', 'INDEX', 'UNIQUE')):
                index_match = re.search(r'(?:KEY|INDEX|UNIQUE)\s*`?(\w+)?`?\s*\(([^)]+)\)', field_def, re.IGNORECASE)
                if index_match:
                    index_name = index_match.group(1) or 'Unnamed'
                    index_columns = [c.strip().strip('`') for c in index_match.group(2).split(',')]
                    table_info['indexes'].append({
                        'name': index_name,
                        'columns': index_columns,
                        'type': 'UNIQUE' if field_def.upper().startswith('UNIQUE') else 'INDEX'
                    })
                continue

            # 解析普通字段
            column = parse_column_definition(field_def)
            if column:
                table_info['columns'].append(column)

        db_structure['tables'][table_name] = table_info

    return db_structure

def split_field_definitions(content):
    """分割字段定义，正确处理嵌套的括号"""
    fields = []
    current = ""
    level = 0

    for char in content:
        if char == '(':
            level += 1
        elif char == ')':
            level -= 1
        elif char == ',' and level == 0:
            if current.strip():
                fields.append(current.strip())
            current = ""
            continue

        current += char

    if current.strip():
        fields.append(current.strip())

    return fields

def parse_column_definition(field_def):
    """解析列定义"""
    # 匹配列定义：`name` type [options]
    match = re.match(r'`([^`]+)`\s+(\w+(?:\([^)]+\))?)\s*(.*)', field_def, re.IGNORECASE)
    if not match:
        return None

    column = {
        'name': match.group(1),
        'type': match.group(2).upper(),
        'nullable': True,
        'default': None,
        'auto_increment': False,
        'comment': None
    }

    options = match.group(3).upper()

    # 解析各种选项
    if 'NOT NULL' in options:
        column['nullable'] = False
    if 'AUTO_INCREMENT' in options:
        column['auto_increment'] = True
    if 'DEFAULT' in options:
        default_match = re.search(r'DEFAULT\s+([^\s,]+)', options)
        if default_match:
            column['default'] = default_match.group(1).strip("'\"")
    if 'COMMENT' in options:
        comment_match = re.search(r"COMMENT\s+'([^']+)'", options)
        if comment_match:
            column['comment'] = comment_match.group(1)

    return column

def get_table_purpose(table_name):
    """根据表名推断表的用途"""
    name = table_name.lower()

    if name.startswith('k_'):
        return '系统框架表'
    elif name.startswith('d_'):
        return '教学管理表'
    elif name.startswith('q_'):
        return '查询视图表'
    elif name.startswith('fstemp_'):
        return '同步临时表'
    elif name.startswith('wx') or name.startswith('wxtemp_'):
        return '微信相关表'
    elif 'member' in name:
        return '会员管理表'
    elif 'card' in name and 'package' in name:
        return '课时卡包表'
    elif 'card' in name:
        return '会员卡表'
    elif 'course' in name:
        return '课程表'
    elif 'lesson' in name:
        return '课时表'
    elif 'contract' in name:
        return '合同表'
    elif 'manager' in name:
        return '员工管理表'
    elif 'payment' in name or 'wages' in name or 'paylog' in name:
        return '财务管理表'
    elif 'product' in name:
        return '产品管理表'
    elif 'msg' in name or 'mail' in name or 'message' in name:
        return '消息管理表'
    elif 'temp' in name:
        return '临时表'
    elif 'import' in name:
        return '数据导入表'
    elif 'backup' in name:
        return '备份表'
    elif 'log' in name:
        return '日志表'
    elif 'config' in name or 'param' in name or 'setting' in name:
        return '配置参数表'
    elif 'news' in name:
        return '新闻公告表'
    elif 'role' in name:
        return '角色权限表'
    elif 'menu' in name:
        return '菜单表'
    elif 'class' in name or 'classroom' in name:
        return '班级教室表'
    elif 'leave' in name:
        return '请假表'
    elif 'homework' in name:
        return '作业表'
    elif 'exam' in name or 'test' in name:
        return '考试测试表'
    elif 'photo' in name:
        return '照片表'
    elif 'file' in name:
        return '文件管理表'
    elif 'health' in name:
        return '健康记录表'
    elif 'bbs' in name:
        return '论坛表'
    else:
        return '业务功能表'

def generate_markdown_doc(db_structure):
    """生成Markdown文档"""
    md = f"""# 教务系统数据库结构文档

## 数据库概览

- **数据库名称**: {db_structure['database']}
- **表总数**: {db_structure['total_tables']}
- **MySQL版本**: 5.0.67-community-nt
- **存储引擎**: 主要使用MyISAM
- **字符集**: UTF-8

## 表分类统计

"""

    # 按用途分组统计
    purpose_count = defaultdict(int)
    for table in db_structure['tables'].values():
        purpose_count[table['purpose']] += 1

    md += "| 表类型 | 数量 |\n"
    md += "|--------|------|\n"
    for purpose, count in sorted(purpose_count.items()):
        md += f"| {purpose} | {count} |\n"

    md += "\n---\n\n"

    # 按用途分组显示表详情
    tables_by_purpose = defaultdict(list)
    for table_name, table_info in db_structure['tables'].items():
        tables_by_purpose[table_info['purpose']].append((table_name, table_info))

    # 核心业务表
    core_purposes = ['会员管理表', '会员卡表', '课时卡包表', '课程表', '课时表', '合同表', '班级教室表']

    md += "## 核心业务表\n\n"

    for purpose in core_purposes:
        if purpose in tables_by_purpose:
            md += f"### {purpose}\n\n"
            for table_name, table_info in tables_by_purpose[purpose]:
                md += generate_table_detail(table_name, table_info)

    # 系统功能表
    system_purposes = ['系统框架表', '角色权限表', '菜单表', '配置参数表', '消息管理表']

    md += "## 系统功能表\n\n"

    for purpose in system_purposes:
        if purpose in tables_by_purpose:
            md += f"### {purpose}\n\n"
            for table_name, table_info in tables_by_purpose[purpose]:
                md += generate_table_detail(table_name, table_info)

    # 教学管理表
    teaching_purposes = ['教学管理表', '请假表', '作业表', '考试测试表']

    md += "## 教学管理表\n\n"

    for purpose in teaching_purposes:
        if purpose in tables_by_purpose:
            md += f"### {purpose}\n\n"
            for table_name, table_info in tables_by_purpose[purpose]:
                md += generate_table_detail(table_name, table_info)

    # 员工管理表
    md += "## 员工管理表\n\n"

    if '员工管理表' in tables_by_purpose:
        for table_name, table_info in tables_by_purpose['员工管理表']:
            md += generate_table_detail(table_name, table_info)

    # 财务管理表
    finance_purposes = ['财务管理表', '产品管理表']

    md += "## 财务和产品管理\n\n"

    for purpose in finance_purposes:
        if purpose in tables_by_purpose:
            md += f"### {purpose}\n\n"
            for table_name, table_info in tables_by_purpose[purpose]:
                md += generate_table_detail(table_name, table_info)

    # 其他功能表
    other_purposes = ['新闻公告表', '照片表', '文件管理表', '健康记录表', '论坛表', '微信相关表']

    md += "## 其他功能表\n\n"

    for purpose in other_purposes:
        if purpose in tables_by_purpose:
            md += f"### {purpose}\n\n"
            for table_name, table_info in tables_by_purpose[purpose]:
                md += generate_table_detail(table_name, table_info)

    # 临时和辅助表
    temp_purposes = ['临时表', '同步临时表', '数据导入表', '备份表', '日志表', '查询视图表']

    md += "## 临时和辅助表\n\n"

    for purpose in temp_purposes:
        if purpose in tables_by_purpose:
            md += f"### {purpose}\n\n"
            for table_name, table_info in tables_by_purpose[purpose]:
                md += generate_table_detail(table_name, table_info)

    # 数据库设计说明
    md += """## 数据库设计说明

### 主要特点

1. **GUID主键设计**: 大部分表使用36位的GUID作为主键，便于分布式部署和数据合并
2. **MyISAM存储引擎**: 适合读多写少的教务系统场景
3. **完善的日志系统**: 包含操作日志、变更日志等多种日志记录
4. **模块化设计**: 按功能模块划分表结构，便于维护
5. **临时表设计**: 使用大量临时表支持数据同步和导入功能
6. **视图支持**: 提供查询视图优化报表性能

### 核心业务流程

1. **会员管理流程**:
   - 会员注册 → 会员卡购买 → 课程购买 → 课时安排 → 上课记录

2. **课程管理流程**:
   - 课程创建 → 教师分配 → 教室安排 → 学员报名 → 上课管理

3. **合同管理流程**:
   - 合同创建 → 课程关联 → 费用支付 → 课时消耗 → 退费管理

4. **员工管理流程**:
   - 员工入职 → 权限分配 → 课程安排 → 薪资计算 → 绩效考核

### 数据完整性

- 使用GUID确保主键唯一性
- 通过业务逻辑保证数据一致性
- 日志记录支持数据追踪和恢复

"""

    return md

def generate_table_detail(table_name, table_info):
    """生成单个表的详细信息"""
    md = f"#### {table_name}\n\n"

    if table_info.get('comment'):
        md += f"**说明**: {table_info['comment']}\n\n"

    md += f"**存储引擎**: {table_info['engine']}\n\n"

    # 主键
    if table_info['primary_keys']:
        md += f"**主键**: {', '.join(table_info['primary_keys'])}\n\n"

    # 字段列表
    if table_info['columns']:
        md += "| 字段名 | 数据类型 | 允许空 | 默认值 | 自增 | 注释 |\n"
        md += "|--------|----------|--------|--------|------|------|\n"

        for col in table_info['columns']:
            nullable = "否" if not col['nullable'] else "是"
            auto_inc = "是" if col['auto_increment'] else "否"
            default = col['default'] or "-"
            comment = col.get('comment') or "-"

            md += f"| {col['name']} | {col['type']} | {nullable} | {default} | {auto_inc} | {comment} |\n"

        md += "\n"

    # 索引信息
    if table_info['indexes']:
        md += "**索引**:\n"
        for idx in table_info['indexes']:
            md += f"- {idx['type']}: {idx['name']} ({', '.join(idx['columns'])})\n"
        md += "\n"

    md += "---\n\n"
    return md

def main():
    """主函数"""
    print("开始分析数据库结构...")

    # 分析SQL文件
    db_structure = analyze_sql_file('/Users/berton/Github/ETM-Plus/database_structure.sql')

    # 保存JSON格式结果
    with open('/Users/berton/Github/ETM-Plus/db_structure.json', 'w', encoding='utf-8') as f:
        json.dump(db_structure, f, ensure_ascii=False, indent=2)

    # 生成Markdown文档
    markdown_content = generate_markdown_doc(db_structure)

    with open('/Users/berton/Github/ETM-Plus/教务系统数据库结构文档.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    print(f"\n分析完成！")
    print(f"数据库名: {db_structure['database']}")
    print(f"表总数: {db_structure['total_tables']}")
    print(f"\n生成的文档:")
    print(f"1. db_structure.json - JSON格式的详细结构数据")
    print(f"2. 教务系统数据库结构文档.md - 完整的数据库文档")

if __name__ == "__main__":
    main()