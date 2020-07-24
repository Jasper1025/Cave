# -*- coding: utf-8 -*-
import urllib.request as req
import csv
import bs4
import requests

def checkformat(root, class_tag, data, index, address):
    
    try:

        content = root.select(class_tag)[index].text

    except:

        content='null'

    return content


#address = "https://www.ptt.cc/bbs/movie/index.html"

#建立一個Request物件, 附加Request Headers 的資訊
#with open("ptt_data.txt", "w", encoding = "utf-8") as file:

c=open("ptt.csv", "w")

writer = csv.writer(c)

writer.writerow(['日期','作者','標題','網址'])

writer_list=[]

for page in range(1):

    address = "https://www.ptt.cc/bbs/movie/index"+str(page)+".html"

    request=req.Request(address, headers={

        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"

    })
    with req.urlopen(request) as response:

        data = response.read().decode("utf-8")

        #解析原始碼, 取得每篇文章的標題

        root=bs4.BeautifulSoup(data, "html.parser")

        articles=root.find_all("div", class_="r-ent")

        for article in articles:

            titles=article.find("div", class_="title") #尋找所有class="title"的div標籤

            date=article.find("div", class_="date") #尋找所有日期

            name=article.find("div", class_="author") #尋找人名

            if titles.a != None:

                print(date.string+"\n")
                writer_list.append(date.string)
                #file.write(date.string+"\n")

                print(name.string+"\n")
                writer_list.append(name.string)
                #file.write(name.string+"\n")
                
                print(titles.a.string+"\n")   #如果標題有a標籤,印出來
                writer_list.append(titles.a.string)
                #file.write(titles.a.string+"\n")

                address2 = "https://www.ptt.cc" + titles.find("a", href=True)['href']
                print(address2+"\n")
                writer_list.append(address2)
                
                #file.write(address2+"\n")
                writer.writerow(writer_list) #寫入ＣＳＶ檔案內
                del writer_list[:]
 
                resp = requests.get(address2) #回傳為一個request.Response的物件
                # #print(resp.status_code)
                # #物件的statu_code屬性取得server回覆的狀態碼(200表示正常,404表示找不到網頁)
                if resp.status_code == 200:
                #     #進入鏈結
                    request2=req.Request(address2, headers={

                        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15"

                    })

                    with req.urlopen(request2) as response2:

                        data2=response2.read().decode("utf-8")


                    root2=bs4.BeautifulSoup(data2, "html.parser")

                #     # #以防網頁不存在

                #     #content 文章內文

                    date = checkformat(root2, '.article-meta-value', 'date', 3, address2)

                    if date=='null':

                        continue

                    content = root2.find(id="main-content").text

                    target_content = u'※ 發信站: 批踢踢實業坊(ptt.cc),'

                #     #去除掉 target_content

                    content = content.split(target_content)

                #    print(content)
            
                    content = content[0].split(date)

                # #     #去除掉文末 --

                    main_content = content[1].replace('--', '')

                #     #印出內文

                    print(main_content+"\n")
                    #file.write(main_content+"\n")

                # #writer.writerow(writer_list)
                # #del writer_list[:]

