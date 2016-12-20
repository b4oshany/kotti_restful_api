# -*- coding: utf-8 -*-

"""
Created on 2016-12-20
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from pytest import fixture


@fixture
def dummy_content(root):

    from kotti_restful_api.resources import CustomContent

    root['cc'] = cc = CustomContent(
        title=u'My content',
        description=u'My very custom content is custom',
        custom_attribute='Lorem ipsum'
    )

    return cc


def test_view(dummy_content, dummy_request):

    from kotti_restful_api.views.view import CustomContentViews

    views = CustomContentViews(dummy_content, dummy_request)

    default = views.default_view()
    assert 'foo' in default

    alternative = views.alternative_view()
    assert alternative['foo'] == u'bar'
