CREATE TABLE youtubeProjectDB.captions(
	videoId VARCHAR(15) NOT NULL,
	captionsText MEDIUMTEXT,
	wordCount INT,
	captionsFile MEDIUMTEXT,
	language VARCHAR(15),
	captionsFileFormat VARCHAR(5),
	queryMethod VARCHAR(150), 
	queriedAt VARCHAR(30),
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
 );

ALTER TABLE youtubeProjectDB.captions CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
