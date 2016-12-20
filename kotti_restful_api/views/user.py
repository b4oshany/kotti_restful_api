# -*- coding: utf-8 -*-

"""
Created on 2016-01-13
:author: Alteroo Team (oshane@alteroo.com)
"""

import io
import os
import re
import json
import csv
import copy
import time
import deform
import urllib
import shutil
import zipfile
import logging
import mimetypes
import subprocess
import urlparse
import transaction
from datetime import datetime
import colander


from kotti import DBSession
from kotti.security import ROLES
from kotti.security import SHARING_ROLES
from kotti.security import USER_MANAGEMENT_ROLES
from kotti.security import get_principals, principals_with_local_roles
from kotti.security import set_groups
from kotti.security import has_permission, list_groups
from kotti.message import send_email, make_token
from kotti.views.site_setup import CONTROL_PANEL_LINKS
from kotti.views import login as kotti_login
from kotti.views import users as kotti_users

from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid import httpexceptions as httpexc
from pyramid.security import forget, remember

from sqlalchemy import func as sql_func

from kotti_restful_api.views import BaseView
from kotti.views.form import AddFormView


class UserViews(BaseView):

    def get_key_token(self, user):
        token = make_token(user)
        user.confirm_token = unicode(token)
        skip_url = "{}-tst-{}-tst-{}".format(
            token,
            user.email,
            's{}w'.format(datetime.now().strftime("%d%m%y%H"))
        )

        return '{0}/@@login?ketoken={1}'.format(
            self.request.application_url,
            skip_url
        )

    @view_config(name='login-status',
                 renderer='json',
                 root_only=True)
    def login_status(self):
        if self.request.user is not None:
            return {
                "status": "success",
                "message": "User has been authenticated"
            }
        return {
            'status': 'failed',
            'url': self.request.application_url + '/@@login',
            'message': 'No user data was sent'
        }

    @view_config(name='login',
                 renderer='json',
                 root_only=True,
                 request_method="POST",
                 content_type="application/json")
    def json_login(self):
        return self.login()

    @view_config(name='login',
                 renderer='json',
                 root_only=True,
                 cross_request="restful",
                 request_method="POST")
    def cross_login(self):
        return self.login()

    def login(self):
        """
        Login view.  Renders either the login or
        password forgot form templates or
        handles their form submission and redirects to came_from on success.
        :result: Either a redirect response or a dictionary passed
                 to the template
                 for rendering
        :rtype: pyramid.httpexceptions.HTTPFound or dict
        """

        principals = get_principals()
        came_from = self.request.params.get(
            'came_from', self.request.resource_url(self.context))
        login, password = u'', u''
        try:
            login = self.request.params["username"].lower()
            password = self.request.params["password"]
        except Exception as e:
            print e
            try:
                params = json.loads(self.request.body)
            except Exception as e:
                print e
                params = dict(urlparse.parse_qsl(self.request.body))
            
            login = params.get("username", "")
            password = params.get("password", "")
        if login and password:
            user = kotti_login._find_user(login)
            if user is None:
                return {
                    "status": "failed",
                    "message": "No user was found"
                }
            if (principals.validate_password(password, user.password)):

                headers = remember(self.request, user.name)
                print headers
                user.last_login_date = datetime.now()
                return httpexc.HTTPFound(location="/@@login-status?from_login=1",
                                 headers=headers)
            return {
                "status": "failed",
                "message": "Incorrect password"
            }


        return {
            'status': 'failed',
            'url': self.request.application_url + '/@@login',
            'came_from': came_from,
            'login': login,
            'message': 'No user data was sent'
        }
