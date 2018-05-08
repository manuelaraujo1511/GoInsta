from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from InstagramAPI import InstagramAPI
from .models import *
from decimal import *
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from PIL import Image

import json
import re
import os, sys
import random
import locale
locale.setlocale( locale.LC_ALL, '' )


# Create your views here.
def getTotalCommentsMedia(api, mediaId):
  verdad= True
  next_max_id = ''
  all_comments = []
  while verdad:
      #print("Entre al while")
      api.getMediaComments(mediaId, next_max_id)
      tem = api.LastJson
      for t in tem['comments']:
          all_comments.append(t)

      if tem['has_more_comments'] is True:
          #print(str(json.loads(tem['next_max_id'])['server_cursor']))
          next_max_id = json.loads(tem['next_max_id'])['server_cursor']
      else:
          verdad = False
  return all_comments

def get_precio(request):
	precio = 0
	if Finanzas.objects.filter(id_usuario_id=request.user.id).exists():
		ventas = Finanzas.objects.filter(id_usuario_id=request.user.id)
		for v in ventas:
			precio +=  (int(v.precio)*int(v.cantidad))


	return locale.currency(precio, grouping=True )

def resize_image(input_image_path,output_image_path,size):
	
	original_image = Image.open(input_image_path)
	
	width, height = original_image.size
	
	print('The original image size is {wide} wide x {height} ' 'high'.format(wide=width, height=height))
	
	resized_image = original_image.resize(size)
	
	width, height = resized_image.size
	
	print('The resized image size is {wide} wide x {height} ''high'.format(wide=width, height=height))
	
	resized_image.show()
	
	resized_image.save(output_image_path)

def get_save_info(api,user_r, user_insta, pass_insta):
	if (api != None):
		api.searchUsername(str(user_insta))
		img_profile = api.LastJson['user']['profile_pic_url']
		follower = api.LastJson['user']['follower_count']
		following = api.LastJson['user']['following_count']
		info_user = Info.objects.get(id_usuario=user_r)
		info_user.seguidores = follower
		info_user.seguidos = following
		info_user.foto_perfil= img_profile
		info_user.save()
	else:
		info_user = Info.objects.get(id_usuario=user_r)
	return info_user

def get_producto(request):
	if request.method == "POST":
		if request.is_ajax():
			media_id = request.POST.get('media_id')
			if (Productos.objects.filter(media_id=media_id).exists()):
				pro = Productos.objects.get(media_id=media_id)
				producto = {'encontre': True,'media_id':pro.media_id, 'cantidad': pro.cantidad,  'disponible': pro.disponible, 'descripcion_producto': pro.descripcion_producto, 'res_automatica': pro.res_automatica}
			else:
				producto = {'encontre': False}

		
			context = {
				'producto':producto
			}
			#print ("get_producto Producto cantidad "+ str(pro.cantidad))
			return JsonResponse(context)


def save_talla(request):
	if request.method == "POST":
		if request.is_ajax():
			estado = 0
			media_id = request.POST.get('media_id')
			talla = request.POST.get('talla')

			producto = Productos.objects.get(media_id=media_id)
			if(Tallas.objects.filter(nombre=talla, media_id=media_id, id_usuario_id = request.user.id, id_producto=producto.id).exists()):
				estado = 2
			else:
				Tallas(id_usuario_id=request.user.id, id_producto_id=producto.id, media_id=media_id, nombre=talla).save()
				estado = 1
		context = {'estado':estado}
		return JsonResponse(context)

def save_modelo(request):
	if request.method == "POST":
		if request.is_ajax():
			estado = 0
			media_id = request.POST.get('media_id')
			modelo = request.POST.get('modelo')

			producto = Productos.objects.get(media_id=media_id)
			if(Modelos.objects.filter(nombre=modelo, media_id=media_id, id_usuario_id = request.user.id, id_producto=producto.id).exists()):
				estado = 2
			else:
				Modelos(id_usuario_id=request.user.id, id_producto_id=producto.id, media_id=media_id, nombre=modelo).save()
				estado = 1
		context = {'estado':estado}
		return JsonResponse(context)

def show_tallas(request):
	if request.method == "POST":
		if request.is_ajax():
			estado = 0
			tallas = []
			media_id = request.POST.get('media_id')
			pro = Productos.objects.get(media_id=media_id)
			if(Tallas.objects.filter(id_usuario_id= request.user.id, media_id=media_id).exists()):
				tall = Tallas.objects.filter(id_usuario_id= request.user.id, media_id=media_id)
				for t in tall:
					tallas.append({'id': t.id, 'producto_id': t.id_producto_id, 'media_id': t.media_id, 'nombre': t.nombre})
					print(str(t.nombre))
				estado = 1
				

		context = {'estado': estado, 'tallas':tallas, 'producto_talla': pro.talla}
		return JsonResponse(context)

def show_modelos(request):
	if request.method == "POST":
		if request.is_ajax():
			estado = 0
			modelos = []
			media_id = request.POST.get('media_id')
			pro = Productos.objects.get(media_id=media_id)
			if(Modelos.objects.filter(id_usuario_id= request.user.id, media_id=media_id).exists()):
				model = Modelos.objects.filter(id_usuario_id= request.user.id, media_id=media_id)
				for m in model:
					modelos.append({'id': m.id, 'producto_id': m.id_producto_id, 'media_id': m.media_id, 'nombre': m.nombre})
					print(str(m.nombre))
				estado = 1
				

		context = {'estado': estado, 'modelos':modelos, 'producto_modelo': pro.modelo}
		return JsonResponse(context)

				

