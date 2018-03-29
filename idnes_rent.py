import sys
import urllib3
import lxml.etree
import time
import datetime
import re
import random
import os
import smtplib

http="http://"
hostname="reality.idnes.cz/"
path = "/home/pi/Documents/idnes_proj/buy/"
httpcon = urllib3.PoolManager()
price_reg = re.compile('(\s)+')
pagination_reg = re.compile('([0-9]{1,3})+')
surface_room_reg = re.compile('([[0-9]{1}\+[0-9]{1}|[[0-9]{1}\+kk)+')
surface_flat_reg = re.compile('([0-9]{1,3})+')
pager_idnes="&page={}"
pager_sreality="&strana={}"
hour = [6,8,11,14,17,20]
minute = [51,52,53,54,55,56,57,58,59]

fromaddr = 'bot@email.com'   #email you use to send the best offers - I will call it BOT email
toaddr  = 'your@email.com'  # email where you would like to receive best offers

username = "YourUsername"  # username to your BOT email
password = "YourPassword"   #password tou your BOT email

location_paths={
    "vinohrady":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=Vinohrad&f_kraj%5B%5D=1&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1",
    "praha_1":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=&f_kraj%5B%5D=1&f_okres1%5B%5D=79&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1",
    "karlin":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=Karlin&f_kraj%5B%5D=1&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1",
    "holesovice":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=Holesovice&f_kraj%5B%5D=1&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1",
    "zizkov":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=Zizkov&f_kraj%5B%5D=1&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1",
    "vysehrad":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=Vysehrad&f_kraj%5B%5D=1&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1",
    "vrsovice":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=Vrsovice&f_kraj%5B%5D=1&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1",
    "dejvice":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=Dejvice&f_kraj%5B%5D=1&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1",
    "stresovice":"s/?st=2&f_typ_nabidky%5B%5D=1&isa%5B%5D=1&f_byt%5B%5D=1&f_byt%5B%5D=2&f_byt%5B%5D=3&f_byt%5B%5D=4&lf%5B%5D=1&loc_more=&upresnit=Stresovice&f_kraj%5B%5D=1&cena_od=&cena_do=4000000&plocha_od=&plocha_do=&podlazi_radio=0&podlazi_od=&podlazi_do=&patro_od=&patro_do=&f_s_aktualni=1"}

locations = ["vinohrady",
             "praha_1",
             "karlin",
             "holesovice",
             "zizkov",
             "vysehrad",
             "vrsovice",
             "dejvice",
             "stresovice"]

TEMPLATE_FILE = """Lokalita: {title}
Datum: {date}
Cena: {price}
Poznamka k cene: {price_note}
Popis: {desc}
Odkaz na web: {web_adress}"""

TEMPLATE_EMAIL = """Subject: {title}

Lokalita: {title}
Datum: {date}
Cena: {price}
Poznamka k cene: {price_note}
Popis: {desc}
Odkaz na web: {web_adress}"""

TEMPLATE_IAMALIVE = """I am still hardworking!"""

def get_url(httpcon, url):
    headers = {}
    headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    headers["Accept-Encoding"] = "gzip, deflate"
    headers["Accept-Language"] = "cs,en-us;q=0.7,en;q=0.3"
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"
    #headers["Cookie"]="op_cookie-test=ok;op_oddsportal=cv704mv1ek2l60ijve9iq9hn62;op_user_cookie=32830896;D_UID=739B93C4-5FB3-34AB-A4B5-0C2C36C3347E"
    res=httpcon.urlopen("GET", url, headers=headers)
    
    if res.status!=200:
        print res.status
        raise Exception("Unable to get_url "+url)
    return res.data

def create_file(path,advert_dict):
    for j in advert_dict:
        advert_output = advert_dict[j].split(';')
        with open(path+advert_output[-1]+".txt","w") as fi:
            out = TEMPLATE_FILE.format(title = advert_output[0],
                                  web_adress = advert_output[1],
                                  price = advert_output[2],
                                  price_note = advert_output[3],   
                                  desc = advert_output[4],
                                  date = advert_output[5],
                                  id_advert = advert_output[6])
            fi.write(out)

