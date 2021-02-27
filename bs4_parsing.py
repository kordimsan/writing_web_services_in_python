from bs4 import BeautifulSoup
import unittest
import re, os
from pprint import pprint

def parse(path_to_file):    
    with open(path_to_file, encoding="utf-8") as file:
        soup = BeautifulSoup(file, "lxml")
        body = soup.find(id="bodyContent")
    imgs = imgs_count(body)
    headers = headers_count(body)
    linkslen = max_links_len(body)
    lists = lists_count(body)
    return [imgs, headers, linkslen, lists]

def imgs_count(body) -> int:
    return len(body.find_all('img', width=lambda x: int(x or 0) > 199))

def headers_count(body) -> int:
    return sum(1 for tag in body.find_all(name = re.compile('h\d')) if tag.get_text()[0] in "ETC")

def max_links_len(body) -> int:
    mc = 0
    for href in body.find_all('a'):
        c = 1
        for tag in href.find_next_siblings():
            if tag.name == 'a':
                c += 1
            else:
                break

        mc = c if c > mc else mc
    return mc

def lists_count(body) -> int:
    return len([l for l in body.find_all(name = re.compile('[ou]l')) if not l.find_parent('li')])


class Bridge:
    def __init__(self, path) -> None:
        actual_pages = os.listdir(path=path)
        self.graph = {}
        for p in actual_pages:
            with open(os.path.join(path, p), encoding="utf-8") as file:
                links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())
            self.graph[p] = set(links) & set(actual_pages) - {p}
        
    def bfs_paths(self, graph, start, goal):
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

    bridge = Bridge(path)
    
    try:
        return next(bridge.bfs_paths(bridge.graph, start_page, end_page))
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
    # result = get_statistics('wiki/', 'The_New_York_Times', 'Stone_Age')
    # pprint(result)
    # result = get_statistics('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing")
    # pprint(result)
    # print(parse('wiki/Stone_Age'))
    unittest.main()