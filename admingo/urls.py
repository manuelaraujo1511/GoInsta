from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'admingo'

urlpatterns = [
	url(r'^$', views.singup, name='singup'),
	url(r'^index$', views.index, name='index'),
	url(r'^registroinsta$', views.registroinsta, name='registroinsta'),
	url(r'^registro$', views.registro, name='registro'),
	url(r'^cerrar_sesion$', views.cerrar_sesion, name='cerrar_sesion'),
	url(r'^vender$', views.vender, name='vender'),
	url(r'^pausar_venta$', views.pausar_venta, name='pausar_venta'),
	url(r'^ventas$', views.ventas, name='ventas'),
	url(r'^upload_img$', views.upload_img, name='upload_img'),
	url(r'^nuevo_concurso$', views.nuevo_concurso, name='nuevo_concurso'),
	url(r'^publicar_concurso$', views.publicar_concurso, name='publicar_concurso'),
	url(r'^mis_concursos$', views.mis_concursos, name='mis_concursos'),
	url(r'^generar_ganadores$', views.generar_ganadores, name='generar_ganadores'),
	url(r'^guardar_ganadores$', views.guardar_ganadores, name='guardar_ganadores'),
	url(r'^publicar_ganadores$', views.publicar_ganadores, name='publicar_ganadores'),
	url(r'^productos$', views.productos, name='productos'),
	url(r'^editar_producto$', views.editar_producto, name='editar_producto'),

	
]