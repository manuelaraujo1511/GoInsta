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
	if Ventas.objects.filter(id_usuario_id=request.user.id).exists():
		ventas = Ventas.objects.filter(id_usuario_id=request.user.id)
		for v in ventas:
			precio +=  (int(v.precio)*int(v.cantidad))

	
	return precio

def resize_image(input_image_path,output_image_path,size):
	
	original_image = Image.open(input_image_path)
	
	width, height = original_image.size
	
	print('The original image size is {wide} wide x {height} ' 'high'.format(wide=width, height=height))
	
	resized_image = original_image.resize(size)
	
	width, height = resized_image.size
	
	print('The resized image size is {wide} wide x {height} ''high'.format(wide=width, height=height))
	
	resized_image.show()
	
	resized_image.save(output_image_path)



#@login_required
def index(request):
	# IMPORTANTE: comprobar conexion a internet
	print("----------")	
	print(request.user)	
	user_r= Usuarios.objects.get(email=request.user.email)
	username_insta = ""+user_r.user_insta+""

	api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
	api.login()
	
	has_more_feed = True
	feed = []
	feed_res = []	
	next_max_id = ''
	usernameId = api.username_id
	minTimestamp=None
	guardo=True

	######  CAMBIAR ESTO  ######
	'''
	if not Info.objects.filter(id_usuario_id=request.user.id).exists():
		print("entre si no existe el perfil de usuario")
		api.searchUsername(str(username_insta))
		img_profile = api.LastJson['user']['profile_pic_url']
		media_count = api.LastJson['user']['media_count']
		follower = api.LastJson['user']['follower_count']
		following = api.LastJson['user']['following_count']
		tags = api.LastJson['user']['usertags_count']
		
		Info(id_usuario_id=request.user.id, username=username_insta, seguidores=follower, seguidos=following, fotos=media_count, foto_perfil= img_profile , hastags=tags).save()

		usuario_info = Info.objects.get(id_usuario_id=request.user.id)
	else:
	'''
	api.searchUsername(str(username_insta))
	img_profile = api.LastJson['user']['profile_pic_url']
	media_count = api.LastJson['user']['media_count']
	follower = api.LastJson['user']['follower_count']
	following = api.LastJson['user']['following_count']
	tags = api.LastJson['user']['usertags_count']

	#usuario_info = Info.objects.get(id_usuario_id=request.user.id)
	#for u in usuario_info:
	usuario_info = {'foto_perfil': img_profile,'fotos': media_count, 'seguidos': following, 'seguidores': follower, 'hastags':tags , 'username': username_insta}
	'''
	usuario_info['foto_perfil']= img_profile
	usuario_info['fotos']=media_count
	usuario_info['seguidos']= following
	usuario_info['seguidores']= follower
	usuario_info['hastags'] = tags
	'''
	#usuario_info.save()


		#usuario = Info.objects.filter(id_usuario_id=request.user.id)
		

		
	

	#api.getTotalUserFeed(api.username_id)
	#todos_concursos = []
	todos_concursos = Concursos.objects.filter(id_usuario_id=request.user.id)

	if (todos_concursos.exists()):		

		while has_more_feed:

		  api.getUserFeed(usernameId, next_max_id, minTimestamp)
		  temp = api.LastJson

		  for item in temp["items"]:
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
		  	feed.append(item)

		  if temp["more_available"] is False:
		    
		    print("entre si es falso")

		    has_more_feed = False
		  
		  else:
		  	next_max_id = temp["next_max_id"]

	context = {
		'usuario' : usuario_info,
		'feed' : feed,
		'monto_total' : get_precio(request)

	}
	print(feed)
	
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
		#print (email, password)
		user_u = Usuarios.objects.get(email=email)
		#print(user_u.user_insta)
		try:
			user_u = Usuarios.objects.get(email=email)
			user_name=user_u.username

			if user_u.user_insta is not None:
				if user_name is not False:
					#print (user_name)
					#print (password)
					user = authenticate(request, username=user_name, password=password)
					login(request, user)
					#print(user)
					if user is not None:
						
							

						# api = InstagramAPI(user_u.user_insta, user_u.pass_insta)
						# if api.login():
							
						# 	#login(request, user)
						# 	#messages.success(request, 'Bienvenido ' + request.user.first_name + ' '+request.user.last_name)
						# 	api.logout()
						print("REDIRECT")
						return redirect('admingo:index')
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

			u = Usuarios(nombre=nombre, apellido=apellido, email=email,password=password,username=username,fin_registro=0,cambiar_pass_insta=0)
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

		

		api = InstagramAPI(cuenta, password_i)


		if api.login():
			Usuarios.objects.filter(username=username).update(user_insta=cuenta, pass_insta=password_i)
			user = authenticate(request, username=username, password=password)

			login(request, user)
			print(request.user)
			messages.success(request, 'Bienvenido ' + request.user.first_name + ' ' + request.user.first_name)
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


			#Ventas(id_usuario = user_r, media_id = media_id, cantidad = cantidad, varias=varias, precio = precio, nombre_cliente=nombre_cliente, telefono_cliente = telefono_cliente, descripcion_venta = descripcion_venta).save()
			if (Productos.objects.filter(id_usuario_id = request.user.id, media_id = media_id).exists()):

				producto = Productos.objects.get(id_usuario_id = request.user.id, media_id = media_id)

				#for pro in producto:
				#print("producto.cantidad: "+ str(int(producto.cantidad))+" - cantidad: "+str(cantidad)+" = "+str(int(producto.cantidad) - int(cantidad)))
				producto.cantidad = int(producto.cantidad) - int(cantidad)
				producto.save()
					
				Ventas(id_usuario = user_r, id_producto_id=producto.id, media_id = media_id, cantidad = cantidad, varias=varias, precio = precio, nombre_cliente=nombre_cliente, telefono_cliente = telefono_cliente, descripcion_venta = descripcion_venta).save()
				print("producto.id: "+ str(producto.id))
			else:
				print("sino")
				
				Productos(id_usuario = user_r, media_id=media_id, texto=texto, descripcion_producto=descripcion_venta).save()

				producto = Productos.objects.get(id_usuario_id = request.user.id, media_id = media_id)

				Ventas(id_usuario = user_r, id_producto_id=producto.id, media_id = media_id, cantidad = cantidad, varias=varias, precio = precio, nombre_cliente=nombre_cliente, telefono_cliente = telefono_cliente, descripcion_venta = descripcion_venta).save()
			#for para el array de rult_img#
			'''
			ventas = Ventas.objects.all()
			for ven in ventas:
				print(ven.id_usuario)
			'''
			#print("tamaño: "+ str(len(result_img)))
			for res in result_img:
				#print (res.split(',')[1])
				if not Imagenes.objects.filter(media_id= media_id, imagen=res.split(',')[1]).exists():
					Imagenes(id_usuario = user_r, media_id= media_id, imagen=res.split(',')[1]).save()


			context = {'estado': 1}
	return JsonResponse(context)

