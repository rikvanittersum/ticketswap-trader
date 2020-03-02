import urllib3
from bs4 import BeautifulSoup as soup
from process_soup import Process_soup
from ticket import Ticket
import pymongo
from datetime import datetime
import pytz

client = pymongo.MongoClient(
    "mongodb+srv://rik:Yanntiersen1970!@cluster0-ebw47.mongodb.net/test?retryWrites=true&w=majority")

urls = [
    'https://www.ticketswap.nl/event/awakenings-festival-2020-20th-anniversary/saturday-tickets/2e502d38-2820-47ed-89e5-ba18920932e0/1333459',
    'https://www.ticketswap.nl/event/lowlands-festival-2020/weekend-tickets/03156ec9-7774-4c70-88aa-0716cb30438c/1588534',
    'https://www.ticketswap.nl/event/intents-festival-2020/saturday-tickets/3cc27e0e-3fc7-44f0-9123-99ec30e409a8/1582663',
    'https://www.ticketswap.nl/event/billie-eilish/floor-tickets/595410b6-aa96-4d78-be99-db7c75ca4f66/1455912',
    'https://www.ticketswap.nl/event/down-the-rabbit-hole-2020/weekend-tickets/a3100ea4-3d72-4a36-a174-b0e61b4b2487/1544263',
    'https://www.ticketswap.nl/event/zwarte-cross-2020/campingkaart-incl-festival-entree-do-t-m-zo/5bebf0e9-728e-4bee-9359-0d414a2c9e35/1468098',
    'https://www.ticketswap.nl/event/best-kept-secret-festival-2020/regular/6a9714ff-cddc-43c2-8af9-9a32240c8e7b/1292839',
    'https://www.ticketswap.nl/event/dekmantel-festival-2020/4-day-ticket-tickets/c4b0156a-aa73-4e89-a027-fe679776c746/1573625',
    'https://www.ticketswap.nl/event/dekmantel-festival-2020/saturday-tickets/c4b0156a-aa73-4e89-a027-fe679776c746/1612125',
    'https://www.ticketswap.nl/event/milkshake-festival-2020/saturday-tickets/62dd0220-e662-494a-8794-4a4365a5f5be/1369143',
    'https://www.ticketswap.nl/event/amsterdam-open-air-2020/saturday/47f6597d-264a-45f2-a002-c57f3607a4b6/1580187',
    'https://www.ticketswap.nl/event/loveland-van-oranje-2020-25yrs/regular-tickets/edf26963-c672-48e6-9f75-222e8ab170bb/1596309',
    'https://www.ticketswap.nl/event/lente-kabinet-festival-2020/saturday-tickets/6eb1d25d-97c6-49fb-8e0e-eabea4c222a6/1580350',
    'https://www.ticketswap.nl/event/terug-naar-toen-winter-festival-2020/regular-tickets/60ba3737-7dd5-44f1-ab09-96fbfcb243be/1494429',
    'https://www.ticketswap.nl/event/de-zon-festival-2020/regular-tickets/2db7c8d4-ab32-4d31-9d01-eaf47422cc47/1569523'
    ]

def make_processed_soup(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return Process_soup(soup(response.data, "html.parser"))

tz = pytz.timezone('Europe/Berlin')
now = datetime.now(tz)
dt_string = now.strftime("%d/%m/%Y %H:%M")

for url in urls:
    try:
        processed_soup = make_processed_soup(url)
        ticket = Ticket(processed_soup)
        db = client.get_database(ticket.get_event_name()[:30])
        records = db[ticket.get_ticket()]
        records.insert_one({'time': dt_string, 'for_sale': ticket.get_tickets_for_sale(), 'price': ticket.get_average_sold_price(),
                            'sold': ticket.get_sold_tickets(), 'searched_tickets': ticket.get_searched_tickets()})
    except:
        continue
