import requests
from lxml import etree
# url ='https://www.dytt8.net/html/gndy/dyzz/list_23_1.html'
base_domain = 'https://www.dytt8.net'#基本域
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Referer':'https://www.dytt8.net/html/gndy/dyzz/list_23_2.html'
}
#定义获得详情url
def get_detail_urls(url):
    response = requests.get(url, headers=headers)
    text = response.text
    html = etree.HTML(text)
    detail_urls = html.xpath('//table[@class="tbspan"]//a/@href')
    #detail详情
    detail_urls = list(map(lambda url:base_domain+url,detail_urls))
    return detail_urls
def parse_detail_url(detail_url):
    def parse_info(info, rule):
        return info.replace(rule, '').strip()  # replace(）第一个参数是被替代的第二个是替代后的，strip可以消除字符串前后空格
    movie = {}
    response = requests.get(detail_url, headers=headers)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath('//div[@class ="title_all"]//font/text()')[0]#返回的是一个列表#tostring()输出修正后的HTML代码，结果为byte类型，用decode可以将其转化成str类型
    movie['tilte'] = title
    cover = html.xpath('//div[@id="Zoom"]//img/@src')[0]
    movie['cover']=cover
    infos =  html.xpath('//div[@id="Zoom"]//p[1]/text()')
    for index,info in enumerate(infos):#enumerate遍历infos，返回两个值index下标，和info
        if info.startswith('◎年　　代'):
            info = parse_info(info,'◎年　　代　')
            movie['age'] = info
        elif info.startswith('◎主　　演'):
             info = parse_info(info,'◎主　　演')
             actors =[info]
             for x in range(index+1,len(infos)):
                 actor = infos[x].strip()
                 if actor.startswith('◎'):
                     break
                 actors.append(actor)

             movie['actor'] = actors

    return movie
    # for x in title:
    #     print(etree.tostring(x,encoding = 'utf-8').decode('utf-8'))
    # Zooms = html.xpath('//div[@id="Zoom"]')
    # infos = Zooms.xpath('//')
    # print( Zooms)
def spider():
    movies = []
    base_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    for x in range(1, 8):
        url = base_url.format(x)
        detail_urls = get_detail_urls(url)
        print(x)
        for detail_url in detail_urls:
             movie = parse_detail_url(detail_url)
             movies.append(movie)
        for movie in movies:
            print(movie)
        break
if __name__=='__main__':
    spider()


