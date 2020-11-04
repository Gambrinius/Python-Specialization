from bs4 import BeautifulSoup
from decimal import Decimal, ROUND_UP


def convert(amount, cur_from, cur_to, date, requests):
    url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
    response = requests.get(url)  # Использовать переданный requests
    soup = BeautifulSoup(response.content, 'xml')

    if cur_from != 'RUR':
        cur_from_tag = soup.find(name='CharCode', text=cur_from)
        value_from = Decimal(cur_from_tag.find_next_sibling('Value').string.replace(',', '.'))
        nominal_from = Decimal(cur_from_tag.find_next_sibling('Nominal').string)
    else:
        value_from, nominal_from = Decimal(1.0), Decimal(1.0)

    if cur_to != 'RUR':
        cur_to_tag = soup.find(name='CharCode', text=cur_to)
        value_to = Decimal(cur_to_tag.find_next_sibling(name='Value').text.replace(',', '.'))
        nominal_to = Decimal(cur_to_tag.find_next_sibling(name='Nominal').text)
    else:
        value_to, nominal_to = Decimal(1.0), Decimal(1.0)

    # не забыть про округление до 4х знаков после запятой
    result = (amount * value_from / nominal_from * nominal_to / value_to).quantize(Decimal('.0001'), rounding=ROUND_UP)

    return result
