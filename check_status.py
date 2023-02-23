import mysql.connector


def check_site_status():
    mydb = mysql.connector.connect(  
        host="64.227.176.243",
        user="phpmyadmin",
        password="Possibilities123.@",
        database="facebook_post"
    )

    mycursor = mydb.cursor()

    sql = "SELECT Source_Name FROM post_fb where status = '1'"

    mycursor.execute(sql)

    facebook_table = mycursor.fetchall()
    site_name = []
    for ii in facebook_table:
        site_name.append(ii[0])
    return site_name

hello = check_site_status()
print(hello)    



