#!/usr/bin/python3
# coding:utf-8
import pymysql
import argparse

# 以markdown格式输出到文件
def output_to_md_file(table_name, table_comment, columns, output_file):
    output_file.write(table_name + ' ')
    output_file.write(table_comment)
    output_file.write('\r\n')
    output_file.write('| 列名称 | 字段类型 | 是否为空 | 键 | 默认值 | 备注 |')
    output_file.write('\n')
    output_file.write('| ----- | -------- | ------- | -- | ----- | ---- |')
    for column_item in columns:
        if column_item is not None and len(column_item) == 6:
            # 列名称
            column_name = column_item[0]
            if column_name is not None:
                column_name = column_name.replace('\r\n', '')
            # 字段类型
            column_type = column_item[1]
            if column_type is not None:
                column_type = column_type.replace('\r\n', '')
            # 是否为空
            column_is_null = column_item[2]
            if column_is_null is not None:
                column_is_null = column_is_null.replace('\r\n', '')
            # 键
            column_key_type = column_item[3]
            if column_key_type is not None:
                column_key_type = column_key_type.replace('\r\n', '')
            # 默认值
            column_default = column_item[4]
            if column_default is not None:
                column_default = column_default.replace('\r\n', '')
            # 备注
            column_comment = column_item[5]
            if column_comment is not None:
                column_comment = column_comment.replace('\r\n', '')

            output_file.write('\n')
            column_str = "| {} | {} | {} | {} | {} | {} |" \
                .format(column_name, column_type, column_is_null, column_key_type, column_default, column_comment)

            output_file.write(column_str)
    output_file.write('\r\n')
    output_file.write('\r\n')


def create():
    ap = argparse.ArgumentParser()
    ap.add_argument('-H', '--host', required=False, help="数据库host地址 默认为本机地址", default='localhost')
    ap.add_argument('-P', '--port', required=False, help="数据库端口 默认为3306", default=3306)
    ap.add_argument('-u', '--user', required=True, help="数据库用户名")
    ap.add_argument('-p', '--password', required=True, help="数据库密码")
    ap.add_argument('-d', '--dbname', required=True, help="数据库名称")
    ap.add_argument('-t', '--tablename', required=False, help="表名称，支持使用下划线或百分号进行模糊匹配")
    ap.add_argument('-f', '--file', required=True, help="输出的文件名称，文件自动以md结尾")
    args = vars(ap.parse_args())
    host = args.get('host')
    port = int(args.get('port'))
    user = args.get('user')
    password = args.get('password')
    dbname = args.get('dbname')
    table_name = args.get('tablename')
    file_name = args.get('file')

    # 连接数据库
    conn = pymysql.connect(host=host, port=port, user=user, password=password)
    # 创建输出文件
    output_file = open(file_name + '.md', encoding='utf-8', mode='w')
    # 获取游标
    cursor = conn.cursor()
    # 执行查询某个数据库中的指定表的所有表名称的sql
    table_name_sql = '''SELECT
                            DISTINCT table_name
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE table_schema = '{}' '''.format(dbname)
    # 如果输入的表名称不为空，则追加表名称查询条件
    if table_name is not None and len(table_name) > 0:
        table_name_sql += "AND table_name LIKE '{}'".format(table_name)
    cursor.execute(table_name_sql)
    tables = cursor.fetchall()
    # 遍历出所有的表名称
    for table_item in tables:
        # 获取每个表的表名称
        table_name = table_item[0]
        # 查询该表对应的注释内容
        table_comment_sql = '''
                SELECT
                    table_comment
                FROM
                    information_schema.TABLES
                WHERE
                    table_schema = '{}'
                    AND table_name = '{}'
                    '''.format(dbname, table_name)
        cursor.execute(table_comment_sql)
        table_comment = cursor.fetchone()

        # 开始查询该表对应的字段说明
        column_name_sql = '''
            SELECT
                COLUMN_NAME 列名,
                COLUMN_TYPE 字段类型,
                IS_NULLABLE 是否为空,
                COLUMN_KEY 键,
                COLUMN_DEFAULT 默认值,
                COLUMN_COMMENT 备注
            FROM
                INFORMATION_SCHEMA.COLUMNS
                WHERE -- table_schema 指定要查询的数据库名称
                table_schema = '{}'
                -- table_name 为指定的表名称
                AND table_name = '{}' '''.format(dbname, table_name)
        # 查询该表的表结构
        cursor.execute(column_name_sql)
        columns = cursor.fetchall()
        # 把每一个表的名称注释以及表的所有字段对应的类型及相关说明以markdown形式写入文件中
        output_to_md_file(table_name, table_comment[0], columns, output_file)

if __name__ == '__main__':
    create()
