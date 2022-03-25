from asyncio import create_task,wait,get_event_loop
from os import makedirs
from aiohttp import ClientSession
from Myhtml import html
from sys import exit


async def main():
    for url_with_page in urls_with_page:
        text = html(url_with_page).get_text(url_with_page)
        title_hrefs = html.parse_domain(text)
        tasks = []
        async with ClientSession() as session:
            for title_href in title_hrefs:
                title = title_href[0]
                makedirs(f'D://绝对领域//{title}', exist_ok=True)
                href = title_href[-1]
                # 图片url生成器
                imgs = domain.episode_parse(url=href)
                for img in imgs:
                    img_url = img.attr('src')
                    tasks.append(create_task(html().one_download(session, img_url, title)))
            await wait(tasks)


if __name__ == '__main__':
    try:
        makedirs('D://绝对领域', exist_ok=True)
        domain_url = 'https://juedly.com/dbyf'
        # 实例化一个html对象
        domain = html(domain_url)
        # 取得主页的源代码
        domain_text = domain.get_text(domain_url)
        # ('愿望是能让自己每天开心', 'https://juedly.com/1891.html')
        urls_with_page = domain.add_page_arg()
        # 创建实践循环
        loop = get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        exit(0)
    finally:
        html().remove_folders()
