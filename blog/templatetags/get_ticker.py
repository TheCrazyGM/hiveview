from beem.market import Market
from beem.instance import shared_blockchain_instance
from django import template
import json
import re
register = template.Library()

m = Market()

@register.filter(name='lookup')
def lookup(key, value):
    return key[value]

@register.simple_tag
def get_ticker():
    value = m.ticker()
    return {"ticker":dict(value)}
