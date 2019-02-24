#from instagram import InstagramAPI
#from InstagramAPI import *
#insta = Instagram('manuel_araujo10', 'candyELEANA1511');


'''
Solicitar el Access Token: 
https://www.instagram.com/oauth/authorize/?client_id=f08be66585a84324a8c0984dded9926d&redirect_uri=http://127.0.0.1:8000&response_type=token&scope=public_content

GET info user https://api.instagram.com/v1/users/search?q=manuel_araujo10&client_id=f08be66585a84324a8c0984dded9926d&access_token=299520449.f08be66.95491da1db834c2b82e167c3a1ea9fa2

'''
'''
access_token = "299520449.f08be66.95491da1db834c2b82e167c3a1ea9fa2"
client_id="f08be66585a84324a8c0984dded9926d"
client_secret = "8f7865cca64e45e698844308b7cad569"
'''

#api = InstagramAPI(access_token=access_token, client_secret=client_secret)
##api = InstagramAPI(client_id=client_id, client_secret=client_secret)
'''
popular_media = api.media_popular(count=20)

for media in popular_media:
	print (media.images['standard_resolution'].url)
'''
#sr = api.user_search('manuel_araujo10')

#print (sr[0].username)


import InstagramAPI

# /////// CONFIG ///////
username = 'manuel_araujo10'
password = 'candyELEANA1511'
debug = False

photo = '/home/manuel/Imágenes/1508515_10208313985264193_7717266571076596964_n.jpg'  # path to the photo
caption = 'quiero  una de estas #Pendiente'  # caption
# //////////////////////

i = InstagramAPI.Instagram(username, password, debug)

try:
	i.login()
except Exception as e:
	e.message
	exit()

try:
	i.uploadPhoto(photo, caption)
except Exception as e:
	print (e.message)
