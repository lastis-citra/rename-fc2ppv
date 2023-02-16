import os
import re
from bs4 import BeautifulSoup
import cloudscraper


# http://javip.net/ から情報を取り出す
def get_javip_data(fc2_id):
    url = f'http://javip.net/fc2-ppv-{fc2_id}/'
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
    descriptions = soup.select_one('div.entry')
    for description in descriptions.text.splitlines():
        if '販売者' in description:
            print(description)
            return description.replace('販売者 ', '')
    return ''


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

    if keywords != '':
        return keywords.split(",")[0]
    return ''


def rename_dir(path):
    file_name_list = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    # print(file_name_list)

    for file_name in file_name_list:
        print(file_name)
        # すでに変換済みのファイルは除く，undefinedが付いているファイルはもう1回検索する
        if '(By ' not in file_name or UNDEFINED_NAME in file_name:
            # FC2PPVのIDを抜き出す
            fc2_ids = re.findall(r'FC2PPV\s(\d+)\s', file_name)
            if len(fc2_ids) == 1:
                fc2_id = fc2_ids[0]
                print('Searching in FC2...')
                seller = get_fc2_data(fc2_id)
                # FC2で見つからない場合はjavipで探す
                if seller == '':
                    print('Searching in javip...')
                    seller = get_javip_data(fc2_id)
                if seller == '':
                    user = UNDEFINED_NAME
                else:
                    user = f'(By {seller})'
                # undefinedが付いているファイルはその部分を置換する
                if UNDEFINED_NAME in file_name:
                    new_file_name = file_name.replace(f'{UNDEFINED_NAME}', f'{user}')
                else:
                    new_file_name = file_name.replace(f'{fc2_id}', f'{fc2_id} {user}')
                # 禁則処理
                new_file_name = re.sub(r'[\\/:*?"<>|]+', '', new_file_name)
                print(f'Rename to: {new_file_name}')
                os.rename(os.path.join(path, file_name), os.path.join(path, new_file_name))
        else:
            print('Already renamed!!!')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    UNDEFINED_NAME = '(By undefined name!!!)'
    rename_dir(os.environ['RENAME_PATH'])

