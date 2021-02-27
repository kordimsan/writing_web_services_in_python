from bs4 import BeautifulSoup
import unittest
import re, os
from pprint import pprint

def parse(path_to_file):    
    with open(path_to_file, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find(id='bodyContent')
    imgs = imgs_count(body)
    headers = headers_count(body)
    linkslen = max_links_len(body)
    lists = lists_count(body)
    return [imgs, headers, linkslen, lists]

def imgs_count(body) -> int:
    return len([w for w in [img.get('width',img.get('data-file-width',0)) for img in body.find_all('img')] if int(w) >= 200])

def headers_count(body) -> int:
    c = 0
    for h in body.find_all(name = re.compile('h\d')):
        if h.span:
            if h.find('span','mw-headline')['id'][0] in ['E', 'T', 'C']:
                c+=1
        else:
            if h.string[0] in ['E', 'T', 'C']:
                c+=1
    return c

def max_links_len(body) -> int:
    mc = 0
    for href in body.find_all('a'):
        sibs = [s.name for s in href.find_next_siblings()]
        for i in range(len(sibs)):
            if sibs[i] == 'a':
                c = i+1
            else:
                break
        if mc < c:
            mc = c + 1
    return mc

def lists_count(body) -> int:
    return len([l for l in body.find_all(name = re.compile('[ou]l')) if (l.parent).name != 'li'])

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                #print(path + [next])
                yield path + [next]
            else:
                queue.append((next, path + [next]))

def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""

    actual_pages = os.listdir(path=path)
    graph = {}
    for p in actual_pages:
        with open(os.path.join(path, p), encoding="utf-8") as file:
            links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())
        graph[p] = set(links) & set(actual_pages) - {p}
    
    try:
        return next(bfs_paths(graph, start_page, end_page))
    except StopIteration:
        return None
    


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    # получаем список страниц, с которых необходимо собрать статистику 
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь
    statistic = {p:parse(path + p) for p in pages}
    return statistic

class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    # result = build_bridge('wiki/', 'The_New_York_Times', 'Stone_Age')
    # print(result)
    # result = get_statistics('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing")
    # pprint(result)
    # print(parse('wiki/Stone_Age'))
    unittest.main()