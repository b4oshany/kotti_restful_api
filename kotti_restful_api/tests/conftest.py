# -*- coding: utf-8 -*-

"""
Created on 2016-12-20
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

pytest_plugins = "kotti"

from pytest import fixture


@fixture(scope='session')
def custom_settings():
    import kotti_restful_api.resources
    kotti_restful_api.resources  # make pyflakes happy
    return {
        'kotti.configurators': 'kotti_tinymce.kotti_configure '
                               'kotti_restful_api.kotti_configure'}
