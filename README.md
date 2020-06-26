# 1. 工具说明
该工具可以生成mysql数据库中对应的表结构，生成的文件为markdown格式
# 2. 如何安装
项目已发布到PyPI，可以使用命令
pip install mysql2md / pip3 install mysql2md
进行安装
# 3. 如何使用
在命令行中使用
python -m mysql2md.mysql2md
# 4. 参数说明
  -H HOST, --host HOST  数据库host地址 默认为本机地址
  -P PORT, --port PORT  数据库端口 默认为3306
  -u USER, --user USER  数据库用户名
  -p PASSWORD, --password PASSWORD
                        数据库密码
  -d DBNAME, --dbname DBNAME
                        数据库名称
  -t TABLENAME, --tablename TABLENAME
                        表名称，支持使用下划线或百分号进行模糊匹配
  -f FILE, --file FILE  输出的文件名称，文件自动以md结尾