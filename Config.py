import mysql.connector


def Variable(source_name):

  mydb = mysql.connector.connect(  
      host="64.227.176.243",
      user="phpmyadmin",
      password="Possibilities123.@",
      database="facebook_post"
  )

  mycursor = mydb.cursor()

  sql = "SELECT * FROM post_fb WHERE Source_Name = '{sourcea}'".format(sourcea = source_name)
  mycursor.execute(sql)
  facebook_table = mycursor.fetchall()[0]

  variables =  {
    "SOURCE_NAME":facebook_table[1],
    "SOURCE_URL" : facebook_table[3],
    "FEATURE_IMAGE" : facebook_table[4],
    "INTERNEL_IMAGE" : facebook_table[5],
    "INTERNEL_IMAGE_1" : facebook_table[6],
    "POST_TIME" : facebook_table[7],
    "POST_TITLE" : facebook_table[8],
    "PAGE_ID" : facebook_table[9],
    "PAGE_TOKEN" : facebook_table[10],
    "IMAGE_SRC": facebook_table[11],
  }

  return variables,mydb