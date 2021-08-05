import pymysql
import pandas as pd


if __name__ == '__main__':
    val = input("Enter Password: ")
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd=val, db='TechCrunch', charset='utf8')
    cursor = db.cursor()

    sql = "SELECT * FROM articles"
    result = pd.read_sql(sql, db)