@login_required
def index(request):
	# IMPORTANTE: comprobar conexion a internet
	user_r= Usuarios.objects.get(email=request.user.email)
	#username_insta = ""+user_r.user_insta+""

	api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
	api.login()
	
	has_more_feed = True
	feed = []
	feed_res = []	
	next_max_id = ''
	usernameId = api.username_id
	minTimestamp=None
	guardo=True

	## Eliminar de la tabla los concursos que no terminaron de publicar
	concursos_delete = Concursos.objects.filter(id_usuario_id=request.user.id, fin_carga=0)
	### cargar informacion actualizada de usuario
	info_user=get_save_info(api,user_r,user_r.user_insta, user_r.pass_insta)
	
	concursos_abiertos=Concursos.objects.filter(id_usuario=user_r, activo=1).count()
	concursos_cerrados=Concursos.objects.filter(id_usuario=user_r, activo=0).count()

	usuario_info = {'foto_perfil': info_user.foto_perfil,'concursos_abiertos': concursos_abiertos, 'concursos_cerrados':concursos_cerrados ,'seguidos': info_user.seguidos, 'seguidores': info_user.seguidores,  'username': user_r.user_insta}
	
	
	for con_d in concursos_delete:
		con_d.delete()
	## fiin de eliminar los que no terminaron de cargar

	todos_concursos = Concursos.objects.filter(id_usuario_id=request.user.id, fin_carga=1)
	pausas = Pausas.objects.filter(id_usuario_id=request.user.id)
	productos = Productos.objects.filter(id_usuario_id=request.user.id)


	if (todos_concursos.exists()):		

		while has_more_feed:

		  api.getUserFeed(usernameId, next_max_id, minTimestamp)
		  temp = api.LastJson

		  for item in temp["items"]:
		  	for p in pausas:
		  		if(str(item['caption']['media_id']) == str(p.media_id)):
		  			item['caption']['pausado'] = True
		  		else:
		  			item['caption']['pausado'] = False
		  	
		  	item['caption']['cant_pro'] = -1

		  	if (not productos):
		  		item['caption']['producto'] = False
		  		
		  	else:
		  		for pro in productos:
			  		if(str(item['caption']['media_id']) == str(pro.media_id)):
			  			item['caption']['producto'] = pro
			  		else:
			  			item['caption']['producto'] = False
		  		

		  	for con in todos_concursos:
		  		if(str(item['caption']['media_id']) == str(con.media_id)):
		  			guardo = False
		  			break


		  	if (guardo):
		  		feed.append(item)
		  	guardo = True
		  if temp["more_available"] is False:

		    has_more_feed = False
		  
		  else:
		  	guardo = True
		  	next_max_id = temp["next_max_id"]
	#print(str(feed))
	else:
		while has_more_feed:

		  api.getUserFeed(usernameId, next_max_id, minTimestamp)
		  temp = api.LastJson

		  for item in temp["items"]:
		  	for p in pausas:
		  		if(str(item['caption']['media_id']) == str(p.media_id)):
		  			item['caption']['pausado'] = True
		  		else:
		  			item['caption']['pausado'] = False
		  	item['caption']['cant_pro'] = -1
		  	
		  	if not productos:
		  		item['caption']['producto'] = False
		  	else:
			  	for pro in productos:
			  		if(str(item['caption']['media_id']) == str(pro.media_id)):
			  			item['caption']['producto'] = pro
			  		else:
			  				item['caption']['producto'] = False
			  	
		  	feed.append(item)

		  if temp["more_available"] is False:
		    
		    print("entre si es falso")

		    has_more_feed = False
		  
		  else:
		  	next_max_id = temp["next_max_id"]
	context = {
		'usuario' : usuario_info,
		'feed' : feed,
		'pausas': pausas,
		'monto_total' : get_precio(request)

	}
	
	api.logout()
	return render(request, 'index.html', context)

def singup(request):
	#if request.user is not None:
	#	return redirect("admingo:index")
	#global api
	print (str(request))
	
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']

		try:

			user_u = Usuarios.objects.get(email=email)
			user_name=user_u.username

			if user_u.user_insta is not None:
				if user_name is not False:
					#print (user_name)
					#print (password)
					user = authenticate(request, username=user_name, password=password)

					#print(user)
					if user is not None:
						if user.is_active:
							

							api = InstagramAPI(user_u.user_insta, user_u.pass_insta)
							if api.login():
								
								login(request, user)
								# Guardo en info
								api.searchUsername(str(user_u.user_insta))
								img_profile = api.LastJson['user']['profile_pic_url']
								follower = api.LastJson['user']['follower_count']
								following = api.LastJson['user']['following_count']
								
								info_user =Info.objects.get(id_usuario_id=request.user.id)

								info_user.img_profile=img_profile
								info_user.seguidores=follower
								info_user.seguidos=following
								info_user.save()


								messages.success(request, 'Bienvenido ' + user_u.nombre + ' '+user_u.apellido)
								api.logout()
								return redirect('admingo:index')
						else:
							messages.error(request, 'Datos Incorrectos, Intente de Nuevo')
						return render(request, 'singup.html')		
					else:
						messages.error(request, 'Datos Incorrectos, Intente de Nuevo')
						return render(request, 'singup.html')	
			else:
				#request.method= "GET"
				context = {
					'username': user_name,
					'password' : password
				}
				messages.error(request, "Debes Registrar tu cuenta de Instagram para poder ingresar.")
				return render(request, 'registroinsta.html', context)


		except ObjectDoesNotExist:
			messages.error(request, 'Datos Incorrectos, Intente de Nuevo.')
			return render(request, 'singup.html')
	return render(request, 'singup.html')

