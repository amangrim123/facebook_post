import requests
import mysql.connector
from bs4 import BeautifulSoup
import os,shutil
import time
from Config import Variable
import cv2
import logging
from PIL import Image, ImageDraw, ImageFont, ImageFilter


######################## Script for post on facebook page   ######################### 

def break_long_title(my_txt):
    with open("texta.txt",'w') as ff:
        ff.write(my_txt)
    ff.close()
    rr1 = open('texta.txt','r')
    rr2 = rr1.read()
    ff3 = rr2.split(' ')
    for i in range(7,len(ff3),7):
        ffa =  open("texta.txt",'r')
        new_ff = ffa.read()
        add_new = new_ff.replace(ff3[i]+' ',ff3[i]+"\n")
        with open("texta.txt",'w') as final_f:
            final_f.write(add_new)

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

def add_site_name_on_image(img_path):
    bg = Image.open(img_path).convert('RGB')
    x = bg.width//2
    y = bg.height//2

    # The text we want to add
    # rr1 = open('texta.txt','r')
    # rr2 = rr1.read()
   
    # Create font
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 25)

    # Draw on sharp text
    draw = ImageDraw.Draw(bg)
    draw.text(xy=(590, 597), text=sour_name.upper(), fill="green",font=font, anchor='mm')

    bg.save(img_path)
              

def add_box_on_image(img_path):
    image = Image.open(img_path)
    logo = Image.open('box_on.png')
    image_copy = image.copy()
    position = ((0), (0))
    image_copy.paste(logo, position,mask=logo)
    image_copy.save(img_path)
    add_text_on_image(img_path)  

def img_resize(img_path):
    image = Image.open(img_path)
    new_image = image.resize((1160, 630))
    new_image.save(img_path)
    add_box_on_image(img_path)    

def add_text_on_image(img_path):
    bg = Image.open(img_path).convert('RGB')
    x = bg.width//2
    y = bg.height//2

    # The text we want to add
    rr1 = open('texta.txt','r')
    rr2 = rr1.read()
   
    # Create font
    # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30,encoding="unic")
    font = ImageFont.truetype('fonts\ARLRDBD.TTF',30)

    # Create piece of canvas to draw text on and blur
    blurred = Image.new('RGBA', bg.size)
    draw = ImageDraw.Draw(blurred)
    draw.text(xy=(582,542), text=rr2, fill='blue', font=font, anchor='mm')
    blurred = blurred.filter(ImageFilter.BoxBlur(1))

    # Paste soft text onto background
    bg.paste(blurred,blurred)

    # Draw on sharp text
    draw = ImageDraw.Draw(bg)
    draw.text(xy=(582,540), text=rr2, fill='white',font=font, anchor='mm')

    draw = ImageDraw.Draw(bg)
    draw.text(xy=(590, 597), text=sour_name.upper(), fill="green",font=font, anchor='mm')

    bg.save(img_path)

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
    f = open(f'{img_folder}/{image_name}.png','wb')
    f.write(requests.get(img_url).content)
    f.close()

    return image_name    

def fb_post(post_u,Source_v):
    # print("start pto")
    # print(post_u)

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
        # print(aa[Source_v['IMAGE_SRC']])
        image_n = download_img(aa[Source_v['IMAGE_SRC']],Image_folder)
        image_get = os.path.join(Image_folder,image_n+".png")
        images_list.append(image_get)
    try:
        for qw in internelImage:
            image_n = download_img(qw['src'],Image_folder)
            image_get = os.path.join(Image_folder,image_n+".png")
            images_list.append(image_get)

        for qw12 in internelImage_1:
            image_n = download_img(qw12['src'],Image_folder)
            image_get = os.path.join(Image_folder,image_n+".png")
            images_list.append(image_get)
    except:
        pass        
    
    break_long_title(str(aaa1))
    img_resize(images_list[0])
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
    Font_folder = os.path.join(Script_path,"fonts")
    
    ######################################################
    print(" === start project ==== ")
    logging.basicConfig(filename="facebook_automation_log.log", level=logging.INFO)
    while True:
        try:
            source_list = check_site_status()
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
                        print("done = ",sour_name)
                    else:
                        pass  
                except:         
                    logging.error(f"=================== please check the tocken for {sour_name} ======================")    
            time.sleep(15)
        except Exception as eee:
            logging.error(eee)