#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import template
from django.contrib.auth.models import AnonymousUser
from website.models import Transaction

register = template.Library()

@register.filter
def formatTransactionAction(action):
       if action == 'canceled':
              return 'Transaction annulée'
       actions = dict(Transaction.ACTIONS)
       return actions[action]

@register.filter
def formatTransactionValidate(action):
       actions = dict(Transaction.SPECIAL_ACTIONS_TEXT)
       return actions[action]

@register.filter
def is_pinned(d, user):
       try:
              return d[user]
       except:
              return ""

@register.filter
def cssTransaction(status):
       css_status = {
              'wait_answer':'status-inverse',
              'wait_deal':'status-inverse',
              
              'transport':'status-primary',
              'confirm_delivery':'status-warning',
              'confirm_receive':'status-warning',
              'wait_feedback' : 'status-success',
              'finished' : 'status-success',
              'canceled' : 'status-important',
              }
       return css_status[status]

@register.filter
def truncchar(value, arg):
    if len(value) < arg:
        return value
    else:
        return value[:arg] + '...'
