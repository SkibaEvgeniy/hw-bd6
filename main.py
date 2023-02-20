import sqlalchemy
from settings import login, password
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
import json

DSN = f"postgresql://{login}:{password}@localhost:5432/hw-bd6"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('data.json', encoding='utf-8') as data:
    data = json.load(data)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


def get_info_buying_books(publisher_name):
    if publisher_name.isnumeric():
        for row in session.query(Book.title, Shop.name, (Sale.count*Sale.price),
                               Sale.date_sale). \
                join(Stock.shop_stock).join(Stock.book_stock).join(Book.publisher). \
                join(Stock.sale_stock).filter(Publisher.id == int(publisher_name)):
            print(row)
    else:
        for row in session.query(Book.title, Shop.name, (Sale.count*Sale.price),
                               Sale.date_sale). \
                join(Stock.shop_stock).join(Stock.book_stock).join(Book.publisher). \
                join(Stock.sale_stock).filter(Publisher.name.like(publisher_name)):
            print(row)

session.close()

if __name__ == '__main__':
    publisher_name = input('Введите имя или id издателя: ')
    get_info_buying_books(publisher_name)
