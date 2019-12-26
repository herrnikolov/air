from lxml import html
import requests

page = requests.get('https://raw.githubusercontent.com/herrnikolov/air/master/air.html')
tree = html.fromstring(page.content)

pm25 = tree.xpath('/html/body/div[2]/table/tbody/tr[3]/td[3]/text()')
print(pm25)

pm10 = tree.xpath('/html/body/div[2]/table/tbody/tr[4]/td[3]/text()')
print(pm10)

temp = tree.xpath('/html/body/div[2]/table/tbody/tr[7]/td[3]/text()')
print(temp)

hu = tree.xpath('/html/body/div[2]/table/tbody/tr[9]/td[3]/text()')
print(hu)