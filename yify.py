"""
YIFY API

This is a lightweight web service, (REST interface), which provides an easy way to access the YIFY-Torrents website.
An API (Application programming interface) is a protocol intended to be used as an interface by software components to communicate with each other.
Our API supports many methods, so there should not be a problem coding some nice applications.
-JSON
-XML
http://yify-torrents.com/api/API_METHOD.json
http://yify-torrents.com/api/API_METHOD.jsonp
http://yify-torrents.com/api/API_METHOD.xml
-
Notes:
http://stackoverflow.com/questions/5384914/deleting-items-from-a-dictionary-while-iterating-over-it
"""
import logging, urllib2, json, urllib

SSL="http"		#|https
HOST="yify-torrents.com"
API_ROOT=HOST + '/api/'
FORMAT=".json?"	#|.xml?|.jsonp?

def API_CALL(method, type, param=None):
	global SSL
	global API_ROOT
	global FORMAT

	params=None
	API_URL = "%s://%s%s%s" % (SSL,API_ROOT,method,FORMAT)

	if type=='POST':
		params = urllib.urlencode(param)
		print params
	else:
		API_URL += urllib.urlencode(param)
		logging.info("API URL: %s" % API_URL)

	request = urllib2.Request(API_URL,params)
	data = json.load(urllib2.urlopen(request))
	return data

def getUpcoming():
	"""
	Upcoming movies

	http://yify-torrents.com/api/upcoming.json
	http://yify-torrents.com/api/upcoming.xml
	-
	Using this function you can make a GET request
	to the API and get a list of all the upcoming
	movies
	-
	returns:
	MovieTitle, MovieCover, ImdbCode, ImdbLink, Uploader,
	UploaderUID, DateAdded, DateAddedEpoch
	-
	Possible Error Responses
	No upcoming movies
	"""
	return API_CALL('upcoming', type='GET')

def listMovies(limit=20, set=1, quality='ALL', 
		rating=0, keywords="", genre='ALL',
		sort='date', order='desc'):
	"""
	List movies

	http://yify-torrents.com/api/list.json
	http://yify-torrents.com/api/list.jsonp
	http://yify-torrents.com/api/list.xml
	Using this function you can make a GET request 
	to the API and get a list of movies, this function 
	can be used as search and or filter. It will return 
	the amount of results and also an array of the
	films named 'MovieList'
	-
	returns:
	MovieCount, MovieID, State, MovieUrl, MovieTitle,
	MovieTitleClean, MovieYear, DateUploaded, DateUploadedEpoch,
	Quality, CoverImage, ImdbCode, ImdbLink, Size, SizeByte,
	MovieRating, Genre, Uploader, UploaderUID, TorrentSeeds, Downloaded,
	TorrentPeers, TorrentUrl, TorrentHash, TorrentMagnetUrl
	-
	Possible Error Responses
	"""
	param={'limit':limit, 'set':set, 'quality':quality,
			'rating':0, 'keywords':keywords, 'genre':'ALL',
				'sort':'date', 'order':'desc'}
	return API_CALL('list','GET', param)

def getMovieDetails(id):
	"""
	Movies Details

	Using this function you can make a GET request 
	to the API with the unique ID of the movie 
	and get all information relating to it
	"""
	param = {'id':id}
	return API_CALL('movie', 'GET', param)

def getMovieComments(movieid):
	"""
	Movie Comments

	Using this function you can make a GET request 
	to the API with the unique ID of the movie and 
	get all the comments made on that specific film
	"""
	param = {'id':id}
	return API_CALL('comments', 'GET', param)

def getUserDetails(id):
	"""
	User Details

	Using this function you can make a GET request 
	to the API with the unique ID of the user and 
	get all the details about them
	"""
	param = {'id':id}
	return API_CALL('user', 'GET', param)

def register(username, password, email):
	"""
	Register

	Using this simple API you can post data and 
	register a new account. (An email verification 
	notice will still be sent and need to be activated 
	before account is fully functional)
	"""
	param = {'username':username, 'password':password, 'email':email}
	return API_CALL('register', 'POST', param)

def registerVerification(code):
	"""
	Register verification

	"""
	param = {'code':code}
	return API_CALL('registerconfirm', 'POST', param)

def login(username, password):
	"""
	Login

	"""
	param = {'username':username, 'password':password}
	return API_CALL('login', 'POST', param)

def recoverPassword(email):
	"""
	Password Recovery

	"""
	param = {'email':email}
	return API_CALL('sendresetpass', 'POST', param)

def getProfileDetails(hash):
	"""
	Profile Details

	"""
	param = {'hash':hash}
	return API_CALL('profile', 'GET', param)

def resetPassword(code, newpassword):
	"""
	Resetting Password
	"""
	param = {'code':code, 'newpassword':newpassword}
	return API_CALL('resetpassconfirm', 'POST', param)

def postComment(hash, text, movieid, replyid=""):
	"""
	"""
	param = {'hash':hash, 'replyid':replyid, 'text':text, 'movieid':movieid}
	return API_CALL('commentpost', 'POST', param)

def editUserProfile(hash, active="", about="", newpassword="", oldpassword="", avatar=""):
	"""
	"""
	param = {'hash':hash, 'active':active, 'about':about, 'newpassword':newpassword, 'oldpassword':oldpassword, 'avatar':avatar}
	return API_CALL('editprofile', 'POST', param)

def getRequestList(page, limit=20, set=1, sort='votes', order='desc'):
	"""
	Request List

	Using this function you can make a GET request 
	to the API and get a list of all the current 
	requests and information about them. It will 
	return the amount of results and also an array 
	of the films named 'RequestList'
	-
	@param page, 
	@param limit,
	@param set,
	@param sort,
	@param order,
	"""
	param = {'page':page, 'limit':limit, 'set':set, 'sort':sort, 'order':order}
	return API_CALL('requests', 'GET', param)

def makeRequest(hash, request):
	"""
	Making Requests

	Using this function you can make a POST request 
	to the API with the user hash and request for a movie
	-
	@param hash, unique user hash used to identify the user
	@param request, Movie name or IMDB Code or IMDB URL
	returns status
	-
	Possible Error Responses:
	Missing 'hash' parameter
	wrong user hash
	You dont have any requests left
	Movie has already been uploaded, MovieID: XXXX
	This movie has already been confirmed
	Movie has already been requested, we have noted that you have requested this movie.
	You have alread requested this movie
	Could not find movie
	missing 'request' parameter
	Needs to be a POST request
	"""
	param = {'hash':hash, 'request':request}
	return API_CALL('makerequest', 'POST', param)

def makeRequestVote(hash, requestid):
	"""
	Request Voting

	Using this function you can make a POST request 
	to the API with the user hash and requestID 
	to vote on a request
	-
	@param hash, uinque user hash used to ident. user
	@param requestid, request ID you wish to vote on
	returns status, the status of this vote submission
	-
	Possible Error Responses:
	Missing 'hash' parameter
	wrong user hash
	You dont have any votes left
	Cant vote on a 'Confirmed' Requests
	Cant vote on a 'Declined' Requests
	Cant vote on a 'Pending' Requests
	Could not find the requested movie
	missing 'requestid' parameter
	Needs to be a POST request
	"""
	param = {'hash':hash, 'requestid':requestid}
	return API_CALL('vote', 'POST', param)