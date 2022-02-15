import requests,os
import asyncio,aiohttp
import time

class Spider(object):
    def __init__(self, query):  # query为搜索的关键字
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) '
                          'Chrome/22.0.1216.0 Safari/537.2',
        }
        self.num = 1
        self.query = query
        if self.query not in os.listdir('.'):
            os.mkdir(self.query)
        self.path = os.path.join(os.path.abspath('.'), self.query)
        os.chdir(self.path)  # 切换到目标目录

    def get_page_info(self, page):
        '''获取json内容'''
        url = 'https://unsplash.com/napi/search/photos'
        data = {
            'page': page,
            'query': self.query,
            'per_page': 20,
            'xp': '',
        }
        response = requests.get(url, params=data)
        if response.status_code == 200:  # 成功返回信息
            return response.json()
        else:
            print('请求失败，状态码为{}'.format(response.status_code))

    async def get_content(self, link):
        '''获取link相应的内容'''
        async with aiohttp.ClientSession() as session:
            response = await session.get(link)
            content = await response.read()
            return content

    async def download_img(self, img):
        '''通过图片下载地址下载图片'''
        content = await self.get_content(img[1])
        with open(img[0] + '.jpg', 'wb') as f:
            f.write(content)
        print('下载第{}张图片成功!'.format(self.num))
        self.num += 1

    def run(self):
        start = time.time()  # 记录起始时间戳
        for i in range(1, 11):
            results = self.get_page_info(i)['results']
            print('hahha ....', results)
            loop = asyncio.get_event_loop()
            tasks = [asyncio.ensure_future(self.download_img((link['id'], link['links']['download']))) for link in
                     results]
            loop.run_until_complete(asyncio.wait(tasks))
        end = time.time()  # 获取结束时间戳
        print('共运行了{}秒'.format(end - start))  # 程序耗时

def main():
    query = input('Please input you want to search keywords: ')
    spider = Spider(query)
    spider.run()

if __name__ == '__main__':
    main()