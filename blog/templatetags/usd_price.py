from beem import Steem
from beem.instance import shared_blockchain_instance
from beem.market import Market
from django import template

register = template.Library()
m = Market()


@register.simple_tag
def usd_price():
    value = m.hive_usd_implied()
    value = float('{0:.2f}'.format(value))
    return value
