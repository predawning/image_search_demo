# coding=UTF-8

from enum import Enum

class Category(Enum):
    painting_and_calligraphy1 = 152
    painting_and_calligraphy2 = 153
    porcelain_craft = 154
    oil_painting_and_sculpture = 155
    ancient_coin = 156
    collection = 158
    paper_money = 159


categories = [{'id': Category.painting_and_calligraphy1.value, 'name': u'中国书画(一)'},
              {'id': Category.painting_and_calligraphy2.value, 'name': u'中国书画(二)'},
              {'id': Category.porcelain_craft.value, 'name': u'瓷器工艺品'},
              {'id': Category.oil_painting_and_sculpture.value, 'name': u'中国油画雕塑'},
              {'id': Category.ancient_coin.value, 'name': u'机制币,古钱,银锭'},
              {'id': Category.collection.value, 'name': u'邮品,名人签名藏品'},
              {'id': Category.paper_money.value, 'name': u'纸币'}]