def registro(request):
	#print (request.method)
	if request.method == "POST":
		nombre = request.POST['nombre']
		apellido = request.POST['apellido']
		email = request.POST['email']
		password = request.POST['contraseña']
		username = email

		'''
		if Usuarios.objects.filter(username=username).exists():
			messages.error(request, 'Nombre de Usuario ya existe')
			return render(request, 'registro.html')
		else:
		'''
		if Usuarios.objects.filter(email=email).exists():
			messages.error(request ,'Email ya se encuentra registrado')
		else:
			user = User.objects.create_user(username, email, password)
			user.first_name = nombre
			user.last_name = apellido
			user.save()

			u = Usuarios(nombre=nombre, apellido=apellido, email=email,password=password,username=username)
			u.save()
			context = {
				'username': username,
				'password' : password
			}
			#messages.success(request, 'calida')
			return render(request, 'registroinsta.html', context)
	
	return render(request, 'registro.html')

def registroinsta(request):
	
	#global api 

	if request.method == "POST":
		# User Instagram
		cuenta = request.POST['cuenta']		
		password_i = request.POST['password_i']
		# ---------------
		username = request.POST['username']
		password = request.POST['password']
		user_u = Usuarios.objects.get(username=username)
		

		api = InstagramAPI(cuenta, password_i)


		if api.login():
			


			Usuarios.objects.filter(username=username).update(user_insta=cuenta, pass_insta=password_i)
			user = authenticate(request, username=username, password=password)


			login(request, user)
			# Guardo en info
			api.searchUsername(str(cuenta))
			img_profile = api.LastJson['user']['profile_pic_url']

			Info(id_usuario_id=request.user.id, username=username, foto_perfil= img_profile).save()

			messages.success(request, 'Bienvenido ' + user_u.nombre + ' ' + user_u.apellido)
			api.logout()
			return redirect("admingo:index")
		else:
			#api.logout()
			messages.error(request, "Usuario no existe o Contraseñana invalida")

	return render(request, 'registroinsta.html')

@login_required
def cerrar_sesion(request):
	#api.logout() # logout in Instagram
	logout(request)
	#print("ceree SESION")
	return redirect('admingo:singup')

@login_required
def vender(request):
	#print (str(request.user.id))
	estado = 1
	if request.method == "POST":
		if request.is_ajax():
			varias=0
			#id_usuario = request.user.id
			nombre_cliente = request.POST.get('nombre')
			telefono_cliente = request.POST.get('telefono')
			cantidad = request.POST.get('cantidad')
			precio = request.POST.get('precio')
			descripcion_venta = request.POST.get('descripcion')
			media_id = request.POST.get('media_id')
			texto = request.POST.get('texto')
			result_img = request.POST.getlist('result_img[]')
			#print (str(result_img[0].split(',')[0]))
			user_r= Usuarios.objects.get(username=request.user)

			if len(result_img) > 1:
				varias=1


		
			if (Productos.objects.filter(id_usuario_id = request.user.id, media_id = media_id).exists()):

				producto = Productos.objects.get(id_usuario_id = request.user.id, media_id = media_id)

				#validar la cantidad en stock con la venta
				print(str("validando cantidad: ----> "+str(int(producto.cantidad) - int(cantidad))))
				if ((int(producto.cantidad) - int(cantidad)) < 0):
					estado = 0
				else:
					producto.cantidad = int(producto.cantidad) - int(cantidad)

					producto.save()
						
					Ventas(id_usuario = user_r, id_producto=producto.id, media_id = media_id, cantidad = cantidad, varias=varias, precio = precio, nombre_cliente=nombre_cliente, telefono_cliente = telefono_cliente, descripcion_venta = descripcion_venta).save()

					Finanzas(id_usuario = user_r, id_producto=producto.id, media_id = media_id, cantidad = cantidad,precio = precio, nombre_cliente=nombre_cliente, telefono_cliente = telefono_cliente, descripcion_finanza = descripcion_venta).save()

					#print("producto.id: "+ str(producto.id))
			else:
				print("sino")
				
				#Productos(id_usuario = user_r, media_id=media_id, texto=texto, descripcion_producto=descripcion_venta).save()

				#producto = Productos.objects.get(id_usuario_id = request.user.id, media_id = media_id)

				Ventas(id_usuario = user_r, media_id = media_id, cantidad = cantidad, varias=varias, precio = precio, nombre_cliente=nombre_cliente, telefono_cliente = telefono_cliente, descripcion_venta = descripcion_venta).save()

				Finanzas(id_usuario = user_r, media_id = media_id, cantidad = cantidad,precio = precio, nombre_cliente=nombre_cliente, telefono_cliente = telefono_cliente, descripcion_finanza = descripcion_venta).save()
		
			for res in result_img:
			
				if (not Imagenes.objects.filter(media_id= media_id).exists()):
					Imagenes(id_usuario = user_r, media_id= media_id, imagen=res.split(',')[1]).save()
					print (str("NNNNNNNNNNNNNNN imagen----> "+res.split(',')[1]))
				else:
					print (str("IIIIIIIII imagen----> "+res.split(',')[1]))


			context = {'estado': estado}
	return JsonResponse(context)

@login_required
def pausar_venta(request):
	if request.method == "POST":
		print ("entre a pausar Venta POST")
		
		user_r= Usuarios.objects.get(email=request.user.email)

		api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
		api.login()

		estado =0

		if request.is_ajax():
			desde_pro =request.POST.get('desde_pro')
			if desde_pro == 0:
				texto = request.POST.get('texto')
				media_id = request.POST.get('media_id')
				if(Productos.objects.filter(media_id=media_id).exists()):
					pro=Productos.objects.get(media_id=media_id)
					pro.texto=texto
					pro.save()

				if(api.editMedia(media_id, ""+texto+"")):
					estado = 1
				
				api.logout()
				
				Pausas(id_usuario=user_r, media_id=media_id).save()
			else:
				texto = request.POST.get('texto')
				media_id = request.POST.get('media_id')
				pro = Productos.objects.get(media_id=media_id)
				pro.texto = texto
				pro.save();
				
				if(api.editMedia(media_id, ""+texto+"")):
					estado = 1
				
				api.logout()
				
				Pausas(id_usuario=user_r, media_id=media_id).save()
			
			context = {'estado': estado}
	return JsonResponse(context)

