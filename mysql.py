import pymysql

"""
使用python操作mysql数据库示例
"""


def select_list(sql):
    """
    查询mysql数据库数据
    :param sql: 查询的语句，示例：select * from test
    :return: 查询到的数据的list集合列表
    """
    result_list = []
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
    cur = conn.cursor()
    cur.execute(query=sql)
    while 1:
        res = cur.fetchone()
        if res is None:
            break
        result_list.append(res)
    cur.close()
    conn.close()
    return result_list


def insert(table_name, columns_list, data_list):
    """
    插入多条mysql记录
    :param table_name: 要插入数据的mysql表名
    :param columns_list: 插入数据的mysql表的字段名称list列表
    :param data_list: 要插入的数据list列表，注意顺序要和字段列表顺序一致
    :return: NONE
    """
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
    cur = conn.cursor()
    s_count = len(columns_list) * "%s,"
    columns = ','.join(columns_list)
    cur.executemany(query='insert into ' + table_name + "(" + columns + ") values (" + s_count[:-1] + ")", args=data_list)
    conn.commit()
    cur.close()
    conn.close()


def update(sql):
    """
    更新mysql的记录
    :param sql: 更新的sql语句，示例: update test set name='张三' where id=1
    :return: NONE
    """
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
    cur = conn.cursor()
    cur.execute(query=sql)
    conn.commit()
    cur.close()
    conn.close()


def delete(sql):
    """
    删除mysql数据库记录
    :param sql: 删除的sql语句，示例：delete from test where id=1
    :return: NONE
    """
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='test')
    cur = conn.cursor()
    cur.execute(query=sql)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    """
    测试
    CREATE TABLE `test` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      `age` int DEFAULT NULL,
      `sex` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    """
    # 测试插入数据
    columns_list = ["name", "age", "sex"]
    data_list = [('jack', 20, '男'), ('alice', 18, '女'), ('tom', 23, '男')]
    insert(table_name='test', columns_list=columns_list, data_list=data_list)

    # 测试查询数据
    result_list = select_list(sql="select * from test")
    print(result_list)

    # 测试修改数据
    update(sql="update test set age=22 where id = 2")
    result_list = select_list(sql="select * from test")
    print(result_list)

    # 测试删除数据
    delete(sql="delete from test where id = 1")
    result_list = select_list(sql="select * from test")
    print(result_list)