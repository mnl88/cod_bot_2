"""
Парсер с сайта https://cod.tracker.gg/
"""

import requests
import logging
import concurrent.futures

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from random import shuffle


logger = logging.getLogger(__name__)

HOST = 'https://cod.tracker.gg/'
URL_MP_START = 'modern-warfare/profile/atvi/'
URL_MP_FINISH = '/mp'
URL_WZ_START = 'warzone/profile/atvi/'
URL_WZ_FINISH = '/overview'

URL_WITH_PROXIES = 'https://free-proxy-list.net/'

working_proxies_list = []
working_proxies_list_3 = []
responses = []


# получаем список ЭЛИТНЫХ =) проксей с сайта https://free-proxy-list.net/
def get_proxies():
    logger.info(f'Парсим прокси с сайта https://free-proxy-list.net/')
    r = requests.get(URL_WITH_PROXIES)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text == 'elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    logger.info(f'Кол-во полученных проксей = {len(proxies)}')
    return proxies


def fetching(url, proxy, game_type):
    user_agent = UserAgent()
    current_ua = user_agent.random
    try:
        response = requests.get(
            url=url,
            headers={'User-Agent': current_ua},
            proxies={'http': proxy, 'https': proxy},
            timeout=2)
        if response.status_code == 200:
            responses.append([game_type, response])
            logger.info(f'Статистика по {str(game_type).upper()} получена')
    except:
        pass


def game_types_and_urls(
        activision_account=None, psn_account=None, blizzard_account=None, xbox_account=None, platform_type=None
) -> dict:
    """парсер. возвращает словарь вида: warzone - plumber - kills - 10"""

    url_host = 'https://cod.tracker.gg/'

    if platform_type == 2 and psn_account is not None:
        url_profile_type_part = 'psn/'
        url_account_name_part = psn_account
        # 'https://cod.tracker.gg/warzone/profile/psn/manile_88/overview'

    elif platform_type == 1 and blizzard_account is not None:
        url_profile_type_part = 'battlenet/'
        url_account_name_part = blizzard_account.replace('#', '%23')
        # 'https://cod.tracker.gg/warzone/profile/battlenet/Manile%2321212/overview'

    elif platform_type == 3 and xbox_account is not None:
        url_profile_type_part = 'xbl/'
        url_account_name_part = xbox_account.replace(' ', '%20')
        # 'https://cod.tracker.gg/warzone/profile/xbl/UNKNOWN%206989/overview'

    elif activision_account is not None:
        # 'https://cod.tracker.gg/warzone/profile/atvi/npopok%236351930/overview'
        url_profile_type_part = 'atvi/'
        url_account_name_part = activision_account.replace('#', '%23')

    else:
        logger.error('Account Activision или сочитание платформа + аккаунт к этой платформе не обнаружены')
        return {'warzone': None, 'modern-warfare': None, 'cold-war': None}

    return {
        'warzone': url_host + 'warzone/profile/' + url_profile_type_part + url_account_name_part + "/overview",
        'modern-warfare': url_host + 'modern-warfare/profile/' + url_profile_type_part + url_account_name_part,
        'cold-war': url_host + 'cold-war/profile/' + url_profile_type_part + url_account_name_part
    }


def get_dict_from_response(response_fetch) -> dict:
    """Вернем список труб"""

    soup = BeautifulSoup(response_fetch, 'lxml')  # превращаем в суп
    stat_dict = {}
    try:
        items = soup.find('div', class_='trn-grid').find_all('div', class_='segment-stats card bordered responsive')
        for item in items:
            header = item.find('h2').get_text()
            stat_dict[header] = {}
            cells = item.find_all('div', class_='numbers')
            for cell in cells:
                title = cell.find('span', class_="name").get('title')
                if cell.find('span', class_="value") is not None:
                    value = cell.find('span', class_="value").get_text()
                else:
                    value = None
                if stat_dict[header].setdefault(title) is None:
                    stat_dict[header][title] = value
    except:
        pass
    return stat_dict


def get_kd(full_statistic: dict):
    kd_ratio = {}
    try:
        kd_ratio['warzone'] = full_statistic.setdefault('warzone').setdefault('Battle Royale').setdefault('K/D Ratio')
    except Exception as ex:
        kd_ratio['warzone'] = None
    try:
        kd_ratio['modern-warfare'] = full_statistic.setdefault('modern-warfare').setdefault(
            'Lifetime Overview').setdefault('K/D Ratio')
    except Exception as ex:
        kd_ratio['modern-warfare'] = None
    try:
        kd_ratio['cold-war'] = full_statistic.setdefault('cold-war').setdefault('Lifetime Overview').setdefault(
            'K/D Ratio')
    except Exception as ex:
        kd_ratio['cold-war'] = None
    return kd_ratio


def show_statistics(full_statistic: dict):
    for game, game_type in full_statistic.items():
        print('\n', game)
        for stat, value in game_type.items():
            print('\n', stat)
            for s, v in value.items():
                print(s, ': ', v)


def get_statistics(
        activision_account=None,
        psn_account=None,
        blizzard_account=None,
        xbox_account=None,
        platform_type=None
) -> dict:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%d.%m.%y %H:%M:%S')

    types_and_urls = game_types_and_urls(
        activision_account=activision_account,
        psn_account=psn_account,
        blizzard_account=blizzard_account,
        xbox_account=xbox_account,
        platform_type=platform_type
    )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for proxy in get_proxies()[:100]:
            futures.append(executor.submit(
                fetching, proxy=proxy, url=types_and_urls['warzone'], game_type='warzone'))
            futures.append(executor.submit(
                fetching, proxy=proxy, url=types_and_urls['modern-warfare'], game_type='modern-warfare'))
            futures.append(executor.submit(
                fetching, proxy=proxy, url=types_and_urls['cold-war'], game_type='cold-war'))

    full_statistic = {
        'warzone': None,
        'modern-warfare': None,
        'cold-war': None
    }

    for response in responses:
        if response[0] == 'warzone':
            full_statistic['warzone'] = get_dict_from_response(response[1].content)
        if response[0] == 'modern-warfare':
            full_statistic['modern-warfare'] = get_dict_from_response(response[1].content)
        if response[0] == 'cold-war':
            full_statistic['cold-war'] = get_dict_from_response(response[1].content)

    return full_statistic


def main():
    data = get_statistics(activision_account='DRONORD#9501196')
    kd = get_kd(data)
    print(kd)


if __name__ == '__main__':
    main()
