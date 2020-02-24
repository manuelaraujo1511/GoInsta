from InstagramAPI import InstagramAPI

api = InstagramAPI("jgcr7", "jgrc*2020")
if (api.login()):
    # api.getSelfUserFeed()  # get self user feed
    # print(api.LastJson)  # print last response JSON
    # print("Login succes!")
    api.getMediaComments("2250560355398705716_30393527811")
    print(api.LastJson)  # print last response JSON
else:
    print("Can't login!")