from bhive import Hive
from bhive.instance import shared_hive_instance
from bhive.market import Market
from django import template

register = template.Library()
shared_hive_instance()
m = Market()


@register.simple_tag
def usd_price():
    value = m.steem_usd_implied()
    value = float('{0:.2f}'.format(value))
    return value