def get_adverts_from_file(path):
    name_list = []
    for filename in os.listdir(path):
        if ".txt" in filename:
            name_list.append(filename.replace(".txt",""))
    return(name_list)

def send_email(username,password,fromaddr,toaddr,path,advert_dict):
    server = smtplib.SMTP('smtp.gmail.com:587') # if you use gmail
    server.starttls()
    server.login(username,password)
    for k in advert_dict:
        advert_output = advert_dict[k].split(';')
        msg = TEMPLATE_EMAIL.format(title = advert_output[0],
                                  web_adress = advert_output[1],
                                  price = advert_output[2],
                                  price_note = advert_output[3],   
                                  desc = advert_output[4],
                                  date = advert_output[5],
                                  id_advert = advert_output[6])
        server.sendmail(fromaddr, toaddr, msg)
    server.quit()

def get_flats_idnes(httpcon,main_url,old_advert_list,quarter):
    
    htmlparser=lxml.etree.HTMLParser()
    page=get_url(httpcon,main_url)
        
    p=lxml.etree.fromstring(page,htmlparser)
    pagination_xpath = p.xpath(u'body//div[@class="paginator"]/div[@class="paginatorGroup"]/a/text()')
    pagination_list = [str(pagination_reg.findall(m)).strip("[]''""") for m in pagination_xpath]
    pagination_list = filter(None,pagination_list)
    advert_dict = {}
    id_advert_dict = {}
    count = 1
    if len(pagination_list) > 0:
        page_cnt = len(pagination_list)+1
    else:
        page_cnt = 1
##
    for page in range(page_cnt):
        flat_list=p.xpath(u'body//div[@id="listingRealty"]/div[@class="item "]')
        for r in flat_list:
            title_xpath = r.xpath('h2/a/text()')
            web_adress_xpath = r.xpath('h2/a/@href')
            price_xpath = r.xpath('p[@class="price"]/text()')
            price_note_xpath = r.xpath('p[@class="price"]/span[@class="poznamka_cena"]/text()')
            desc_xpath = r.xpath('p[@class="text"]/text()')

            title = title_xpath[0].replace(u'\xb2',"2").encode('cp1250').strip()
            web_adress = http+hostname+web_adress_xpath[0].encode('cp1250')
            id_advert = web_adress.split('/')[-1]
            price = price_xpath[0].encode('cp1250').replace('\xa0','.').replace('\n','')
            if len(price_note_xpath) > 0:
                price_note = price_note_xpath[0].encode('cp1250')
            else:
                price_note = ''
            desc = desc_xpath[0].replace(u'\xb2',"2").replace(u'\u200b',"2").encode('cp1250','ignore').lstrip()
            date = desc_xpath[1].encode('cp1250')
            if id_advert in old_advert_list:
                continue
            else:
                advert_list = title + ';' + web_adress + ';' + str(price) + ';' + price_note + ';' + desc + ';' + date + ';' + id_advert
                advert_dict[count] = advert_list
                id_advert_dict[count] = id_advert
                count += 1
        if page+1 < page_cnt:
            url=main_url+pager_idnes.format(page+2)
            page=get_url(httpcon,url)
            p=lxml.etree.fromstring(page,htmlparser)
        else:
            continue
                    
    send_email(username,password,fromaddr,toaddr,path,advert_dict)
    create_file(path+quarter+"/",advert_dict)

       
def execute_script():
    time.sleep(random.uniform(300,640))

def i_am_alive(current_time,username,password, fromaddr,toaddr):
    if current_time.hour in hour and current_time.minute in minute:
        server = smtplib.SMTP('smtp.gmail.com:587') #if you use gmail
        server.starttls()
        server.login(username,password)
        msg = "iDnes buy - I am still hardworking!"
        server.sendmail(fromaddr, toaddr, msg)
        server.quit()
    
while True:
    tstart=time.time()
    for i in locations:
        old_advert_list = get_adverts_from_file(path+i+"/")
        get_flats_idnes(httpcon,http+hostname+location_paths[i],old_advert_list,i)
    current_time = datetime.datetime.now()
    print current_time
    print "total time",time.time()-tstart
    print "iDNES.py"
    i_am_alive(current_time,username,password, fromaddr,toaddr)
    execute_script()
