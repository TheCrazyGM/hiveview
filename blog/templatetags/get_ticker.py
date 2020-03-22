from bhive.market import Market
from bhive.instance import shared_hive_instance
from django import template
import json
import re
register = template.Library()

shared_hive_instance()
m = Market()

@register.filter(name='lookup')
def lookup(key, value):
    return key[value]

@register.simple_tag
def get_ticker():
    value = m.ticker()
    return {"ticker":dict(value)}