@login_required
def play_venta(request):

	if request.method == "POST":
		
		print ("entre a pausar Venta POST")
		user_r= Usuarios.objects.get(email=request.user.email)
		username_insta = ""+user_r.user_insta+""

		api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
		api.login()

		if request.is_ajax():
			estado= 0
			texto = request.POST.get('texto')
			media_id = request.POST.get('media_id')
			if (api.editMedia(media_id, ""+texto+"")):
				estado =1
			api.logout()
			# buscar en productos si esta pausada la venta
			product=Productos.objects.get(media_id=media_id)
			if (product):
				product.texto = texto
				product.save()

			pausa = Pausas.objects.get(media_id=media_id)
			pausa.delete()
			
			context = {'estado': estado}
	return JsonResponse(context)

@login_required
def ventas (request):

	todas_ventas = Ventas.objects.filter(id_usuario_id=request.user.id)
	ventas_distinc = Ventas.objects.filter(id_usuario_id=request.user.id).values_list('media_id', flat=True).distinct()
	imagenes = Imagenes.objects.filter(id_usuario_id=request.user.id)
	
	user_r= Usuarios.objects.get(email=request.user.email)

	
	### cargar informacion actualizada de usuario
	info_user=get_save_info(None,request.user.id,user_r.user_insta, user_r.pass_insta)

	usuario_info = {'foto_perfil': info_user.foto_perfil,'seguidos': info_user.seguidos, 'seguidores': info_user.seguidores,  'username': user_r.user_insta}


	arr_img = []
	arr_ventas = []
	into = False
	
	for vd in ventas_distinc:
		'''
		for v in todas_ventas:
			if (v.media_id == vd):
				
		'''
		for img in imagenes:
			if (img.media_id == vd):

				arr_img.append(img.imagen)
			
		arr_ventas.append({'media_id': vd, 'imagen': arr_img, 'cant_img': len(arr_img)})

		arr_img = []
		

	context = {
		'usuario' : usuario_info,
		'todas_ventas': arr_ventas,
		'monto_total' : get_precio(request)
	}

	return render (request,'ventas.html', context)


def detalles_venta (request):
	if request.method == "POST":
		media_id = request.POST.get('media_id')
		ventas=Ventas.objects.filter(media_id=media_id)
		arr_ventas = []
		cont=0
		for v in ventas:
			#date=split(v.fecha_venta,'T')
			#date_bien = date[2]+"/"date[1]+"/"+date[0]
			print(str(v.fecha_venta.strftime("%d-%m-%Y")))
			monto_v = (v.precio*v.cantidad)
			monto_venta = locale.currency(monto_v, grouping=True )
			precio=locale.currency( v.precio, grouping=True )
			arr_ventas.append({'cantidad':v.cantidad,'precio': precio,'monto_venta': monto_venta, 'nombre_cliente': v.nombre_cliente, 'telefono_cliente': v.telefono_cliente,'descripcion_venta': v.descripcion_venta, 'fecha_venta': v.fecha_venta.strftime("%d-%m-%Y")})
			cont+=1
		context = {
			'ventas': arr_ventas,
			'cont' : cont
		}
		return JsonResponse(context)

def delete_venta (request):
	if request.method == "POST":
		media_id = request.POST.get('media_id')
		ventas=Ventas.objects.filter(media_id=media_id)
		
		estado = 0
		for v in ventas:
			if (v.delete()):
				estado = 1
			else:
				estado = 0

		
		context ={
			'estado': estado
		}
		return JsonResponse(context)

def upload_img(request):
	ruta_original=os.getcwd()
	

	if request.method == 'POST' and request.FILES['img-ig']:
		# Creo carpeta de Usuario
		ruta = os.getcwd()+"/admingo/static/img/usuario-"+str(request.user.id)+"/"

		if(os.path.exists(ruta)):
			
			#me muevo hasta la carpeta de usuario
			os.chdir(ruta)

		else:
			#me muevo hasta la carpeta de usuario
			os.mkdir(ruta)

			#me muevo hasta la carpeta creada
			os.chdir(ruta)		

		myfile = request.FILES['img-ig']
		#print ("myfile: "+ str(myfile))

		if not os.path.isfile(str(myfile)):	

			fs = FileSystemStorage()

			

			filename = fs.save(myfile.name, myfile)
			#print ("filename: "+ str(filename))
			
			#Guardo el archivo
			uploaded_file_url = fs.url(filename)

			

		#me muevo a la ruta del proyecto
		os.chdir(ruta_original)
		#resize_image(ruta+'/'+myfile.name, ruta+'/'+myfile.name+'-resize',size=(780, 780))


	context = {'imagen': str(myfile)}
	return JsonResponse(context)

