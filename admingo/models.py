from django.db import models
from datetime import datetime


class Usuarios(models.Model):
	nombre = models.CharField( max_length = 100, blank = True, null = True) # blank para colocarlo como obligatorio, null o default para establecer valores por defecto
	apellido = models.CharField( max_length = 100, blank = True, null = True)
	email = models.EmailField()
	password = models.CharField( max_length = 16, blank = True, null = True )
	username = models.CharField( max_length = 100, blank = True, null = True )
	sexo = models.CharField( max_length = 9, blank = True, null = True)
	user_insta = models.CharField( max_length = 100, blank = True, null = True)
	pass_insta = models.CharField( max_length = 100, blank = True, null = True)
	fecha_creacion = models.DateTimeField(default=datetime.now)
	fecha_modificacion = models.DateTimeField(default=datetime.now)
	#description = models.TextField( max_length = 300 )
	
	def __unicode__(self ):
		return self.email

	def __str__(self ):
		return self.email

	def get_username(self, email=email):
		if email == self.email:
			return self.username
		return False

class Productos(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	media_id = models.CharField( max_length = 1000 )
	talla = models.IntegerField(default=0)
	modelo = models.IntegerField(default=0)
	cantidad = models.IntegerField(default=0)
	disponible = models.IntegerField(default=1)
	texto = models.TextField(max_length= 1000, default = None)
	descripcion_producto = models.TextField(max_length= 1000, default = None)
	res_automatica = models.IntegerField(default=0)
	fecha_creacion = models.DateTimeField(default= datetime.now)


class Ventas(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	id_producto = models.IntegerField(default=0)
	media_id = models.CharField( max_length = 1000 )
	cantidad = models.IntegerField(default=0)
	varias = models.IntegerField(default=0)
	precio = models.DecimalField(max_digits = 19, decimal_places= 10)
	nombre_cliente = models.CharField(max_length= 100, default = None)
	telefono_cliente = models.CharField(max_length= 100, default = None)
	descripcion_venta = models.TextField(max_length= 1000, default = None)
	fecha_venta = models.DateTimeField(default= datetime.now)



class Imagenes(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	media_id = models.CharField( max_length = 1000 )
	imagen = models.TextField( max_length = 10000 )

class Info(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	username = models.CharField( max_length = 1000, blank = True, null = True)
	seguidores = models.IntegerField(default=0)
	seguidos = models.IntegerField(default=0)
	fotos = models.IntegerField(default=0)
	foto_perfil = models.TextField(max_length= 1000, default = None)
	hastags = models.IntegerField(default=0)
	fecha_creacion = models.DateTimeField(default= datetime.now)

class Concursos(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	img_url = models.CharField( max_length = 1000, null=True)
	media_id = models.CharField( max_length = 1000, null=True )
	ruta_img = models.CharField( max_length = 1000 )
	seguirnos = models.IntegerField(default=0)
	like = models.IntegerField(default=0)
	hastags = models.CharField( max_length = 1000, default=None)
	seguir_otros = models.CharField( max_length = 1000, default=None)
	cant_etiqueta = models.IntegerField(default=0)
	like_amigo_otros = models.IntegerField(default=0)
	seguirme_amigos = models.IntegerField(default=0)
	seguir_amigos_otras = models.IntegerField(default=0)
	condiciones = models.TextField(max_length= 1000)
	ganadores = models.IntegerField(default=0)
	activo = models.IntegerField(default=0)
	publi_ganadores = models.IntegerField(default=0)
	view_otro = models.IntegerField(default=0)
	fin_carga = models.IntegerField(default=0)
	fecha_creacion = models.DateTimeField(default= datetime.now)


class Ganadores(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	id_concurso = models.IntegerField(default=0)
	media_id = models.CharField( max_length = 1000, null=True )
	username = models.CharField( max_length = 1000 )
	fecha_creacion = models.DateTimeField(default= datetime.now)

class Pausas(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	media_id = models.CharField( max_length = 1000, null=True )
	fecha_creacion = models.DateTimeField(default= datetime.now)

class Finanzas(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	id_producto = models.IntegerField(default=0)
	media_id = models.CharField( max_length = 1000 )
	cantidad = models.IntegerField(default=0)
	precio = models.DecimalField(max_digits = 19, decimal_places= 10)
	nombre_cliente = models.CharField(max_length= 100, default = None)
	telefono_cliente = models.CharField(max_length= 100, default = None)
	descripcion_finanza = models.TextField(max_length= 1000, default = None)
	fecha_creacion = models.DateTimeField(default= datetime.now)

class Modelos(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
	media_id = models.CharField( max_length = 1000 )
	nombre = models.CharField( max_length = 1000 )
	fecha_creacion = models.DateTimeField(default= datetime.now)

class Tallas(models.Model):
	id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
	id_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
	media_id = models.CharField( max_length = 1000 )
	nombre = models.CharField( max_length = 1000 )
	fecha_creacion = models.DateTimeField(default= datetime.now)

