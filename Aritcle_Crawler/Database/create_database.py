import pymysql
from Aritcle_Crawler.Gather_data.gather_techcruch import *

def drop_tables(table_name, db) :

    cursor = db.cursor()
    sql = "SHOW TABLES LIKE '" + table_name + "'"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        sql = "DROP TABLE articles"
        cursor.execute(sql)



if __name__ == '__main__':
    article_df, author_df = get_articles(10000)


    val = input("Enter Password: ")
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd=val, db='TechCrunch', charset='utf8')
    cursor = db.cursor()

    drop_tables('articles', db)
    drop_tables('author', db)

    sql = '''
    CREATE TABLE articles (
        num INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        title VARCHAR(1000) NOT NULL,
        link  VARCHAR(2083) NOT NULL,
        author  VARCHAR(50) NOT NULL,
        article_date DATE NOT NULL,
        content TEXT NOT NULL
    );
    '''
    cursor.execute(sql)


    sql = '''
    CREATE TABLE author (
        num INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        author VARCHAR(50) NOT NULL,
        account_id VARCHAR(50) NOT NULL,
        account_link  VARCHAR(2083) NOT NULL
    );
    '''
    cursor.execute(sql)

    # import pdb;
    # pdb.set_trace()

    sql_list = article_df.apply( lambda row : "INSERT INTO articles (title, link, author, article_date, content) VALUES('" +
                                   str(row["Title"].replace("'", "\"")) + "','" + str(row["Link"])+ "','" + str(row["author"])+
                                   "','" + str(row["time"])+ "','" +  str(row["text"].replace("'", "\"")) + "')", axis =1)
    for sql_line in sql_list :
        cursor.execute(sql_line)

    sql_list = author_df.apply( lambda row : "INSERT INTO author (author,account_id, account_link) VALUES('" +
                                   row["author"] + "','" + row["account"]+ "','" + row["account_link"]+ "')", axis =1)

    for sql_line in sql_list :
        cursor.execute(sql_line)

    db.commit()
    db.close()