@login_required
def nuevo_concurso (request, nuevo =None):
	if (request.is_ajax()):
		print ('entro si request ajax')
		user_r= Usuarios.objects.get(email=request.user.email)
		username_insta = ""+user_r.user_insta+""

		api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
		api.login()

		media_id = request.POST.get('media_id')
		print("media_id desde python "+ str(media_id))
	
		api.mediaInfo(media_id)

		media_info= api.LastJson
		#print("media type:  "+str(media_info["items"][0]["media_type"]))
		imagen = []
		hastag= ""
		existe_img= False

		if (media_info["items"][0]["media_type"] == 1):
			
			comentario=media_info["items"][0]["caption"]["text"]
			img_url=media_info["items"][0]["image_versions2"]["candidates"][0]["url"]

			## para determinar los hastags del comentario
			tag_re = re.compile('#(\w+)')
			lista_hastag = tag_re.findall(comentario)
			for c in lista_hastag:
				hastag+= " #"+c+" "

			print(str(hastag))
			if (not Imagenes.objects.filter(id_usuario = user_r,media_id=media_id).exists()):
				Imagenes(id_usuario = user_r,media_id=media_id, imagen=img_url).save()

				Concursos(id_usuario = user_r,img_url=img_url,media_id=media_id,hastags = hastag,  seguir_otros= "",condiciones = comentario, view_otro = 1).save()
		else:
			
			
			arra_img=[]

			for img in media_info["items"][0]["carousel_media"]:
			
				if (not Imagenes.objects.filter(id_usuario = user_r,media_id=media_id).exists()):

					Imagenes(id_usuario = user_r,media_id=media_id, imagen=img["image_versions2"]["candidates"][0]['url']).save()

				else:
					existe_img = True
					break


			comentario=media_info["items"][0]["caption"]["text"]
			## para determinar los hastags del comentario
			tag_re = re.compile('#(\w+)')
			lista_hastag = tag_re.findall(comentario)
			for c in lista_hastag:
				hastag+= " #"+c+" "
			if (not existe_img):
				Concursos(id_usuario = user_r,img_url="",media_id=media_id,hastags = hastag, seguir_otros= "",condiciones = comentario, view_otro = 1).save()


		context = {
		
			'estado' : request.user.id
		}
		api.logout()
		#return render (request,'nuevo_concurso.html', context)

		return JsonResponse(context)
	else:
		user_r= Usuarios.objects.get(email=request.user.email)


		### cargar informacion actualizada de usuario
		info_user=get_save_info(None,request.user.id,user_r.user_insta, user_r.pass_insta)
		
		concursos_abiertos=Concursos.objects.filter(id_usuario=user_r, activo=1).count()
		concursos_cerrados=Concursos.objects.filter(id_usuario=user_r, activo=0).count()

		usuario_info = {'foto_perfil': info_user.foto_perfil,'concursos_abiertos': concursos_abiertos, 'concursos_cerrados':concursos_cerrados ,'seguidos': info_user.seguidos, 'seguidores': info_user.seguidores,  'username': user_r.user_insta}

			
		
		if(nuevo == None):

			print("entro si nuevo_concurso request no ajax y nuevo = None")
			print("User ID: " + str(request.user.id))	
			concursos = None
			imagenes_count = "0"
			imagenes=None
			if Concursos.objects.filter(id_usuario_id=request.user.id, view_otro = 1).exists():
				concursos = Concursos.objects.filter(id_usuario_id=request.user.id, view_otro = 1)
				for c in concursos:
					imagenes = Imagenes.objects.filter(id_usuario_id=request.user.id, media_id = c.media_id)
				
				imagenes_count = imagenes.count()

				#print("imagenes_count: "+ str(imagenes_count))
				## Esto esta por hacer ###
				##usuario = Info.objects.get(id_usuario_id=request.user.id)
				###
			#print("concursos: "+str(concursos))
			context = {
					'usuario' : usuario_info,
					'concursos': concursos,
					'imagenes' : imagenes 	,
					'imagenes_count': str(imagenes_count),
					'monto_total' : get_precio(request)
				}

		else:
			context = {
				'usuario' : usuario_info,
				'monto_total' : get_precio(request)
			}
		
		return render (request,'nuevo_concurso.html', context)

@login_required
def publicar_concurso(request):
	if request.method == "POST":


		ruta_original=os.getcwd()
		#print ("ruta original: "+str(ruta_original))
		#print ("entre a Publicar Concurso POST")
		user_r= Usuarios.objects.get(email=request.user.email)
		username_insta = ""+user_r.user_insta+""

		api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
		api.login()
		if request.is_ajax():
						
			img = request.POST.get('img')
			img2 = "admingo"+request.POST.get('img')
			comentario = request.POST.get('comentario')
			seguirme = request.POST.get('seguirme')
			like = request.POST.get('like')
			hastag = request.POST.get('hastag')
			seguir_otros = request.POST.get('seguir_otros')
			cant_etiqueta = request.POST.get('cant_etiquetas')
			amigos_like_otros = request.POST.get('amigos_like_otros')
			amigos_seguirme = request.POST.get('amigos_seguirme')
			amigos_seguir_otros = request.POST.get('amigos_seguir_otros')
			ganadores = request.POST.get('ganadores')
			media_id = request.POST.get('media_id')

			if (media_id != 0):
				print("media_id != 0")
				concurso = Concursos.objects.filter(id_usuario_id=request.user.id, media_id = media_id)
				for con in concurso:
					con.seguirnos=seguirme
					con.like=like
					con.hastags=hastag
					con.seguir_otros=seguir_otros
					con.cant_etiqueta=cant_etiqueta
					con.like_amigo_otros=amigos_like_otros
					con.seguirme_amigos=amigos_seguirme
					con.seguir_amigos_otras=amigos_seguir_otros
					con.ganadores=ganadores
					con.activo = 1
					con.fin_carga = 1
					con.save()
				context = {'estado': 1}
			else:			

				## subir foto al Insta
				api.uploadPhoto(str(img2), ""+comentario+"")
				subir_foto=api.LastJson
				#print("subir foto: "+str(subir_foto))
				#####

				## para buscar la ultima publicacion
				next_max_id=''
				has_more_feed = True
				minTimestamp= 100
				feed = []
				usernameId= api.username_id
				media_id = ''
				img_url  = ''
				iguales = True
				########

				while has_more_feed:

				  api.getUserFeed(usernameId, next_max_id, minTimestamp)
				  temp = api.LastJson

				  for item in temp["items"]:
				    
				    feed.append(item)

				  if temp["more_available"] is False:
				    
				    #print("entre si es falso")

				    has_more_feed = False
				  
				  else:
				  	
				    next_max_id = temp["next_max_id"]

				
				for obj in feed:
					media_id = obj['caption']['media_id']
					img_url = obj['image_versions2']['candidates'][0]['url']
					break

					
				#print("media_id: "+str(media_id))
				#print("img_url: "+str(img_url))

				#print("esta es la imagen: "+str(img2))
				#print(str(comentario))
				if (subir_foto['status']== 'ok'):
					Concursos(id_usuario = user_r,img_url=img_url,media_id=media_id, ruta_img = img, seguirnos =seguirme, like=like, hastags = hastag, seguir_otros=seguir_otros, cant_etiqueta = cant_etiqueta, like_amigo_otros = amigos_like_otros, seguirme_amigos=amigos_seguirme, seguir_amigos_otras = amigos_seguir_otros,condiciones = comentario, ganadores= ganadores, activo = 1).save()
					#print("esta es la imagen: "+str(img2))
					#print(str(comentario))
					#print("Despues de publicar: " +str(api.LastJson));
					api.logout()
						
					context = {'estado': 1}
				else:
					api.logout()
					context = {'estado': 0}
			
	return JsonResponse(context)


