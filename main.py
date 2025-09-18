import os
import re
from bs4 import BeautifulSoup
import cloudscraper


# https://javip.net/ から情報を取り出す
def get_javip_data(fc2_id):
    url = f'https://javip.net/fc2-ppv-{fc2_id}'
    # print(f'javip_url: {url} ', end='')
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
    contents = soup.select_one('div[class="entry"]')
    for content in contents.text.splitlines():
        if '販売者' in content:
            # print(content)
            return content.replace('販売者 ', '')
    return ''


# https://www.jav380.com/ から情報を取り出す
def get_jav380_data(fc2_id):
    url = f'https://www.jav380.com/?s=FC2+PPV+{fc2_id}'
    # print(f'jav380_url: {url} ', end='')
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
    a_tags = soup.select('a[class="more-link"]')
    if len(a_tags) > 0:
        content_url = a_tags[-1]["href"]
        res = scraper.get(content_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        contents = soup.select_one('div[class="post-content"]')
        for content in contents.text.splitlines():
            if '販売者' in content:
                # print(content)
                return content.replace('販売者 ', '')
    return ''


# https://fc2cm.com/ から情報を取り出す
def get_fc2cm_data(fc2_id):
    url = f'https://fc2cm.com/?p={fc2_id}'
    # print(f'fc2cm_url: {url} ', end='')
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
    a_tags = soup.select('a[rel="category"]')
    if len(a_tags) == 1:
        return a_tags[0].text
    return ''


# http://javip.net/ から情報を取り出す
def get_javip_data(fc2_id):
    url = f'http://javip.net/fc2-ppv-{fc2_id}/'
    # print(f'javip_url: {url} ', end='')
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
            # print(description)
            return description.replace('販売者 ', '').replace('販売者', '')
    return ''


# FC2のHPから情報を取り出す
def get_fc2_data(fc2_id):
    url = f'https://ads.contents.fc2.com/article/{fc2_id}/'
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
    try:
        keywords = soup.select_one('meta[name="keywords"]')['content']
    except TypeError as e:
        return ''
    keywords = keywords.split(',Videos')[0]

    if keywords != '':
        return keywords.split(",")[0]
    return ''


def duplicate_rename(file_path):
    if os.path.exists(file_path):
        name, ext = os.path.splitext(file_path)
        i = 1
        while True:
            # 数値を3桁などにしたい場合は({:0=3})とする
            new_name = "{} ({}){}".format(name, i, ext)
            if not os.path.exists(new_name):
                return new_name
            i += 1
    else:
        return file_path


def rename_dir(path):
    print(f'Loading... ')
    file_names = os.listdir(path)
    print(f'Sorting... ')
    file_names = sorted(file_names)

    new_file_names = []
    for file_name in file_names:
        if 'FC2 PPV' in file_name:
            new_file_name = file_name.replace('FC2 PPV', 'FC2PPV')
            new_file_path = os.path.join(path, new_file_name)
            try:
                os.rename(os.path.join(path, file_name), os.path.join(new_file_path))
            except OSError:
                print(f'OSError')
            new_file_names.append(new_file_name)
        elif 'FC2PPV-' in file_name:
            new_file_name = file_name.replace('FC2PPV-', 'FC2PPV ')
            new_file_path = os.path.join(path, new_file_name)
            try:
                os.rename(os.path.join(path, file_name), os.path.join(new_file_path))
            except OSError:
                print(f'OSError')
            new_file_names.append(new_file_name)
        elif 'FC2-PPV-' in file_name:
            new_file_name = file_name.replace('FC2-PPV-', 'FC2PPV ')
            new_file_path = os.path.join(path, new_file_name)
            try:
                os.rename(os.path.join(path, file_name), os.path.join(new_file_path))
            except OSError:
                print(f'OSError')
            new_file_names.append(new_file_name)
        else:
            new_file_names.append(file_name)

    count = len(file_names)
    i = 1
    for file_name in new_file_names:
        print(f'Renaming... {i}/{count} {file_name}')
        # すでに変換済みのファイルは除く，undefinedが付いているファイルはもう1回検索する
        if ('(By ' not in file_name or UNDEFINED_NAME in file_name) and os.path.isfile(os.path.join(path, file_name)):
            # FC2PPVのIDを抜き出す
            fc2_ids = re.findall(r'FC2PPV\s(\d+)\s', file_name)
            if len(fc2_ids) == 1:
                fc2_id = fc2_ids[0]
                print('Searching in FC2...')
                seller = get_fc2_data(fc2_id)
                # FC2で見つからない場合はjavipで探す
                # if seller == '':
                #     print('Searching in javip...')
                #     seller = get_javip_data(fc2_id)
                # javipで見つからない場合はfc2cmで探す
                if seller == '':
                    print('Searching in fc2cm...')
                    seller = get_fc2cm_data(fc2_id)
                if seller == '':
                    user = UNDEFINED_NAME
                # fc2cmで見つからない場合はjav380で探す
                if seller == '':
                    print('Searching in jav380...')
                    seller = get_jav380_data(fc2_id)
                # fc2cmで見つからない場合はjavipで探す
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
                # 拡張子とそれ以外に分割
                ext = os.path.splitext(new_file_name)[1]
                base_name = os.path.splitext(new_file_name)[0]
                if len(base_name) > MAX_LENGTH:
                    base_name = [base_name[x:x + MAX_LENGTH] for x in range(0, len(base_name), MAX_LENGTH)][0]
                # 禁則処理
                base_name = re.sub(r'[\\/:*?"<>|]+', '', base_name)
                # 同名ファイルがある場合かつ自分自身でない場合は連番にする
                new_file_path = os.path.join(path, base_name + ext)
                if os.path.join(path, file_name) != new_file_path:
                    new_file_path = duplicate_rename(os.path.join(path, base_name + ext))
                print(f'Rename to: {new_file_path}')
                try:
                    os.rename(os.path.join(path, file_name), os.path.join(new_file_path))
                except OSError:
                    print(f'OSError')
        else:
            print('Already renamed!!!')
        i += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    UNDEFINED_NAME = '(By undefined name!!!)'
    MAX_LENGTH = int(os.getenv('MAX_LENGTH', '10000'))
    rename_dir(os.getenv('RENAME_PATH'))
