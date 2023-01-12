import requests
from bs4 import BeautifulSoup
import os,shutil
import time


######################## Script for therc online  ######################### 

# auth_token = "EAAOWRIDVYF8BALYFFZAthwQpuLBUunYRZAqoZCcxIlObkJVD2ZB5lkkPet7ZA6BXDju9M9EafYIhTwIamfOF5Cz1N5sZBzM43iSRFMIpwH9bA5bLwV8aLQa8lZABZCEXwEQPnc7ymrqha2unrRYTAxrHqFadvESZBzNHJonUq9fKzHn1rDhoe4HuWwrPNG1X793oZD"
auth_token = "EABSzXdolOtABAFy6s9CCVGhLNQqZALfkAN1GzRqg6HiFfycRiNJ80Pdtt5gCXMXm9CWdF1ZBCDnWoKw0yN8gZBMAfDolQe8bz2avNotiFrN2QzVcxBFg17bbcYDCNGUZCLFuevlzXeGVkK3s66LKyTxIAZCiOQE7DVaVbqpoZAKnV7eLOxhUl7Aqy95uK4O3QZD"
def postImage(group_id, img_url):
    url = f"https://graph.facebook.com/{group_id}/photos?access_token=" + auth_token
   
    files = {
            'file': open(img_url,'rb'), 
            }
    data = {
        "published" : False
    }
    r = requests.post(url, files=files, data=data).json()
    return r

def multiPostImage(group_id,img_list):
    imgs_id = []
    for img in img_list:
        post_id = postImage(group_id ,img)
        
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

def fb_post(hello):
    page_id = 107329725577307

    images_list = []

    page=requests.get(hello)
    soup= BeautifulSoup(page.content,"html.parser")
    feature_image = soup.findAll(class_="attachment-csco-large size-csco-large wp-post-image")
    aaa = soup.findAll(class_="aligncenter")
    
    aaa12 = soup.findAll(class_ = "alignnone")

    aaa1=soup.find(class_="cs-entry__header-info").find("h1").text

    with open(r"title1.txt","w") as save1:
        save1.write(str(aaa1))

    for aa in feature_image:
        image_n = download_img(aa['src'],Image_folder)
        image_get = os.path.join(Image_folder,image_n+".jpg")
        images_list.append(image_get)
    
    for qw in aaa:
        image_n = download_img(qw['src'],Image_folder)
        image_get = os.path.join(Image_folder,image_n+".jpg")
        images_list.append(image_get)

    for qw12 in aaa12:
        image_n = download_img(qw12['src'],Image_folder)
        image_get = os.path.join(Image_folder,image_n+".jpg")
        images_list.append(image_get)

    multiPostImage(page_id,images_list[0:3])

def main():
    page = requests.get("https://www.therconline.com/feed/")

    soup = BeautifulSoup(page.content,'html.parser')

    itema = soup.find('item')
    get_post_time = (itema.find('pubdate').text)

    try:

        ff = open('times.txt','r')
        hf = ff.read()

        if hf != get_post_time:
            f = open("times.txt",'w')
            f.write(get_post_time)
            post_link = (itema.find("comments").text).replace("#respond",'')
            return post_link 
        else:
            return False
    except:
        post_link = (itema.find("comments").text).replace("#respond",'')
        f = open("times.txt",'w')
        f.write(get_post_time)
        return post_link



if __name__ == "__main__":

    ############################### script path #######################

    Script_path = os.getcwd()
    Image_folder = os.path.join(Script_path,"image")
    if (os.path.exists(Image_folder)) is not True:
        os.mkdir(Image_folder)
    #############################################################
    print("start project")
    # page_id = 101071396211987
    while True:
        hello = main()
        try:
            if hello is not False:
                fb_post(hello)
                shutil.rmtree(Image_folder)
            else:
                pass
        except:
            print(" ============ the token is expired ========== ")    
        time.sleep(60)
        
