# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class CommonDataSpidersPipeline:
    def __init__(self):
        # connection database
        self.connect = pymysql.connect(host='uaa.metaq.cn', user='root', passwd='123456',port=13306,
                                       db='common_srv')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
                insert into t_area_copy1(code, `name`, p_code,`level`,`order`) VALUES (%s,%s,%s,%s,%s)
                """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql,
                            (item['code'], item['name'], item['p_code'], str(item['level']), str(item['order'])
                             ))
        # 提交，不进行提交无法保存到数据库
        self.connect.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()
