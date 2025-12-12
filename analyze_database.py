#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库结构分析工具
分析MySQL数据库结构文件，生成完整的数据库文档
"""

import re
import json
from collections import defaultdict
from typing import Dict, List, Tuple, Any

class DatabaseAnalyzer:
    def __init__(self, sql_file_path: str):
        self.sql_file_path = sql_file_path
        self.tables = {}
        self.current_database = None
        self.foreign_keys = defaultdict(list)

    def analyze(self) -> Dict:
        """分析整个SQL文件"""
        with open(self.sql_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 分割成多个语句
        statements = self._split_statements(content)

        for stmt in statements:
            self._parse_statement(stmt)

        return self._generate_document()

    def _split_statements(self, content: str) -> List[str]:
        """将SQL文件分割成多个语句"""
        # 移除注释
        content = re.sub(r'--.*?\n', '', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

        # 分割语句
        statements = []
        current_stmt = ""
        in_string = False
        string_char = None

        for char in content:
            if char in ("'", '"') and (not current_stmt.endswith('\\') or current_stmt.endswith('\\\\')):
                in_string = not in_string
                if in_string:
                    string_char = char
                else:
                    string_char = None

            if char == ';' and not in_string:
                if current_stmt.strip():
                    statements.append(current_stmt.strip())
                current_stmt = ""
            else:
                current_stmt += char

        if current_stmt.strip():
            statements.append(current_stmt.strip())

        return statements

    def _parse_statement(self, stmt: str):
        """解析单个SQL语句"""
        stmt = stmt.strip()

        # 解析数据库创建
        if stmt.upper().startswith('CREATE DATABASE'):
            match = re.search(r'CREATE DATABASE[^`]*`([^`]+)`', stmt, re.IGNORECASE)
            if match:
                self.current_database = match.group(1)

        # 解析使用数据库
        elif stmt.upper().startswith('USE '):
            match = re.search(r'USE\s+`([^`]+)`', stmt, re.IGNORECASE)
            if match:
                self.current_database = match.group(1)

        # 解析表创建
        elif stmt.upper().startswith('CREATE TABLE'):
            self._parse_create_table(stmt)

    def _parse_create_table(self, stmt: str):
        """解析CREATE TABLE语句"""
        # 提取表名
        table_match = re.search(r'CREATE TABLE\s+(?:IF NOT EXISTS\s+)?`([^`]+)`', stmt, re.IGNORECASE)
        if not table_match:
            return

        table_name = table_match.group(1)

        # 提取表内容（匹配从第一个(到ENGINE之前的内容）
        content_match = re.search(r'CREATE TABLE\s+.*?\((.*?)\)\s*ENGINE', stmt, re.IGNORECASE | re.DOTALL)
        if not content_match:
            return

        table_content = content_match.group(1)

        # 提取引擎信息
        engine_match = re.search(r'ENGINE\s*=\s*(\w+)', stmt, re.IGNORECASE)
        engine = engine_match.group(1) if engine_match else 'Unknown'

        # 提取字符集
        charset_match = re.search(r'CHARSET\s*=\s*(\w+)', stmt, re.IGNORECASE)
        charset = charset_match.group(1) if charset_match else 'Unknown'

        # 解析字段
        columns = []
        primary_keys = []
        indexes = []
        foreign_keys = []

        # 分割字段定义
        field_definitions = self._split_table_fields(table_content)

        for field_def in field_definitions:
            field_def = field_def.strip()
            if not field_def:
                continue

            # 解析主键
            if field_def.upper().startswith('PRIMARY KEY'):
                pk_match = re.search(r'PRIMARY KEY\s*\(`?([^`)]+)`?\)', field_def, re.IGNORECASE)
                if pk_match:
                    primary_keys.append(pk_match.group(1))
                continue

            # 解析索引
            if field_def.upper().startswith(('KEY', 'INDEX', 'UNIQUE')):
                index_match = re.search(r'(?:KEY|INDEX|UNIQUE)\s*`?(\w+)?`?\s*\(([^)]+)\)', field_def, re.IGNORECASE)
                if index_match:
                    index_name = index_match.group(1) or 'Unnamed'
                    index_columns = [c.strip().strip('`') for c in index_match.group(2).split(',')]
                    indexes.append({
                        'name': index_name,
                        'columns': index_columns,
                        'type': 'UNIQUE' if field_def.upper().startswith('UNIQUE') else 'INDEX'
                    })
                continue

            # 解析外键
            if field_def.upper().startswith('CONSTRAINT') or field_def.upper().startswith('FOREIGN KEY'):
                fk_match = re.search(r'(?:CONSTRAINT\s+`?(\w+)`?\s+)?FOREIGN KEY\s*\(`?([^`)]+)`?\)\s*REFERENCES\s+`?([^`]+)`?\s*\(`?([^`)]+)`?\)', field_def, re.IGNORECASE)
                if fk_match:
                    constraint_name = fk_match.group(1) or f'fk_{table_name}_{fk_match.group(2)}'
                    foreign_keys.append({
                        'constraint_name': constraint_name,
                        'column': fk_match.group(2),
                        'references_table': fk_match.group(3),
                        'references_column': fk_match.group(4)
                    })
                continue

            # 解析普通字段
            column = self._parse_column(field_def)
            if column:
                columns.append(column)

        # 保存表信息
        self.tables[table_name] = {
            'database': self.current_database,
            'engine': engine,
            'charset': charset,
            'columns': columns,
            'primary_keys': primary_keys,
            'indexes': indexes,
            'foreign_keys': foreign_keys,
            'row_count': None,
            'comment': self._extract_table_comment(stmt)
        }

        # 收集所有外键关系
        for fk in foreign_keys:
            self.foreign_keys[fk['references_table']].append({
                'table': table_name,
                'column': fk['column'],
                'references_column': fk['references_column'],
                'constraint_name': fk['constraint_name']
            })

    def _split_table_fields(self, content: str) -> List[str]:
        """分割表字段定义"""
        fields = []
        current_field = ""
        in_parentheses = 0

        for char in content:
            if char == '(':
                in_parentheses += 1
            elif char == ')':
                in_parentheses -= 1

            if char == ',' and in_parentheses == 0:
                if current_field.strip():
                    fields.append(current_field.strip())
                current_field = ""
            else:
                current_field += char

        if current_field.strip():
            fields.append(current_field.strip())

        return fields

    def _parse_column(self, field_def: str) -> Dict[str, Any]:
        """解析单个列定义"""
        # 基本格式：`name` type [options]
        match = re.match(r'`([^`]+)`\s+(\w+(?:\([^)]+\))?(?:\s+\w+)*)\s*(.*)', field_def, re.IGNORECASE)
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

        # 解析选项
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

    def _extract_table_comment(self, stmt: str) -> str:
        """提取表注释"""
        comment_match = re.search(r"COMMENT\s*=\s*'([^']+)'", stmt, re.IGNORECASE)
        return comment_match.group(1) if comment_match else None

    def _generate_document(self) -> Dict:
        """生成数据库文档"""
        doc = {
            'database_info': {
                'name': self.current_database,
                'total_tables': len(self.tables),
                'mysql_version': '5.0.67-community-nt',
                'export_time': None
            },
            'tables': {},
            'relationships': []
        }

        # 整理表信息
        for table_name, table_info in self.tables.items():
            doc['tables'][table_name] = {
                'name': table_name,
                'database': table_info['database'],
                'engine': table_info['engine'],
                'charset': table_info['charset'],
                'columns': table_info['columns'],
                'primary_keys': table_info['primary_keys'],
                'indexes': table_info['indexes'],
                'foreign_keys': table_info['foreign_keys'],
                'comment': table_info['comment'],
                'referenced_by': self.foreign_keys.get(table_name, []),
                'purpose': self._infer_table_purpose(table_name, table_info)
            }

        # 整理关系
        for table_name, table_info in self.tables.items():
            for fk in table_info['foreign_keys']:
                doc['relationships'].append({
                    'from_table': table_name,
                    'from_column': fk['column'],
                    'to_table': fk['references_table'],
                    'to_column': fk['references_column'],
                    'constraint_name': fk['constraint_name']
                })

        return doc

    def _infer_table_purpose(self, table_name: str, table_info: Dict) -> str:
        """推断表的用途"""
        name_lower = table_name.lower()

        # 根据表名推断用途
        if 'member' in name_lower or 'membertemp' in name_lower:
            return '会员/用户相关表'
        elif 'card' in name_lower:
            return '会员卡相关表'
        elif 'course' in name_lower:
            return '课程相关表'
        elif 'contract' in name_lower:
            return '合同相关表'
        elif 'lesson' in name_lower:
            return '课时相关表'
        elif 'manager' in name_lower:
            return '员工/管理员相关表'
        elif 'payment' in name_lower or 'wages' in name_lower:
            return '财务相关表'
        elif 'product' in name_lower:
            return '产品相关表'
        elif 'msg' in name_lower or 'mail' in name_lower:
            return '消息相关表'
        elif 'wx' in name_lower:
            return '微信相关表'
        elif 'temp' in name_lower:
            return '临时表'
        elif name_lower.startswith('k_'):
            return '系统框架表'
        elif name_lower.startswith('d_'):
            return '教学相关表'
        elif name_lower.startswith('q_'):
            return '查询视图表'
        elif name_lower.startswith('fstemp_'):
            return '同步临时表'
        else:
            return '系统功能表'

def main():
    analyzer = DatabaseAnalyzer('/Users/berton/Github/ETM-Plus/database_structure.sql')
    doc = analyzer.analyze()

    # 保存分析结果
    with open('/Users/berton/Github/ETM-Plus/database_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

    # 生成Markdown文档
    generate_markdown_doc(doc)

    print(f"\n数据库分析完成！")
    print(f"数据库名: {doc['database_info']['name']}")
    print(f"表总数: {doc['database_info']['total_tables']}")
    print(f"关系总数: {len(doc['relationships'])}")
    print(f"\n详细文档已保存到:")
    print(f"1. database_analysis.json - JSON格式分析结果")
    print(f"2. database_structure.md - Markdown格式文档")

def generate_markdown_doc(doc: Dict):
    """生成Markdown格式的数据库文档"""
    md_content = f"""# 教务系统数据库结构文档

