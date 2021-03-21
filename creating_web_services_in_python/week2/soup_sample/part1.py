from bs4 import BeautifulSoup
import unittest


def parse(path_to_file):
    imgs, headers, linkslen, lists = 0, 0, 0, 0
    with open(path_to_file, encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find(name='div', attrs={'id': 'bodyContent'})

    imgs = len([i for i in body.find_all('img', {'width': True}) if int(i['width']) >= 200])

    headers = len([h for h in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if h.text[0] in 'ETC'])

    for tag in body('a'):
        max_len = 1
        for tag in tag.find_next_siblings():
            if tag.name == 'a':
                max_len += 1
            else:
                break
        linkslen = max(max_len, linkslen)

    lists = len([list_ for list_ in body.find_all(['ul', 'ol']) if not list_.find_parents(['ul', 'ol'])])

    return [imgs, headers, linkslen, lists]


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
    unittest.main()
