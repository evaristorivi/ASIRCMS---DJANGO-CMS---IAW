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


class Command(BaseCommand):
	#Indicar el nombre de usuario como argumento
	def add_arguments(self, parser):
		parser.add_argument('user',type=str)
		 
	def handle(self, *args, **options):
    #Activar idioma
		activate('en')
		#Recuperar el parámetro guardándolo en la variables user
    user=options['user']
		#Lista de permisos
    permisos=['Can add boostrap3 panel body plugin','Can change boostrap3 panel body plugin','Can add boostrap3 panel plugin','Can change boostrap3 panel plugin','Can add article','Can change article','Can delete article','Can add cms plugin','Can change cms plugin','Can delete cms plugin','Can add placeholder','Can change placeholder','Can delete placeholder','Can use Structure mode','Can add placeholder reference','Can change placeholder reference','Can add content type','Can change content type','Can delete content type']
		usuario=LDAPBackend().populate_user(user)
		#Si el usuairo no existe en LDAP asignaremos permisos y si no existe la página del usuario crearmos la Userpage, el blog para el usuario y la página del usuario, luego
    #asignaremos permisos y finalmente publicaremos la página.
    #si ya existe la página del usuario entonces mostramos un mensaje informativo.
    if usuario is None:
			self.stdout.write(self.style.SUCCESS('No existe ese usuario en LDAP.'))
		
		else:
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
				self.stdout.write(self.style.SUCCESS('Usuario creado + blog'))
			
			else:
				self.stdout.write(self.style.SUCCESS('El usuario ya tiene página + blog.'))
