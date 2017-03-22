ALTER DATABASE youtubeProjectDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
ALTER TABLE youtubeProjectDB.search_api CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# The lines above deal with all the weird and wacky emojis in youtube metadata
# otherwise the python loading script crashes as soon as it hits one.
# http://stackoverflow.com/questions/34305587/uploading-python-pandas-dataframe-to-mysql-internalerror-1366-incorrect-str

CREATE TABLE search_api(
    videoTitle VARCHAR(150) NOT NULL,
	channelTitle VARCHAR(255) NOT NULL,
	videoId VARCHAR(15) NOT NULL,
	description VARCHAR(255),
	publishedAt DATETIME,
	queriedAt DECIMAL(22,9),
	kind VARCHAR(40),
	etag VARCHAR(70),
	regionCode VARCHAR(2),
	items_etag VARCHAR(70),
	channelId VARCHAR(30),
	query_q VARCHAR(50), 
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
 );