## validando el comentario para generar ganadores
def validar_hastags(media_hastags, comentario):
	tag_re = re.compile('#(\w+)')
	tag_media = tag_re.findall(media_hastags)
	tag_comentario = tag_re.findall(comentario)

	if (list(filter(lambda x: x in tag_media, tag_comentario)) == tag_media):

		#print("tag_media:" +str(tag_media))
		#print("tag_comentario: "+str(tag_comentario))

		return True
	else:
		return False

def validar_cant_etiquetas(cant_etiquetas, comentario):
	mencion_re = re.compile('@(\w+)')

	if (len(mencion_re.findall(comentario))==cant_etiquetas):
		##print("---> com en validar etiquetas: "+ comentario)
		return True
	else:
		return False


def validar_likes_media(com_username, likers):
	like_user = likers['users']
	like = True
	#print("desde el llamado: "+str(com_username))

	for like in like_user:
		
		if (like['username'] == com_username):
			like = True
			#print("valido : "+ str(com_username))
			break
		else:
			like=False

	return like

def validar_like_amigos_tag(comentario, likers):
	mencion_re = re.compile('@(\w+)')
	amigos_tag=mencion_re.findall(comentario)
	cont_likes = 0
	#print("---> amigos_tag: "+str(amigos_tag))

	like_user = likers['users']
	like_amigo=True
	for l in like_user:
		#print("likers : "+str(l['username']))
		if (list(filter(lambda x : x in str(l['username']),amigos_tag)) != []):
			#like_amigo=False
			#print("---> Lista []: " +str(list(filter(lambda x : x in l['username'],amigos_tag))))
			cont_likes+=1

	if (cont_likes == len(amigos_tag)):
		return True
	else:
		return False


def validar_comentarios(api,array_comentario, media):
	comentarios_validos = []
	api.getMediaLikers(media.media_id)
	likers = api.LastJson
	entra_like= True
	entra_hastag= True
	entra_etiqueta= True
	entra_like_amigo= True
	entra = True

	for com in array_comentario:
		com['media_id']=media.media_id
		
		if (media.like == 1):
			if(validar_likes_media(com['user']['username'], likers)):
				
				entra_like=True
			else:
				entra_like= False

		if (media.hastags != ""):
			if(validar_hastags(media.hastags,com['text'])):
				
				entra_hastag = True
			else:
				entra_hastag = False

		if (media.cant_etiqueta > 0):
			
			if(validar_cant_etiquetas(media.cant_etiqueta, com['text'])):
				entra_etiqueta= True
				
			else:
				entra_etiqueta= False

		if (media.like_amigo_otros == 1):
			
			if (validar_like_amigos_tag(com['text'], likers)):
				
				entra_like_amigo =  True
			else:
				entra_like_amigo =  True

		
		if (entra_like and entra_hastag and entra_etiqueta and entra_like_amigo):
			comentarios_validos.append(com)
		'''
		if (validar_hastags(media.hastags,com['text']) and validar_cant_etiquetas(media.cant_etiqueta, com['text'])):
			if(validar_likes_media(com['user']['username'], likers) and validar_like_amigos_tag(com['text'], likers)):
				comentarios_validos.append(com)
				#comentarios_validos.append({'media_id':media.media_id})
		'''

	#print(str(comentarios_validos))
	retorno = {
		'comentarios_validos': comentarios_validos,
		'cont_likers': likers['user_count']
	}
	return retorno

## Fin validando el comentario para generar ganadores



