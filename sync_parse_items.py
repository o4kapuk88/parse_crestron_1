import json
import requests
from bs4 import BeautifulSoup
import fake_useragent


def save_to_json(data, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write(',\n')


def get_html(url):
    ua = fake_useragent.UserAgent()
    headers = {'User-Agent': ua.random}
    r = requests.get(url, headers=headers, verify=True)
    return r.text, r.url


def get_items(url):
    html, final_url = get_html(url)
    if final_url != url:
        print(f"Redirected to: {final_url}")
        with open('failed_url.txt', 'a', encoding='utf-8') as f:
            f.write(f"{url}\n")
        return None
    soup = BeautifulSoup(html, 'lxml')
    rubicator_elements = [_.text.strip() for _ in soup.select('div.column.medium-13.elips.align-middle > a')]
    title = soup.select_one('p.model-name').text.strip()
    title_wrapper = soup.select_one('p.model-title').text.strip()
    description_wrapper = soup.select_one(
        'div.model-short-description > p').text.strip() if soup.select_one(
        'div.model-short-description > p') else soup.select_one(
        'div.model-short-description').text.strip()
    tables = soup.select('div#panel2 table')

    data = {
        'url': url,
        'title': title,
        'rubicator': ' | '.join(rubicator_elements),
        'title_wrapper': title_wrapper,
        'description_wrapper': description_wrapper,
        'specification': [],
    }
    key = None
    for table in tables:
        for row in table.find_all('tr'):

            collumns = row.find_all('td')

            num_collumns = len(collumns)
            specification = {}
            if num_collumns == 1:
                if key is not None and 'productSpecTDHead' not in collumns[0].attrs.get('class', []):
                    specification[key] = collumns[0].text.strip()
                    key = None
                else:

                    key = collumns[0].text.strip()
            elif num_collumns == 1 and key is not None:
                specification[key] = collumns[0].text.strip()
                key = None

            elif num_collumns == 2:
                specification[collumns[0].text.strip()] = collumns[1].text.strip()

            elif num_collumns == 3:
                specification[collumns[1].text.strip()] = collumns[2].text.strip()

            data['specification'].append(specification)

    data['specification'] = [spec for spec in data['specification'] if spec]
    return data


if __name__ == '__main__':
    with open('links_items.txt', 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            print(url)
            data = get_items(url)
            if data:
                save_to_json(data, 'test_test.json')
