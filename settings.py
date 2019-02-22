# -*- coding: utf-8 -*-
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-django-cms',
    'aldryn-bootstrap3',
    'aldryn-newsblog',
    'djangocms-googlemap',
    'djangocms-history',
    'djangocms-snippet',
    'djangocms-style',
    'djangocms-text-ckeditor',
    'djangocms-video',
    'django-filer',
    # </INSTALLED_ADDONS>
]


import aldryn_addons.settings
aldryn_addons.settings.load(locals())


# all django settings can be altered here

INSTALLED_APPS.extend([
    # add your project specific apps here
     'django_extensions',
     'crearusuarios',
])



AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_LDAP_SERVER_URI = "ldap://192.168.1.70"

AUTH_LDAP_BIND_DN = "cn=admin,dc=planetexpress,dc=com"
AUTH_LDAP_BIND_PASSWORD = "GoodNewsEveryone"
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,dc=planetexpress,dc=com",
    ldap.SCOPE_SUBTREE, "(cn=%(user)s)")


AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=people,dc=planetexpress,dc=com",
    ldap.SCOPE_SUBTREE, "(objectClass=Group)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_MIRROR_GROUPS = True


