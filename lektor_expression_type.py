# -*- coding: utf-8 -*-
"""Add jinja-evaluated types to lektor.
"""
import jinja2
from lektor.environment import (
    Expression,
    FormatExpression,
    )
from lektor.pluginsystem import Plugin
from lektor.types import Type


class ExpressionDescriptor(object):
    def __init__(self, pad, expr):
        self.pad = pad
        self.expr = expr

    def __get__(self, obj, type_=None):
        if obj is None:
            return self
        return self.expr.evaluate(self.pad, this=obj, alt=obj.alt)


class ExpressionTypeBase(Type):

    def value_from_raw(self, raw):
        if raw.value is None:
            return raw.missing_value('missing string')
        pad = raw.pad
        if pad is None:
            return raw.bad_value('a pad is required')
        try:
            expr = self.expression_class(pad.env, raw.value)
        except jinja2.TemplateSyntaxError as exc:
            return raw.bad_value('jinja syntax error: {!s}'.format(exc))
        return ExpressionDescriptor(pad, expr)


class ExpressionType(ExpressionTypeBase):
    expression_class = Expression


class FormatExpressionType(ExpressionTypeBase):
    name = 'format_expression'
    expression_class = FormatExpression


class ExpressionTypePlugin(Plugin):
    name = 'Expression Type'
    description = u'Add jinja-evaluated types.'

    def on_setup_env(self, **extra):
        self.env.add_type(ExpressionType)
        self.env.add_type(FormatExpressionType)
