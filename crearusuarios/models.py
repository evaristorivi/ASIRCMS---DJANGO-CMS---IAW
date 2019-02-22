from django.db import models
from django.core.management.base import BaseCommand, CommandError
from cms import constants
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms import api
from cms.models.pagemodel import Page, PageType, TreeNode
from cms.models.permissionmodels import GlobalPagePermission, PagePermission, PageUser, PageUserGroup
from django.contrib.auth.models import Group, Permission, User
from aldryn_newsblog.cms_appconfig import NewsBlogConfig, NewsBlogConfigTranslation
from django_auth_ldap.backend import LDAPBackend
from django.utils.translation import activate

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
# Create your models here.
@receiver(user_logged_in)
def creausuario(sender,user,request,**kwargs):
		if user.is_superuser == False:
			activate('en')
			permisos=['Can add boostrap3 panel body plugin','Can change boostrap3 panel body plugin','Can add boostrap3 panel plugin','Can change boostrap3 panel plugin','Can add article','Can change article','Can delete article','Can add cms plugin','Can change cms plugin','Can delete cms plugin','Can add placeholder','Can change placeholder','Can delete placeholder','Can use Structure mode','Can add placeholder reference','Can change placeholder reference','Can add content type','Can change content type','Can delete content type']
			usuario=User.objects.get(username=user.username)
			for p in permisos:
				per=Permission.objects.get(name=str(p))
				usuario.user_permissions.add(per)
			usuario.save()
			try:
				Page.objects.get(created_by=usuario)
			except Page.DoesNotExist:
				#Crear UserPage
				api.create_page_user(created_by=usuario,user=usuario,can_add_page=True)
				#Crear Blog
				blog=NewsBlogConfig()
				blog.app_title=usuario.username
				blog.namespace=usuario.username
				blog.save()
				#Crear pagina del usuario
				pagina=api.create_page(title=usuario.username,language='en',template=TEMPLATE_INHERITANCE_MAGIC,parent=None,created_by=usuario,apphook='NewsBlogApp',apphook_namespace=usuario.username) 
				#Permisos de usuario
				api.assign_user_to_page(pagina,usuario,can_add=True,can_change=True,can_delete=True)
				pagina.publish('en')
				pagina.save()