## 数据库基本信息

- **数据库名称**: {doc['database_info']['name']}
- **MySQL版本**: {doc['database_info']['mysql_version']}
- **表总数**: {doc['database_info']['total_tables']}
- **字符集**: UTF-8
- **存储引擎**: 主要为MyISAM

## 目录

1. [核心业务表](#核心业务表)
   - [会员管理](#会员管理)
   - [课程管理](#课程管理)
   - [合同管理](#合同管理)
   - [课时管理](#课时管理)
   - [员工管理](#员工管理)
2. [系统功能表](#系统功能表)
   - [系统框架](#系统框架)
   - [消息通知](#消息通知)
   - [财务管理](#财务管理)
   - [产品管理](#产品管理)
3. [临时和辅助表](#临时和辅助表)
4. [数据关系图](#数据关系图)

---

## 核心业务表

### 会员管理

"""

    # 按用途分组表
    tables_by_purpose = defaultdict(list)
    for table_name, table_info in doc['tables'].items():
        purpose = table_info['purpose']
        tables_by_purpose[purpose].append((table_name, table_info))

    # 生成会员管理部分
    if '会员/用户相关表' in tables_by_purpose:
        md_content += "#### 会员信息表\n\n"
        for table_name, table_info in tables_by_purpose['会员/用户相关表']:
            md_content += generate_table_doc(table_name, table_info)

    # 生成会员卡相关
    if '会员卡相关表' in tables_by_purpose:
        md_content += "#### 会员卡管理\n\n"
        for table_name, table_info in tables_by_purpose['会员卡相关表']:
            md_content += generate_table_doc(table_name, table_info)

    # 继续其他部分...
    md_content += generate_other_sections(tables_by_purpose, doc)

    # 保存Markdown文档
    with open('/Users/berton/Github/ETM-Plus/database_structure.md', 'w', encoding='utf-8') as f:
        f.write(md_content)

def generate_table_doc(table_name: str, table_info: Dict) -> str:
    """生成单个表的文档"""
    doc = f"##### {table_name}\n\n"

    if table_info['comment']:
        doc += f"**说明**: {table_info['comment']}\n\n"

    doc += f"**用途**: {table_info['purpose']}\n\n"
    doc += f"**存储引擎**: {table_info['engine']}\n\n"
    doc += f"**字符集**: {table_info['charset']}\n\n"

    # 主键
    if table_info['primary_keys']:
        doc += f"**主键**: {', '.join(table_info['primary_keys'])}\n\n"

    # 字段列表
    doc += "| 字段名 | 数据类型 | 允许空 | 默认值 | 自增 | 注释 |\n"
    doc += "|--------|----------|--------|--------|------|------|\n"

    for col in table_info['columns']:
        nullable = "是" if col['nullable'] else "否"
        auto_inc = "是" if col['auto_increment'] else "否"
        default = col['default'] or "-"
        comment = col['comment'] or "-"

        doc += f"| {col['name']} | {col['type']} | {nullable} | {default} | {auto_inc} | {comment} |\n"

    doc += "\n"

    # 外键关系
    if table_info['foreign_keys']:
        doc += "**外键关系**:\n"
        for fk in table_info['foreign_keys']:
            doc += f"- {fk['column']} → {fk['references_table']}.{fk['references_column']}\n"
        doc += "\n"

    # 被引用关系
    if table_info['referenced_by']:
        doc += "**被以下表引用**:\n"
        for ref in table_info['referenced_by']:
            doc += f"- {ref['table']}.{ref['column']}\n"
        doc += "\n"

    doc += "---\n\n"
    return doc

def generate_other_sections(tables_by_purpose: Dict, doc: Dict) -> str:
    """生成其他部分的文档"""
    content = ""

    # 课程管理
    content += "### 课程管理\n\n"
    for purpose in ['课程相关表', '课时相关表']:
        if purpose in tables_by_purpose:
            for table_name, table_info in tables_by_purpose[purpose]:
                content += generate_table_doc(table_name, table_info)

    # 合同管理
    content += "### 合同管理\n\n"
    if '合同相关表' in tables_by_purpose:
        for table_name, table_info in tables_by_purpose['合同相关表']:
            content += generate_table_doc(table_name, table_info)

    # 员工管理
    content += "### 员工管理\n\n"
    if '员工/管理员相关表' in tables_by_purpose:
        for table_name, table_info in tables_by_purpose['员工/管理员相关表']:
            content += generate_table_doc(table_name, table_info)

    # 系统功能表
    content += "## 系统功能表\n\n"

    # 系统框架
    content += "### 系统框架\n\n"
    if '系统框架表' in tables_by_purpose:
        for table_name, table_info in tables_by_purpose['系统框架表']:
            content += generate_table_doc(table_name, table_info)

    # 消息通知
    content += "### 消息通知\n\n"
    if '消息相关表' in tables_by_purpose:
        for table_name, table_info in tables_by_purpose['消息相关表']:
            content += generate_table_doc(table_name, table_info)

    # 财务管理
    content += "### 财务管理\n\n"
    if '财务相关表' in tables_by_purpose:
        for table_name, table_info in tables_by_purpose['财务相关表']:
            content += generate_table_doc(table_name, table_info)

    # 产品管理
    content += "### 产品管理\n\n"
    if '产品相关表' in tables_by_purpose:
        for table_name, table_info in tables_by_purpose['产品相关表']:
            content += generate_table_doc(table_name, table_info)

    # 临时和辅助表
    content += "## 临时和辅助表\n\n"
    for purpose in ['临时表', '同步临时表', '查询视图表']:
        if purpose in tables_by_purpose:
            for table_name, table_info in tables_by_purpose[purpose]:
                content += generate_table_doc(table_name, table_info)

    # 数据关系
    content += "## 数据关系图\n\n"
    content += "### 主要外键关系\n\n"
    content += "| 子表 | 子表字段 | 父表 | 父表字段 |\n"
    content += "|------|----------|------|----------|\n"

    for rel in doc['relationships'][:50]:  # 显示前50个关系
        content += f"| {rel['from_table']} | {rel['from_column']} | {rel['to_table']} | {rel['to_column']} |\n"

    content += "\n### 系统架构说明\n\n"
    content += """本教务系统采用模块化设计，主要包含以下核心模块：

1. **会员管理模块**：管理学员信息、会员卡、课程购买等
2. **课程管理模块**：管理课程信息、课时安排、教师分配等
3. **合同管理模块**：管理学员合同、费用、退费等
4. **员工管理模块**：管理员工信息、权限、薪资等
5. **财务管理模块**：管理收支、工资、采购等
6. **消息通知模块**：管理系统消息、邮件、短信通知等
7. **微信集成模块**：管理微信公众号、小程序等功能

数据库特点：
- 使用MyISAM存储引擎，适合读多写少的教务场景
- 使用GUID作为主键，支持分布式部署
- 完善的日志记录，支持数据追踪
- 丰富的查询视图，提高报表性能
"""

    return content

if __name__ == "__main__":
    main()