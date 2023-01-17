import requests
import mysql.connector
from bs4 import BeautifulSoup
import os,shutil
import time
from Config import Variable


######################## Script for post on facebook page   ######################### 

def postImage(group_id, img_url,auth_token):
    url = f"https://graph.facebook.com/{group_id}/photos?access_token=" + auth_token
   
    files = {
            'file': open(img_url,'rb'), 
            }
    data = {
        "published" : False
    }
    r = requests.post(url, files=files, data=data).json()
    return r

def multiPostImage(group_id,img_list,auth_token):
    imgs_id = []
    for img in img_list:
        post_id = postImage(group_id ,img,auth_token)
        
        imgs_id.append(post_id['id'])
    tit = open('title1.txt','r')
    titlea = tit.read()     

    args=dict()
    args["message"]=titlea
    for img_id in imgs_id:
        key="attached_media["+str(imgs_id.index(img_id))+"]"

        args[key]="{'media_fbid': '"+img_id+"'}"
    url = f"https://graph.facebook.com/{group_id}/feed?access_token=" + auth_token
    requests.post(url, data=args)

def download_img(img_url,img_folder):
    get_nme = img_url.split("/")[-1]
    image_name = get_nme.split(".")[0]
    f = open(f'{img_folder}/{image_name}.jpg','wb')
    f.write(requests.get(img_url).content)
    f.close()

    return image_name    

def fb_post(post_u,Source_v):

    images_list = []

    page=requests.get(post_u)
    soup= BeautifulSoup(page.content,"html.parser")
    feature_image = soup.findAll(class_=Source_v['FEATURE_IMAGE'])
    internelImage = soup.findAll(class_=Source_v['INTERNEL_IMAGE'])
    
    internelImage_1 = soup.findAll(class_ = Source_v['INTERNEL_IMAGE_1'])

    aaa1=soup.find(class_=Source_v['POST_TITLE']).text

    with open(r"title1.txt","w") as save1:
        save1.write(str(aaa1))

    for aa in feature_image:
        image_n = download_img(aa['src'],Image_folder)
        image_get = os.path.join(Image_folder,image_n+".jpg")
        images_list.append(image_get)
    
    for qw in internelImage:
        image_n = download_img(qw['src'],Image_folder)
        image_get = os.path.join(Image_folder,image_n+".jpg")
        images_list.append(image_get)

    for qw12 in internelImage_1:
        image_n = download_img(qw12['src'],Image_folder)
        image_get = os.path.join(Image_folder,image_n+".jpg")
        images_list.append(image_get)

    multiPostImage(Source_v['PAGE_ID'],images_list[0:3],Source_v['PAGE_TOKEN'])

def main(Source_v,mydb):
    page = requests.get(Source_v['SOURCE_URL'])

    soup = BeautifulSoup(page.content,'xml')

    itema = soup.find('item')
    get_post_time = (itema.find('pubDate').text)

    if Source_v['POST_TIME'] != get_post_time:
        mycursor = mydb.cursor()
        sql = "UPDATE post_fb SET post_time = '{0}' WHERE Source_Name = '{1}'".format(get_post_time,Source_v['SOURCE_NAME'])
        mycursor.execute(sql)
        mydb.commit()
        post_link = (itema.find("link").text).replace("#respond",'')
        return post_link 
    else:
        return False


if __name__ == "__main__":

    ################## script path #######################

    Script_path = os.getcwd()
    Image_folder = os.path.join(Script_path,"image")
    
    ######################################################
    print("start project")

    while True:
        source_list = ["bulletinxp","therconline"]
        for sour_name in source_list:

            vari = Variable(sour_name)
            ######################## define #############################

            # vari[0] is all variable
            # vari[1] is database

            ##############################################################

            if (os.path.exists(Image_folder)) is not True:
                os.mkdir(Image_folder)

            check_post = main(vari[0],vari[1])
            try:
                if check_post is not False:
                    fb_post(check_post,vari[0])
                    shutil.rmtree(Image_folder)
                else:
                    pass
            except:
                print("=================== please check the tocken ======================")    
        time.sleep(15)
        
