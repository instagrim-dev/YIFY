#import.py

import yify, urllib2, transmissionrpc, logging, urllib, httplib, sqlite3, json


# logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# settings
LIMIT=50
SET=1
QUALITY="720p"

# get list of new releases
movies = yify.listMovies(quality=QUALITY)
# Count of total results that match the listMovies() query we sent
movieCount = movies['MovieCount']

# prepare to write to DB
conn = sqlite3.connect('yify.db')
c = conn.cursor()

#import all items in [movies] into yify.db
page = 1
for x in xrange(1, movieCount, LIMIT):	# ie. page in xrange(1, 2388, 50)
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
	#notify(MSG=MSG)

	page+=1
	movies = yify.listMovies(quality=QUALITY, set=page)
conn.commit()
conn.close()