@login_required
def pausar_venta(request):
	if request.method == "POST":
		print ("entre a pausar Venta POST")
		user_r= Usuarios.objects.get(email=request.user.email)
		username_insta = ""+user_r.user_insta+""

		api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
		api.login()

		if request.is_ajax():
			texto = request.POST.get('texto')
			media_id = request.POST.get('media_id')
			api.editMedia(media_id, ""+texto+"")

			api.logout()
			context = {'estado': 1}
	return JsonResponse(context)

@login_required
def ventas (request):

	todas_ventas = Ventas.objects.filter(id_usuario_id=request.user.id)
	imagenes = Imagenes.objects.filter(id_usuario_id=request.user.id)
	## Esto esta por Hacer ##
	##usuario = Info.objects.get(id_usuario_id=request.user.id)
	###
	user_r= Usuarios.objects.get(email=request.user.email)
	username_insta = ""+user_r.user_insta+""

	api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
	api.login()
	api.searchUsername(str(username_insta))
	img_profile = api.LastJson['user']['profile_pic_url']
	media_count = api.LastJson['user']['media_count']
	follower = api.LastJson['user']['follower_count']
	following = api.LastJson['user']['following_count']
	tags = api.LastJson['user']['usertags_count']
	usuario = {'foto_perfil': img_profile,'fotos': media_count, 'seguidos': following, 'seguidores': follower, 'hastags':tags, 'username': username_insta }

	arr_img = []
	arr_ventas = []
	for v in todas_ventas:
		for img in imagenes:
			if (img.media_id == v.media_id):
				arr_img.append(img.imagen)

		arr_ventas.append({'media_id': v.media_id, 'nombre_cliente': v.nombre_cliente, 'telefono_cliente': v.telefono_cliente,'precio': v.precio, 'precio_total':(int(v.cantidad)*v.precio),'descripcion_venta':v.descripcion_venta, 'cantidad': v.cantidad, 'imagen': arr_img, 'cant_img': len(arr_img)})

		arr_img = []

	context = {
		'usuario' : usuario,
		'todas_ventas': arr_ventas,
		'monto_total' : get_precio(request)
	}
	api.logout()

	return render (request,'ventas.html', context)

