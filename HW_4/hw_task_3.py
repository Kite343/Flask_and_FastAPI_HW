import os
import sys
import time
import asyncio
import aiofiles
import aiohttp


async def download(url, start_time):
    dir_name = 'images'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()

        filename = os.path.join(dir_name, url.split("/")[-1])
        async with aiofiles.open(filename, 'wb') as f:
            await f.write(content)

    print(f"Downloaded {url} in {time.time()-start_time:.2f} seconds")



async def main(urls):
    start_time = time.time()

    tasks = []
    for url in urls:
        task = asyncio.create_task(download(url, start_time))
        tasks.append(task)
    # запустить одновременно все задачи из tasks
    await asyncio.gather(*tasks)

    print(f"Downloaded in {time.time()-start_time:.2f} seconds")


if __name__ == "__main__":
    urls = ['https://i01.fotocdn.net/s105/f3b0ce5482763fd2/public_pin_l/2239418211.jpg',
        'https://shutok.ru/uploads/posts/2021-05/1621766945_shutok.ru.1621329408154464102.jpg',
        'https://i.pinimg.com/736x/34/2f/0d/342f0def20208a9c5b23afabdd5ad698.jpg',
        'https://pbs.twimg.com/media/EHU_rf8W4AAKDib.jpg',
        'https://demotivatorium.ru/sstorage/3/2016/03/05142413921376/demotivatorium_ru_vizitka_programmista_108967.jpg',
        'https://fikiwiki.com/uploads/posts/2022-02/thumbs/1644723021_8-fikiwiki-com-p-kartinki-vi-prinyati-9.jpg',
        'https://i.pinimg.com/originals/61/3e/0a/613e0a862c7c5239942e6f991679713b.jpg',
        'https://bugaga.ru/uploads/posts/2014-04/1398276250_komiksy-novinki-10.jpg',
        'https://zasmeshi.ru/data/photo/big/10865-programmisty-pokinuli-logovo.jpg',
        ]
    
    asyncio.run(main(urls))

    # # цикл событий загружаем в loop
    # loop = asyncio.get_event_loop()
    # # запустить корутину main до её завершения
    # loop.run_until_complete(main(urls))

    # через коммандную строку
    # asyncio.run(main(sys.argv[1:]))
    # python hw_task_3.py https://i01.fotocdn.net/s105/f3b0ce5482763fd2/public_pin_l/2239418211.jpg https://shutok.ru/uploads/posts/2021-05/1621766945_shutok.ru.1621329408154464102.jpg https://i.pinimg.com/736x/34/2f/0d/342f0def20208a9c5b23afabdd5ad698.jpg https://pbs.twimg.com/media/EHU_rf8W4AAKDib.jpg