@login_required
def mis_concursos(request):
	todos_concursos = Concursos.objects.filter(id_usuario_id=request.user.id)
	
	imagenes = Imagenes.objects.filter(id_usuario_id=request.user.id)

	user_r= Usuarios.objects.get(email=request.user.email)
	username_insta = ""+user_r.user_insta+""
	
	api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
	api.login()
	
	comentarios=[]
	tiene = 0
	i =0 
	#print(str(api.username_id))
	#api.getSelfUserFollowers()
	#print("seguidores: "+str(api.LastJson))
	imagenes_count = imagenes.count()
	tam=len(todos_concursos)
	print(str(len(todos_concursos)))
	for c in todos_concursos:
		
		cont_comentario = 0
		cont_validos = 0
		cont_likers = 0
		imagen2 = []

		if (c.media_id != None):
			todos_comments=getTotalCommentsMedia(api,c.media_id)			
			cont_comentario = len(todos_comments)

			#api.getMediaComments(c.media_id)
			#cont_comentario = api.LastJson['comment_count']
			
			if (cont_comentario > 0):
				aux=validar_comentarios(api,todos_comments,c)
				validos = aux['comentarios_validos']
				cont_likers=aux['cont_likers']
				cont_validos = len(validos)
				#validos.append({'media_id':c.media_id})
			else:
				validos=[]

			for img in imagenes:
				if (c.media_id == img.media_id):
					imagen2.append(img.imagen)
		

		if (imagen2):
		
			comentarios.append({'imagen2':imagen2,'ruta_img': c.ruta_img, 'condiciones': c.condiciones, 'media_id': c.media_id,'cont_comentario': cont_comentario, 'cont_validos': cont_validos, 'validos': validos, 'activo': c.activo, 'cont_likers': cont_likers, 'publi_ganadores': c.publi_ganadores})
		else:
			comentarios.append({'imagen2':None,'ruta_img': c.ruta_img, 'condiciones': c.condiciones, 'media_id': c.media_id,'cont_comentario': cont_comentario, 'cont_validos': cont_validos, 'validos': validos, 'activo': c.activo, 'cont_likers': cont_likers, 'publi_ganadores': c.publi_ganadores})
		print("comentarios["+str(i)+"]['imagen2']"+str(comentarios[i]['imagen2']))
		i+=1
	
	## Esto esta por hacer ##
	#usuario = Info.objects.get(id_usuario_id=request.user.id)
	####
	info_user=get_save_info(None,request.user.id,user_r.user_insta, user_r.pass_insta)	

	usuario_info = {'foto_perfil': info_user.foto_perfil,'seguidos': info_user.seguidos, 'seguidores': info_user.seguidores,  'username': user_r.user_insta}
	#todos_comments=getTotalCommentsMedia(api,str(1660217691590099505))
	#print(str(todos_comments[0]['text']))
	context = {
		'usuario' : usuario_info,
		'comentarios': comentarios,
		'imagenes_count' : imagenes_count,
		'monto_total' : get_precio(request)
	}
	api.logout()
	return render (request,'mis_concursos.html', context)


@login_required
def delete_concurso(request):
	estado = 0
	if request.method == "POST":
		if request.is_ajax():
			media_id= request.POST.get('media_id')
			concurso = Concursos.objects.get(media_id=media_id)
			imganes = Imagenes.objects.filter(media_id=media_id)
			for img in imagenes:
				img.delete()

			if (concurso.delete()):
				estado = 1

			context ={
				'estado':estado
			}
			return JsonResponse(context)
	

@login_required
def generar_ganadores(request):

	if request.is_ajax():
		
		media_id = request.POST.get('media_id')
		despues = request.POST.get('despues')
		res=[]
		if (despues == '0'):

			user_r= Usuarios.objects.get(email=request.user.email)
			username_insta = ""+user_r.user_insta+""
			
			api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
			api.login()

			todos_concursos = Concursos.objects.filter(id_usuario_id=request.user.id, media_id = media_id)
			comentarios=[]
			res_username=""
			res_text=""
			
			no_gana = True

			for c in todos_concursos:
				cont_comentario = 0
				cont_validos = 0

				if (c.media_id != None):
					todos_comments=getTotalCommentsMedia(api,c.media_id)			
					cont_comentario = len(todos_comments)

					#api.getMediaComments(c.media_id)
					#cont_comentario = api.LastJson['comment_count']
					
					if (cont_comentario > 0):
						aux=validar_comentarios(api,todos_comments,c)
						validos = aux['comentarios_validos']
						cont_validos = len(validos)
						#validos.append({'media_id':c.media_id})
					else:
						validos=[]

					comentarios.append({'validos': validos})
				ganadores=c.ganadores

			for x in range(0,ganadores):
				
				## validar que el ganador no se repita
				i=random.randrange(len(validos))
				res_username=validos[i]['user']['username']
				res_text=validos[i]['text']

				if (x > 0):

					while no_gana:					
						for r in res:
							if (r['username'] != res_username):
								#print("entre si son distintos: "+str(r['username']))
								res.append({'username': res_username, 'text':res_text})
								no_gana = False
							else:
								#print("entre si son iguales: "+str(res_username))
								#print(" -->> A eliminar: "+str(validos[i]))
								del(validos[i])

						if (no_gana):

							i=random.randrange(len(validos))
							res_username=validos[i]['user']['username']
							res_text=validos[i]['text']
							#print(" -->> Nuevo a verificar: "+str(res_username))
				else:

					#print("-----> 1 primero agregado: " + str(res_username))
					res.append({'username': res_username, 'text':res_text})		

					#print(" -->> A eliminar abajo: "+str(validos[i]))
					del(validos[i])
			api.logout()
			context = {'res': res}
			return JsonResponse(context)
			#print(" -->> El 'X' va: "+str(x))

		else:
			ganadores = Ganadores.objects.filter(media_id = media_id)
			#print(str(media_id))
			for g in ganadores:
				res.append(g.username)
			#print(str(res))
			context = {'res': res}
	
			return JsonResponse(context)

@login_required
def guardar_ganadores(request):
	
	if request.method=="POST":
		
		if request.is_ajax():
			#user_r= Usuarios.objects.get(email=request.user.email)

			result_ganadores = request.POST.getlist('result_ganadores[]')

			#print(str(len(result_ganadores)))
			#print(str(result_ganadores))

			media_id = request.POST.get('media_id')

			concurso = Concursos.objects.filter(id_usuario_id=request.user.id, media_id = media_id)

			for c in concurso:
				#print(str(c.media_id))

				#print(str(c.id))

				for x in range(0,len(result_ganadores)):
					Ganadores(id_usuario_id=request.user.id, id_concurso=c.id, media_id=media_id,username=result_ganadores[x]).save()
					pass
				c.activo=0
				c.save()

	context ={'estado':1}
	return JsonResponse(context)