def upload_img(request):
	ruta_original=os.getcwd()
	#print ("ruta actual "+ str(os.getcwd()))
	#os.chdir(os.getcwd()+"/admingo/static/img")
	#print ("ruta cambio "+ str(os.getcwd()))
	
	# Creo carpeta
	#os.mkdir(os.getcwd()+"/admingo/static/img/usuario-"+str(request.user.id)+"/")

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
def nuevo_concurso (request):
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
		print("---"*20)
		print(media_info)

		if (media_info["items"][0]["media_type"] == 1):
			print("media_info[media_type] == 1")
			comentario=media_info["items"][0]["caption"]["text"]
			img_url=media_info["items"][0]["image_versions2"]["candidates"][0]["url"]

			## para determinar los hastags del comentario
			tag_re = re.compile('#(\w+)')
			lista_hastag = tag_re.findall(comentario)
			for c in lista_hastag:
				hastag+= " #"+c+" "

			print(str(hastag))
			
			Imagenes(id_usuario = user_r,media_id=media_id, imagen=img_url).save()

			Concursos(id_usuario = user_r,img_url=img_url,media_id=media_id,hastags = hastag,  seguir_otros= "",condiciones = comentario, view_otro = 1).save()
		else:
			
			print("media_info[media_type] == 8")
			arra_img=[]
			for img in media_info["items"][0]["carousel_media"]:
				#arra_img.append(img["image_versions2"]["candidates"][0]['url'])
				Imagenes(id_usuario = user_r,media_id=media_id, imagen=img["image_versions2"]["candidates"][0]['url']).save()


			comentario=media_info["items"][0]["caption"]["text"]
			## para determinar los hastags del comentario
			tag_re = re.compile('#(\w+)')
			lista_hastag = tag_re.findall(comentario)
			for c in lista_hastag:
				hastag+= " #"+c+" "

			Concursos(id_usuario = user_r,img_url="",media_id=media_id,hastags = hastag, seguir_otros= "",condiciones = comentario, view_otro = 1).save()

		#print("imagen : "+str(imagen))

		#print("si es ajax nuevo concurso")
		#usuario = Info.objects.get(id_usuario_id=request.user.id)
		#print ("Usuario INFO: "+str(usuario))

		context = {
			#'usuario' : usuario,		
			#'monto_total' : get_precio(request),
			'estado' : request.user.id
		}
		api.logout()
		#return render (request,'nuevo_concurso.html', context)

		return JsonResponse(context)
	else:
		concursos = None
		imagenes_count = "0"
		imagenes=None
		if Concursos.objects.filter(id_usuario_id=request.user.id, view_otro = 1).exists():
			concursos = Concursos.objects.filter(id_usuario_id=request.user.id, view_otro = 1)
			for c in concursos:
				imagenes = Imagenes.objects.filter(id_usuario_id=request.user.id, media_id = c.media_id)
			
			imagenes_count = imagenes.count()

			print("imagenes_count: "+ str(imagenes_count))
			## Esto esta por hacer ###
			##usuario = Info.objects.get(id_usuario_id=request.user.id)
			###

		user_r= Usuarios.objects.get(email=request.user.email)
		username_insta = ""+user_r.user_insta+""

		api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
		api.login()
		api.searchUsername(str(username_insta))
		img_profile = api.LastJson['user']['profile_pic_url']
		media_count = api.LastJson['user']['media_count']
		follower = api.LastJson['user']['follower_count']
		following = api.LastJson['user']['following_count']
		tags = api.LastJson['user']['usertags_count']
		usuario = {'foto_perfil': img_profile,'fotos': media_count, 'seguidos': following, 'seguidores': follower, 'hastags':tags , 'username' : username_insta}
			
		context = {
				'usuario' : usuario,
				'concursos': concursos,
				'imagenes' : imagenes 	,
				'imagenes_count': str(imagenes_count),
				'monto_total' : get_precio(request)
			}
		api.logout()
		print("concursos: "+str(concursos))
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
	api.searchUsername(str(username_insta))
	img_profile = api.LastJson['user']['profile_pic_url']
	media_count = api.LastJson['user']['media_count']
	follower = api.LastJson['user']['follower_count']
	following = api.LastJson['user']['following_count']
	tags = api.LastJson['user']['usertags_count']
	usuario = {'foto_perfil': img_profile,'fotos': media_count, 'seguidos': following, 'seguidores': follower, 'hastags':tags, 'username' : username_insta }
	#todos_comments=getTotalCommentsMedia(api,str(1660217691590099505))
	#print(str(todos_comments[0]['text']))
	context = {
		'usuario' : usuario,
		'comentarios': comentarios,
		'imagenes_count' : imagenes_count,
		'monto_total' : get_precio(request)
	}
	api.logout()
	return render (request,'mis_concursos.html', context)


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



