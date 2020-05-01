# -*- coding: utf-8 -*-
try:
    from unittest import mock
except ImportError:             # pragma: no cover
    import mock

import pytest

import jinja2

from lektor.types import RawValue

from lektor_expression_type import (
    ExpressionDescriptor,
    ExpressionType,
    FormatExpressionType,
    ExpressionTypePlugin,
    )


class TestExpressionDescriptor(object):
    @pytest.fixture
    def expr(self):
        return mock.Mock(name='expression', spec=['evaluate'])

    @pytest.fixture
    def descriptor(self, lektor_pad, expr):
        return ExpressionDescriptor(lektor_pad, expr)

    def test_get_attr(self, descriptor, lektor_pad, expr):
        obj = mock.Mock(name='obj')
        assert descriptor.__get__(obj) is expr.evaluate.return_value
        assert expr.mock_calls == [
            mock.call.evaluate(lektor_pad, this=obj, alt=obj.alt),
            ]

    def test_get_class_attr(self, descriptor):
        assert descriptor.__get__(None, object) is descriptor


class ExpressionTypeTestBase(object):
    @pytest.fixture
    def expression(self):
        return self.test_expression

    @pytest.fixture
    def raw_value(self, expression, lektor_pad):
        return RawValue('test', expression, field=None, pad=lektor_pad)

    @pytest.fixture
    def record(self, lektor_pad):
        return lektor_pad.root

    @pytest.fixture
    def type_(self, lektor_env):
        return self.type_class(lektor_env, options={})

    def test(self, type_, raw_value):
        descr = type_.value_from_raw(raw_value)
        assert isinstance(descr, ExpressionDescriptor)

    @pytest.mark.parametrize('expression', [None])
    def test_missing(self, type_, raw_value):
        missing = type_.value_from_raw(raw_value)
        assert jinja2.is_undefined(missing)
        assert "missing string" in missing._undefined_message

    @pytest.mark.parametrize('lektor_pad', [None])
    def test_no_pad(self, type_, raw_value):
        bad_value = type_.value_from_raw(raw_value)
        assert jinja2.is_undefined(bad_value)
        assert "a pad is required" in bad_value._undefined_message

    # NB: expression carefully chose to be invalid syntax for both
    # a jinja expression and a jinja template
    @pytest.mark.parametrize('expression', ['{{ foo bar }}'])
    def test_jinja_syntax_error(self, type_, raw_value):
        bad_value = type_.value_from_raw(raw_value)
        assert jinja2.is_undefined(bad_value)
        assert "syntax error" in bad_value._undefined_message

    def test_integration(self, type_, raw_value, record):
        # Actually test evaluation of jinja expressions
        descr = type_.value_from_raw(raw_value)
        assert descr.__get__(record) == self.expected_value


class TestExpressionType(ExpressionTypeTestBase):
    type_class = ExpressionType

    test_expression = 'site.root.title'
    expected_value = "Welcome to Test Site!"


class TestFormatExpressionType(ExpressionTypeTestBase):
    type_class = FormatExpressionType

    test_expression = 'Number of subpages: {{ site.root.children.count() }}'
    expected_value = "Number of subpages: 2"


class TestExpressionTypePlugin(object):
    @pytest.fixture
    def plugin(self, lektor_env):
        return ExpressionTypePlugin(lektor_env, 'expression-type')

    def test_on_setup_env(self, plugin, lektor_env):
        plugin.on_setup_env()
        types = lektor_env.types
        assert types['expression'] is ExpressionType
        assert types['format_expression'] is FormatExpressionType