@login_required
def publicar_ganadores(request):
	if request.is_ajax():
		user_r= Usuarios.objects.get(email=request.user.email)
		username_insta = ""+user_r.user_insta+""
		
		api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
		api.login()
		media_id = request.POST.get('media_id')
		comentario = request.POST.get('comentario')

		concurso = Concursos.objects.filter(id_usuario_id=request.user.id, media_id = media_id)
		

		con = api.comment(media_id, comentario)
		if (con):

			for c in concurso:
				c.publi_ganadores = 1
				c.save()
			context={'estado':1}
		else:
			context={'estado':0}
	
	return JsonResponse(context)



def agregar_producto(request):

	if request.is_ajax():
		media_id = request.POST.get('media_id')
		#talla = request.POST.get('talla')
		#modelo = request.POST.get('modelo')
		cantidad = request.POST.get('cantidad')
		descripcion = request.POST.get('descripcion')
		res_auto = request.POST.get('res_automatica')
		result_img = request.POST.getlist('result_img[]')
		texto = request.POST.get('texto')

		estado = 1
		if (res_auto == "si"):
			res_automatica = 1
		else:
			res_automatica = 0

		print("respuesta automatica: "+str(res_automatica))

		if (Productos.objects.filter(id_usuario_id=request.user.id, media_id=media_id).exists()):

			producto = Productos.objects.filter(id_usuario_id=request.user.id, media_id=media_id)

			for p in producto:
				p.cantidad = cantidad
				p.descripcion_producto = descripcion
				p.res_automatica = res_automatica
				p.texto=texto
				p.save()
				estado =2


		else:
			Productos(id_usuario_id= request.user.id, media_id= media_id, cantidad=cantidad, texto=texto,descripcion_producto=descripcion, res_automatica=res_automatica).save()
			user_r= Usuarios.objects.get(email=request.user.email)

			for res in result_img:
				#print (res.split(',')[1])
				if not Imagenes.objects.filter(media_id= media_id, imagen=res.split(',')[1]).exists():
					Imagenes(id_usuario = user_r, media_id= media_id, imagen=res.split(',')[1]).save()
					#print("noe existe")
					#print(str(res.split(',')[1]))

		
		context= {'estado':estado}
		return JsonResponse(context)


def editar_producto(request):
	if request.method == "POST":
		if request.is_ajax():
			print("entre a editar_ producto")
			media_id = request.POST.get('media_id')
			cantidad = request.POST.get('cantidad')
			descripcion = request.POST.get('descripcion')
			res_auto = request.POST.get('res_automatica')
			talla = request.POST.get('talla')
			talla_id = request.POST.get('talla_id')
			modelo = request.POST.get('modelo')
			modelo_id = request.POST.get('modelo_id')

			estado = 0
			if (res_auto == "si"):
				res_automatica = 1
			else:
				res_automatica = 0

			producto = Productos.objects.filtre(id_usuario_id=request.user.id, media_id=media_id)


			for p in producto:
				if (talla_id == ""):
					tal = Tallas.objects.create(media_id=media_id, id_producto_id= p.id, id_usuario_id=request.user.id, nombre = talla)
					tal.save()
					talla_id = tal.id

				if (modelo_id == ""):
					mode = Modelos.objects.create(media_id=media_id, id_producto_id= p.id, id_usuario_id=request.user.id, nombre = modelo)
					mode.save()
					modelo_id = mode.id

				p.cantidad = cantidad
				p.descripcion_producto = descripcion
				p.res_automatica = res_automatica
				p.talla=talla_id
				p.modelo=modelo_id
				p.save()
				estado =1


			
		context= {'estado':estado}
		return JsonResponse(context)
def delete_producto(request):

	if request.is_ajax():
		estado =0
		media_id = request.POST.get('media_id')		
		pro = Productos.objects.get(media_id= media_id)
		imagenes = Imagenes.objects.filter(media_id=media_id)
		for img in imagenes:
			img.delete()

		if (pro.delete()):
			estado = 1

		context= {'estado':estado}
		return JsonResponse(context)

@login_required
def productos(request):
	product = Productos.objects.filter(id_usuario_id= request.user.id)
	imagenes = Imagenes.objects.filter(id_usuario_id=request.user.id)
	### Esto esta por HAcer ####
	#usuario = Info.objects.get(id_usuario_id=request.user.id)
	#####
	user_r= Usuarios.objects.get(email=request.user.email)
	username_insta = ""+user_r.user_insta+""
	
	info_user=get_save_info(None,request.user.id,user_r.user_insta, user_r.pass_insta)	

	usuario_info = {'foto_perfil': info_user.foto_perfil,'seguidos': info_user.seguidos, 'seguidores': info_user.seguidores,  'username': user_r.user_insta}
	
	arr_img = []
	products = []
	pausas = Pausas.objects.filter(id_usuario_id=request.user.id)
	play =False
	for pro in product:
		for p in pausas:
			if (p.media_id == pro.media_id):
				play = True
		for img in imagenes:
			if (img.media_id == pro.media_id):
				arr_img.append(img.imagen)

		products.append({'media_id':pro.media_id,'texto':pro.texto,'play':play,'descripcion':pro.descripcion_producto, 'talla': pro.talla, 'modelo': pro.modelo, 'cantidad': pro.cantidad, 'disponible':pro.disponible, 'res_automatica': pro.res_automatica, 'imagen':arr_img, 'cant_img': len(arr_img)})
		arr_img = []
	

	context = {
		'usuario' : usuario_info,
		'products':products,
		'monto_total' : get_precio(request)
	}
	return render (request,'productos.html', context)