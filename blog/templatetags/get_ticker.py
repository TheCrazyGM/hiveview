from beem import Steem
from beem.market import Market
from beem.instance import shared_steem_instance
from django import template
import json
import re
register = template.Library()

shared_steem_instance()
m = Market()

@register.filter(name='lookup')
def lookup(key, value):
    return key[value]

@register.simple_tag
def get_ticker():
    value = m.ticker()
    return {"ticker":dict(value)}