def editar_producto(request):

	if request.is_ajax():
		media_id = request.POST.get('media_id')
		talla = request.POST.get('talla')
		modelo = request.POST.get('modelo')
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
				p.talla = talla
				p.modelo = modelo
				p.cantidad = cantidad
				p.descripcion_producto = descripcion
				p.res_automatica = res_automatica
				p.texto=texto
				p.save()
				estado =2


		else:
			Productos(id_usuario_id= request.user.id, media_id= media_id, talla=talla, modelo=modelo, cantidad=cantidad, texto=texto,descripcion_producto=descripcion, res_automatica=res_automatica).save()
			user_r= Usuarios.objects.get(email=request.user.email)

			for res in result_img:
				#print (res.split(',')[1])
				if not Imagenes.objects.filter(media_id= media_id, imagen=res.split(',')[1]).exists():
					Imagenes(id_usuario = user_r, media_id= media_id, imagen=res.split(',')[1]).save()
					#print("noe existe")
					#print(str(res.split(',')[1]))

		
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
	
	api= InstagramAPI(user_r.user_insta, user_r.pass_insta)
	api.login()
	api.searchUsername(str(username_insta))
	img_profile = api.LastJson['user']['profile_pic_url']
	media_count = api.LastJson['user']['media_count']
	follower = api.LastJson['user']['follower_count']
	following = api.LastJson['user']['following_count']
	tags = api.LastJson['user']['usertags_count']
	usuario = {'foto_perfil': img_profile,'fotos': media_count, 'seguidos': following, 'seguidores': follower, 'hastags':tags, 'username' : username_insta }
	
	
	arr_img = []
	products = []

	for pro in product:
		for img in imagenes:
			if (img.media_id == pro.media_id):
				arr_img.append(img.imagen)

		products.append({'media_id':pro.media_id,'texto':pro.texto,'descripcion':pro.descripcion_producto, 'talla': pro.talla, 'modelo': pro.modelo, 'cantidad': pro.cantidad, 'disponible':pro.disponible, 'res_automatica': pro.res_automatica, 'imagen':arr_img, 'cant_img': len(arr_img)})
		arr_img = []

	context = {
		'usuario' : usuario,
		'products':products,
		'monto_total' : get_precio(request)
	}
	api.logout()
	return render (request,'productos.html', context)