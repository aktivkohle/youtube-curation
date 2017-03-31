CREATE TABLE youtubeProjectDB.captions(
	videoId VARCHAR(15) NOT NULL,
	captionsText TEXT,
	captionsFile TEXT,
	language VARCHAR(5),
	captionsFileFormat VARCHAR(5),
	queryMethod VARCHAR(150), 
	queriedAt VARCHAR(30),
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
 );

ALTER TABLE youtubeProjectDB.captions CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# DataError: (1406, "Data too long for column 'captionsXML' at row 1")
# Kind of error message you want
# No..
# Was generated by https://www.youtube.com/watch?v=XZOUPnH4aN0
# Which is just full of spam!