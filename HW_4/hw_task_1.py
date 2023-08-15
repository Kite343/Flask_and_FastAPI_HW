# � Написать программу, которая скачивает изображения с заданных URL-адресов и
# сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
# файле, название которого соответствует названию изображения в URL-адресе.
# � Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
# image1.jpg
# � Программа должна использовать многопоточный, многопроцессорный и
# асинхронный подходы.
# � Программа должна иметь возможность задавать список URL-адресов через
# аргументы командной строки.
# � Программа должна выводить в консоль информацию о времени скачивания
# каждого изображения и общем времени выполнения программы.

import requests
import threading
import os
import time
from sys import argv

# urls = ['https://i01.fotocdn.net/s105/f3b0ce5482763fd2/public_pin_l/2239418211.jpg',
#         'https://shutok.ru/uploads/posts/2021-05/1621766945_shutok.ru.1621329408154464102.jpg',
#         'https://i.pinimg.com/736x/34/2f/0d/342f0def20208a9c5b23afabdd5ad698.jpg',
#         'https://pbs.twimg.com/media/EHU_rf8W4AAKDib.jpg',
#         'https://demotivatorium.ru/sstorage/3/2016/03/05142413921376/demotivatorium_ru_vizitka_programmista_108967.jpg',
#         'https://fikiwiki.com/uploads/posts/2022-02/thumbs/1644723021_8-fikiwiki-com-p-kartinki-vi-prinyati-9.jpg',
#         'https://i.pinimg.com/originals/61/3e/0a/613e0a862c7c5239942e6f991679713b.jpg',
#         'https://bugaga.ru/uploads/posts/2014-04/1398276250_komiksy-novinki-10.jpg',
#         'https://zasmeshi.ru/data/photo/big/10865-programmisty-pokinuli-logovo.jpg',
#         ]

def download(url, start_time):
    response = requests.get(url)
    dir_name = 'images'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    filename = dir_name + '/' + url.split("/")[-1]
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded {url} in {time.time()-start_time:.2f} seconds")

def main(urls):    
    threads = []
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=download, args=[url, start_time])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

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
    main(urls)

    # через коммандную строку
    # main(argv[1:])
    # python hw_task_1.py https://i01.fotocdn.net/s105/f3b0ce5482763fd2/public_pin_l/2239418211.jpg https://shutok.ru/uploads/posts/2021-05/1621766945_shutok.ru.1621329408154464102.jpg https://i.pinimg.com/736x/34/2f/0d/342f0def20208a9c5b23afabdd5ad698.jpg https://pbs.twimg.com/media/EHU_rf8W4AAKDib.jpg