


CREATE TABLE youtubeProjectDB.statistics(
	videoId VARCHAR(15) NOT NULL,
	viewCount INT,
	likeCount INT,
	dislikeCount INT,
	favoriteCount INT,
	commentCount INT,
	duration VARCHAR(20),
	durationSeconds INT,
	dimension VARCHAR(5),
	definition VARCHAR(5),
	caption VARCHAR(8),
	licensedContent VARCHAR(8), # don't trust Bools in PyMySQL /MySQL
	projection VARCHAR(15),
	relevantTopicIDs VARCHAR(150),   # 30 was not enough
	topicCategories VARCHAR(500),
	kind VARCHAR(50),
	etag VARCHAR(100),    
	queriedAt VARCHAR(30),
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
 );

ALTER TABLE youtubeProjectDB.statistics CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Once completed : 
SELECT * FROM statistics A INNER JOIN (SELECT * FROM search_api) B ON A.videoId = B.videoId;
