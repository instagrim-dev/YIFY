"""
Fetch new YIFY releases using API.py


Install Transmission RPC:
	pip install transmissionrpc
NOTES:
http://stackoverflow.com/questions/862173/how-to-download-a-file-using-python-in-a-smarter-way
http://pythonhosted.org/transmissionrpc/
http://docs.python.org/2/library/sqlite3.html
http://stackoverflow.com/questions/8250814/sqlite-autoincrement-how-to-insert-values
"""

import yify, urllib2, transmissionrpc, logging, urllib, httplib, sqlite3, json, time

# logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
# downloaddir
WATCH_DIR="/Users/apple/Desktop/"
# transmission
HOST=""
PORT=9091
USER=""
PASSWORD=""
# pushover
APP_TOKEN=""
USER_KEY=""
MSG="YIFY release downloaded"
# YIFY
QUALITY="720p"
RATING=0

def save(URL):
	global WATCH_DIR

	rfile = urllib2.urlopen(URL)
	try:
		rfilename = rfile.info()['Content-Disposition']	#attachment; filename="The_Butler_2013_1080p_BluRay_x264_YIFY_mp4.torrent"
		rfilename = rfilename.split("filename=")[1][1:-1]
	except KeyError:
		rfilename = URL.split('/')[-1]

	f = open(WATCH_DIR+rfilename, "wb")
	f.write(rfile.read())
	f.close()

def send(tc, hash):
	tc.add_torrent(hash)

def notify(URL=False, APP_TOKEN=APP_TOKEN, USER_KEY=USER_KEY, MSG=MSG):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
		urllib.urlencode({
			"token": APP_TOKEN,
			"user": USER_KEY,
			"message": MSG,
			"url": URL,
			"timestamp": int(time.time()),
		}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()

# Create transmissionClient obj (send) or update WATCH_DIR (save)
tc = transmissionrpc.Client(address=HOST, port=PORT, user=USER, password=PASSWORD)
# get list of new releases
movies = yify.listMovies(quality=QUALITY)

# Count of total results that match the listMovies() query we sent
movieCount = movies['MovieCount']

conn = sqlite3.connect('yify.db')
c = conn.cursor()

newlist = False
oldlist = []
for movie in movies['MovieList']:
	c.execute("select count(MovieID) from movies where MovieID = :id", {'id':movie['MovieID']})
	values = (movie['DateUploaded'], movie['DateUploadedEpoch'], movie['MovieID'], 
				movie['State'], movie['MovieUrl'], movie['MovieTitle'], movie['MovieYear'], 
				movie['Quality'], movie['ImdbCode'], movie['TorrentUrl'], movie['TorrentHash'], 
				movie['TorrentMagnetUrl'])
	if 0 == c.fetchone()[0]:
		newlist = []
		newlist.append(movie['MovieTitle'].encode('ascii','ignore'))
		# record release
		c.execute('''
			INSERT INTO movies(
				DateUploaded, DateUploadedEpoch, MovieID, State, 
				MovieUrl, MovieTitle, MovieYear, Quality, 
				ImdbCode, TorrentUrl, TorrentHash, TorrentMagnetUrl
				) 
			VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', values)
		# send/save release
		#send(tc, movie['TorrentMagnetUrl'])
	else:
		oldlist.append(movie['MovieTitle'].encode('ascii','ignore'))

logging.info("New releases: %i" % (len(newlist) if newlist else 0))
logging.debug("New releases:\n%s" % newlist)
logging.info("Old releases: %i" % len(oldlist))
logging.debug("Old releases:\n%s" % oldlist)
if newlist:
	MSG = "Fetched:"
	for x in newlist:
		MSG += "\n%s" % x
else:
	MSG = "Nothing new released toady"
logging.info("Pushover MSG parameter: %s" % MSG)
notify(MSG=MSG)

conn.commit()
conn.close()