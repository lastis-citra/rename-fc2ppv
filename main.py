import os
import re
from bs4 import BeautifulSoup
import cloudscraper


# FC2のHPから情報を取り出す
def get_fc2_data(fc2_id):
    url = f'https://adult.contents.fc2.com/article/{fc2_id}/'
    # print(f'fc2_url: {url} ', end='')
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    res = scraper.get(url)
    # res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.content, 'html.parser')
    description = soup.select_one('meta[name="description"]')['content']
    # 特に古いIDだと製品ページにたどり着けないため
    if 'Unable' in description:
        return ''
    keywords = soup.select_one('meta[name="keywords"]')['content']
    keywords = keywords.split(',Videos')[0]

    # print(keywords)
    return keywords


def rename_dir(path):
    file_name_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # print(file_name_list)

    for file_name in file_name_list:
        print(file_name)
        # すでに変換済みのファイルは除く
        if '(By ' not in file_name:
            # FC2PPVのIDを抜き出す
            fc2_ids = re.findall(r'FC2PPV\s(\d+)\s', file_name)
            if len(fc2_ids) == 1:
                fc2_id = fc2_ids[0]
                keywords = get_fc2_data(fc2_id)
                if keywords != '':
                    user = ' (By ' + keywords.split(',')[0] + ') '
                else:
                    user = ' (By undefined name!!!) '
                new_file_name = file_name.replace(f'{fc2_id}', f'{fc2_id}{user}')
                # 禁則処理
                new_file_name = re.sub(r'[\\/:*?"<>|]+', '', new_file_name)
                print(f'Rename to: {new_file_name}')
                os.rename(os.path.join(path, file_name), os.path.join(path, new_file_name))
        else:
            print('Already renamed!!!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rename_dir(os.environ['RENAME_PATH'])

