from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

app_name = 'admingo'
''' PAra las tallas y Modelos
	url(r'^show_tallas$', views.show_tallas, name='show_tallas'),
	url(r'^save_talla$', views.save_talla, name='save_talla'),
	url(r'^show_modelos$', views.show_modelos, name='show_modelos'),
	url(r'^save_modelo$', views.save_modelo, name='save_modelo'),
'''
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^singup$', views.singup, name='singup'),
	url(r'^registroinsta$', views.registroinsta, name='registroinsta'),
	url(r'^registro$', views.registro, name='registro'),
	url(r'^cerrar_sesion$', views.cerrar_sesion, name='cerrar_sesion'),
	url(r'^vender$', views.vender, name='vender'),
	url(r'^pausar_venta$', views.pausar_venta, name='pausar_venta'),
	url(r'^play_venta$', views.play_venta, name='play_venta'),
	url(r'^ventas$', views.ventas, name='ventas'),
	url(r'^detalles_venta$', views.detalles_venta, name='detalles_venta'),
	url(r'^delete_venta$', views.delete_venta, name='delete_venta'),
	url(r'^upload_img$', views.upload_img, name='upload_img'),
	url(r'^nuevo_concurso$', views.nuevo_concurso, name='nuevo_concurso'),
	url(r'^nuevo_concurso/(?P<nuevo>[^/]+)/', views.nuevo_concurso, name='nuevo_concurso'),
	url(r'^publicar_concurso$', views.publicar_concurso, name='publicar_concurso'),
	url(r'^mis_concursos$', views.mis_concursos, name='mis_concursos'),
	url(r'^delete_concurso$', views.delete_concurso, name='delete_concurso'),
	url(r'^generar_ganadores$', views.generar_ganadores, name='generar_ganadores'),
	url(r'^guardar_ganadores$', views.guardar_ganadores, name='guardar_ganadores'),
	url(r'^publicar_ganadores$', views.publicar_ganadores, name='publicar_ganadores'),
	url(r'^productos$', views.productos, name='productos'),
	url(r'^agregar_producto$', views.agregar_producto, name='agregar_producto'),
	url(r'^editar_producto$', views.editar_producto, name='editar_producto'),

	url(r'^get_producto$', views.get_producto, name='get_producto'),
	url(r'^delete_producto$', views.delete_producto, name='delete_producto'),


	
]