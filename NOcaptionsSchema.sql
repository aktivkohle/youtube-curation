
# start keeping track of videoIds where youtube-dl FAILED to pull

CREATE TABLE youtubeProjectDB.NOcaptions(
	videoId VARCHAR(15) NOT NULL,
	queriedAt VARCHAR(30),
	errorMessage VARCHAR(500),	
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
 );

ALTER TABLE youtubeProjectDB.NOcaptions CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Oh no! 1 April 2017
# DataError: (1406, "Data too long for column 'errorMessage' at row 1")
ALTER TABLE youtubeProjectDB.NOcaptions MODIFY errorMessage VARCHAR(5000);
