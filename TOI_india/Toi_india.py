from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://timesofindia.indiatimes.com/india').text
soup = BeautifulSoup(html_text, "lxml")
links = soup.find_all("span", class_="w_tle")
for link in links:
    site_link = link.a["href"]
    if site_link.split("/")[0] == "" and site_link.split("/")[1] == "india" and not link.a.i:
        full_link = f"https://timesofindia.indiatimes.com/{site_link}"
        another_html_req = requests.get(f'{full_link}').text
        another_soup = BeautifulSoup(another_html_req, "lxml")
        content = another_soup.find("div", class_="_2NFXP")
        title = content.h1.text
        date_and_time = content.find("div", class_="_3Mkg- byline").text.split("|")
        if (len(date_and_time) == 1):
            date_and_time = content.find("div", class_="_3Mkg- byline").text
        else:
            date_and_time = date_and_time[len(date_and_time)-1]
        dnt = date_and_time.split(":")
        if(dnt[0] == " Updated"):
            date_and_time = dnt[1] + dnt[2]
        para_content = another_soup.find("div", class_="ga-headlines").text.split(".")
        edited_para_content = '.\n'.join(para_content)
        edited_para_content = edited_para_content.replace("â","'")
        with open("india.txt", "a") as file:
            file.write(f"\nTITLE:\n{title}\n\nLINK:\n{full_link}\n\nDATE&TIME:\n{date_and_time}\n\nTEXT:\n{edited_para_content}\n\n")