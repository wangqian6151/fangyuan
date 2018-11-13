# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class AnjukeTwoItem(Item):
    collection = table = 'AnjukeTwo'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    community = Field()
    img = Field()
    area = Field()
    layout = Field()
    build_year = Field()
    floor = Field()
    district = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class AnjukeShoprentalItem(Item):
    collection = table = 'AnjukeShoprental'

    title = Field()
    url = Field()
    price = Field()
    img = Field()
    area = Field()
    floor = Field()
    type = Field()
    community = Field()
    district = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class AnjukeShopsaleItem(Item):
    collection = table = 'AnjukeShopsale'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    img = Field()
    area = Field()
    floor = Field()
    type = Field()
    community = Field()
    district = Field()
    location = Field()
    address = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class AnjukeNewItem(Item):
    collection = table = 'AnjukeNew'

    title = Field()
    url = Field()
    no_price = Field()
    price = Field()
    img = Field()
    area = Field()
    layout = Field()
    district = Field()
    location = Field()
    address = Field()
    phone = Field()
    comment = Field()
    status = Field()
    type = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class FangtianxiaTwoItem(Item):
    collection = table = 'FangtianxiaTwo'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    community = Field()
    img = Field()
    area = Field()
    layout = Field()
    orientation = Field()
    floor = Field()
    build_year = Field()
    location = Field()
    address = Field()
    distance = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class FangtianxiaShoprentalItem(Item):
    collection = table = 'FangtianxiaShoprental'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    img = Field()
    area = Field()
    community = Field()
    address = Field()
    type = Field()
    floor = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class FangtianxiaShopsaleItem(Item):
    collection = table = 'FangtianxiaShopsale'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    img = Field()
    area = Field()
    community = Field()
    address = Field()
    type = Field()
    floor = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class LianjiaTwoItem(Item):
    collection = table = 'LianjiaTwo'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    community = Field()
    img = Field()
    area = Field()
    layout = Field()
    orientation = Field()
    decoration = Field()
    elevator = Field()
    floor = Field()
    location = Field()
    focus_num = Field()
    watch_num = Field()
    pubdate = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class LianjiaNewItem(Item):
    collection = table = 'LianjiaNew'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    img = Field()
    location = Field()
    community = Field()
    address = Field()
    area = Field()
    type = Field()
    status = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class QfangTwoItem(Item):
    collection = table = 'QfangTwo'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    img = Field()
    layout = Field()
    area = Field()
    decoration = Field()
    floor = Field()
    orientation = Field()
    build_year = Field()
    district = Field()
    location = Field()
    community = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class QfangNewItem(Item):
    collection = table = 'QfangNew'

    title = Field()
    alias = Field()
    url = Field()
    unit_price = Field()
    total_price = Field()
    img = Field()
    area = Field()
    layout = Field()
    district = Field()
    location = Field()
    address = Field()
    phone = Field()
    status = Field()
    type = Field()
    decoration = Field()
    time = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    number = Field()


class TongchengTwoItem(Item):
    collection = table = 'TongchengTwo'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    community = Field()
    img = Field()
    area = Field()
    layout = Field()
    orientation = Field()
    floor = Field()
    district = Field()
    location = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    time = Field()
    number = Field()


class TongchengShoprentalItem(Item):
    collection = table = 'TongchengShoprental'

    title = Field()
    url = Field()
    month_price = Field()
    day_price = Field()
    img = Field()
    area = Field()
    type = Field()
    status = Field()
    district = Field()
    location = Field()
    address = Field()
    tags = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    # time = Field()
    number = Field()


class TongchengShopsaleItem(Item):
    collection = table = 'TongchengShopsale'

    title = Field()
    url = Field()
    total_price = Field()
    unit_price = Field()
    img = Field()
    area = Field()
    type = Field()
    status = Field()
    district = Field()
    location = Field()
    address = Field()
    tags = Field()
    lat = Field()
    lng = Field()
    precise = Field()
    confidence = Field()
    # time = Field()
    number = Field()


class GanjiShoprentalItem(Item):
    collection = table = 'GanjiShoprental'

    title = Field()
    url = Field()
    month_price = Field()
    day_price = Field()
    img = Field()
    area = Field()
    floor = Field()
    type = Field()
    district = Field()
    location = Field()
    address = Field()
    transfer = Field()
    status = Field()
    industry = Field()

    payment = Field()
    width = Field()
    lease = Field()
    depth = Field()
    height = Field()
    street = Field()
    total_floor = Field()
    shop_type = Field()

    lat = Field()
    lng = Field()
    # precise = Field()
    # confidence = Field()
    number = Field()


class GanjiShopsaleItem(Item):
    collection = table = 'GanjiShopsale'

    title = Field()
    url = Field()
    total_price = Field()
    uint_price = Field()
    img = Field()
    area = Field()
    floor = Field()
    type = Field()
    district = Field()
    location = Field()
    address = Field()
    tags = Field()
    status = Field()
    industry = Field()

    width = Field()
    depth = Field()
    height = Field()
    sale = Field()
    street = Field()
    total_floor = Field()

    lat = Field()
    lng = Field()
    # precise = Field()
    # confidence = Field()
    number = Field()
