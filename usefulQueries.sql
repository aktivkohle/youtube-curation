USE youtubeProjectDB;

SELECT DISTINCT(videoId) FROM search_api WHERE videoID NOT IN (SELECT * FROM captions WHERE queryMethod != 'http://video.google.com/timedtext');

SELECT videoId, COUNT(videoId) FROM youtubeProjectDB.captions WHERE queryMethod="youtube-dl" GROUP BY videoId ORDER BY COUNT(videoId) DESC;

# the video with the most different languages! 
SELECT * FROM youtubeProjectDB.captions WHERE videoId = 'DEZycYWIJf4';

SELECT * FROM youtubeProjectDB.statistics WHERE videoId = 'DEZycYWIJf4';

SELECT * FROM youtubeProjectDB.captions WHERE queryMethod != 'http://video.google.com/timedtext';

SELECT COUNT(*) FROM youtubeProjectDB.search_api; # 2525

SELECT COUNT(*) FROM youtubeProjectDB.search_api WHERE query_q = 'dog+training';  # 2525

SELECT COUNT(*) FROM youtubeProjectDB.search_api WHERE query_q != 'dog+training';   # 0

SELECT COUNT(videoId) FROM youtubeProjectDB.search_api; # 2525    ()

SELECT COUNT(DISTINCT(videoId)) FROM youtubeProjectDB.search_api;   # 1248

SELECT * FROM youtubeProjectDB.search_api WHERE queriedAt LIKE '%29 March 2017%';

SELECT COUNT(videoId) FROM youtubeProjectDB.search_api WHERE queriedAt LIKE '%29 March 2017%' AND query_q = "machine+learning";

SELECT COUNT(DISTINCT(videoId)) FROM youtubeProjectDB.search_api WHERE queriedAt LIKE '%29 March 2017%' AND query_q = "machine+learning";

# first half of 2016 Jan - June pulled 442 (unique) videos on machine+learning
# second half of 2016 July - Dec yielded 629 - 442 = 227

SELECT COUNT(*) FROM youtubeProjectDB.statistics;
# 1243 at 18:02 Uhr
# 2059 at 18:09 Uhr

SELECT query_q, COUNT(query_q) FROM youtubeProjectDB.search_api GROUP BY query_q;

SELECT caption, COUNT(caption) FROM youtubeProjectDB.statistics GROUP BY caption;

SELECT  search_api.videoId, videoTitle, caption, duration, durationSeconds, channelTitle FROM search_api
INNER JOIN statistics
ON search_api.videoId = statistics.videoId
#WHERE query_q='scikit'
ORDER BY durationSeconds ASC;

SELECT COUNT(videoId) FROM statistics WHERE durationSeconds = 0;   # 189
SELECT COUNT(DISTINCT(videoId)) FROM statistics WHERE durationSeconds = 0;  # 189


SELECT topicCategories, count(topicCategories) FROM statistics GROUP BY topicCategories ORDER BY count(topicCategories) DESC;

SELECT videoId, viewCount, likeCount, dislikeCount, commentCount, durationSeconds FROM statistics;

SELECT videoId, captionsText FROM captions;

# http://stackoverflow.com/questions/748276/using-sql-to-determine-word-count-stats-of-a-text-field

DELIMITER $$
CREATE FUNCTION wordcount(str TEXT)
       RETURNS INT
       DETERMINISTIC
       SQL SECURITY INVOKER
       NO SQL
  BEGIN
    DECLARE wordCnt, idx, maxIdx INT DEFAULT 0;
    DECLARE currChar, prevChar BOOL DEFAULT 0;
    SET maxIdx=char_length(str);
    WHILE idx < maxIdx DO
        SET currChar=SUBSTRING(str, idx, 1) RLIKE '[[:alnum:]]';
        IF NOT prevChar AND currChar THEN
            SET wordCnt=wordCnt+1;
        END IF;
        SET prevChar=currChar;
        SET idx=idx+1;
    END WHILE;
    RETURN wordCnt;
  END
$$
DELIMITER ;

# (takes too long like they say on stackoverflow) - use a python script instead

SELECT videoId, captionsText, wordcount(captionsText) AS 'wordcount' FROM captions;

SELECT queryMethod, COUNT(queryMethod) FROM captions GROUP BY queryMethod;

SELECT language, COUNT(language) FROM captions GROUP BY language ORDER BY count(language) DESC;
# pt-BR, 500 Brazillian portuguese

SELECT language, COUNT(language) FROM captions WHERE language LIKE '%en%' GROUP BY language ORDER BY count(language) DESC;
# en-IE irish English
# language, COUNT(language)

SELECT query_q, COUNT(query_q) FROM search_api GROUP BY query_q ORDER BY COUNT(query_q) DESC;

SELECT videoId from search_api WHERE query_q = 'machine+learning' OR query_q = 'scikit';

SELECT language, COUNT(language) FROM captions WHERE language LIKE '%en%' 
AND videoId IN (SELECT videoId from search_api WHERE query_q = 'machine+learning' OR query_q = 'scikit')  
GROUP BY language 
ORDER BY count(language) DESC;

# to save time go with just 'en' for now unlikely that something has a different en and not that one
# but can check that:
SELECT videoId, captionsText FROM captions 
WHERE language='en'
AND videoId IN (SELECT videoId from search_api WHERE query_q = 'machine+learning' OR query_q = 'scikit');

SELECT COUNT(videoId) FROM captions WHERE language='en' 
AND videoId IN (SELECT videoId from search_api WHERE query_q = 'machine+learning' OR query_q = 'scikit');

SELECT COUNT(DISTINCT(videoId)) FROM captions WHERE language='en' 
AND videoId IN (SELECT videoId from search_api WHERE query_q = 'machine+learning' OR query_q = 'scikit');
# thank christ no repeats! 

SELECT captions.videoId, captions.captionsText, statistics.durationSeconds FROM captions 
INNER JOIN statistics
ON captions.videoId = statistics.videoId
WHERE captions.language='en'
AND captions.videoId IN (SELECT videoId from search_api WHERE query_q = 'machine+learning' OR query_q = 'scikit');

SELECT videoId FROM statistics WHERE caption=false;

SELECT COUNT(videoId) FROM statistics WHERE caption='false'      # 234
AND videoId NOT IN (SELECT videoId FROM captions WHERE queryMethod = 'youtube-dl')  # 234
AND videoId NOT IN (SELECT videoId FROM NOcaptions);   # 189 - oh!! it's already got some of them!

# Run the youtube-dl and see if the 189 reduces to 0.

SELECT videoId, durationSeconds FROM statistics WHERE caption='false' 
AND videoId NOT IN (SELECT videoId FROM captions WHERE queryMethod = 'youtube-dl') 
# AND videoId NOT IN (SELECT DISTINCT(videoId) FROM statistics WHERE durationSeconds < 10) 
AND videoId NOT IN (SELECT videoId FROM NOcaptions);

SELECT * FROM search_api WHERE query_q = 'data+science' ORDER BY STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s');

SELECT videoId, query_q, publishedAt FROM search_api;

SELECT COUNT(*) FROM youtubeProjectDB.captions where language LIKE '%en%' AND wordCount IS NULL;

SELECT * FROM youtubeProjectDB.captions where language LIKE '%en%' ORDER BY wordCount DESC;

SELECT wordCount FROM youtubeProjectDB.captions where language LIKE '%en%' ORDER BY wordCount DESC;

SELECT * FROM captions WHERE id = 5978;
SELECT * FROM search_api WHERE videoId = 'bcXMt6ZCJPY';
SELECT captionsText FROM captions WHERE id = 5978;

SELECT NOW(), COUNT(*) FROM captions; 
#  NOW(), COUNT(*)
# '2017-04-04 21:49:37', '8438'
# # NOW(), COUNT(*)
# 2017-04-04 22:30:09	9482
# gained about 1000 in half an hour..
# NOW(), COUNT(*)
# 2017-04-04 23:37:13, 11577
# 2017-04-05 00:55:14	13706
# 2017-04-05 02:30:20	14494

SELECT videoId, COUNT(videoId) FROM youtubeProjectDB.captions WHERE queryMethod="youtube-dl" GROUP BY videoId ORDER BY COUNT(videoId) DESC;

SELECT * FROM captions WHERE videoId = 'fgNSdXKrA_Y';

SELECT * FROM youtubeProjectDB.search_api WHERE id IN (9894, 9897, 9901, 9, 4708,4717,4864, 5823, 2630, 2714);

SELECT * FROM captions  
WHERE videoId IN
(SELECT videoId FROM youtubeProjectDB.search_api WHERE id IN (9894, 9897, 9901, 9, 4708,4717,4864, 5823, 2630, 2714));

SELECT COUNT(DISTINCT(language)) FROM youtubeProjectDB.captions;

SELECT COUNT(DISTINCT(language)) FROM youtubeProjectDB.captions WHERE language IS LIKE '%en%';

SELECT COUNT(language) FROM captions WHERE language LIKE '%en%'; 

SELECT COUNT(language) FROM captions WHERE language LIKE '%de%';

SELECT COUNT(DISTINCT(videoId)) FROM captions;

SELECT COUNT(videoId) FROM captions WHERE language LIKE '%en%';

SELECT AVG(durationSeconds)/60 FROM statistics WHERE statistics.videoId IN (SELECT videoId FROM captions WHERE language LIKE '%en%');

# https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format
# http://stackoverflow.com/questions/12776075/searching-data-between-dates-stored-in-varchar-in-mysql#12776356

# STR_TO_DATE - runs fast enough for this number of rows without creating a column with a MySQL DATETIME type.
# can leave the column as VARCHAR for now

# basic tests:

SELECT STR_TO_DATE(publishedAt, '%Y-%m-%d %h:%i:%s') FROM youtubeProjectDB.search_api WHERE id = 10;

SELECT STR_TO_DATE('2017-02-06 17:40:47', '%Y-%m-%d %k:%i:%s');

SELECT STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s') FROM youtubeProjectDB.search_api;

# Now for something useful:

SELECT * FROM search_api
WHERE STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s') 
BETWEEN STR_TO_DATE('01/01/2017', '%d/%m/%Y')
AND STR_TO_DATE('31/01/2017', '%d/%m/%Y')
AND query_q='machine+learning';


SELECT  * FROM search_api
INNER JOIN statistics
ON search_api.videoId = statistics.videoId
WHERE STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s') 
BETWEEN STR_TO_DATE('01/01/2017', '%d/%m/%Y')
AND STR_TO_DATE('31/01/2017', '%d/%m/%Y')
AND query_q='machine+learning';

# Note - it wants the WHERE clause at the end, after the 'ON' section.

(SELECT publishedAt, videoTitle, channelTitle, description, videoId 
  FROM search_api 
  WHERE query_q='machine+learning' 
  ORDER BY STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s') DESC 
  LIMIT 5)
UNION
(SELECT publishedAt, videoTitle, channelTitle, description, videoId 
  FROM search_api 
  WHERE query_q='machine+learning' 
  ORDER BY STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s') ASC 
  LIMIT 5);
# It likes the WHERE clause before the ORDER BY clause
# Also, the statements on each side of "UNION" need to be in brackets.


# or the same thing, without restrictions on query_q : 
(SELECT publishedAt, videoTitle, channelTitle, description, videoId FROM search_api ORDER BY STR_TO_DATE(queriedAt, '%Y-%m-%d %k:%i:%s') DESC LIMIT 5)
UNION
(SELECT publishedAt, videoTitle, channelTitle, description, videoId FROM search_api ORDER BY STR_TO_DATE(queriedAt, '%Y-%m-%d %k:%i:%s') ASC LIMIT 5);

# test TIME_TO_SEC :
SELECT TIME_TO_SEC('05:15:40');

SELECT duration FROM statistics;

SELECT TIME_TO_SEC(duration) FROM statistics;

SELECT date_format(cast('18:00:00' as time), '%h %p');

# Duration is in ISO 8601

SELECT * FROM search_api WHERE query_q='machine+learning' ORDER BY STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s');

SELECT YEAR(STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s')) FROM search_api;

SELECT YEAR(STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s')), COUNT(*) FROM search_api WHERE query_q='machine+learning' GROUP BY YEAR(STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s'));

SELECT queriedAt, videoId, captionsText FROM captions ORDER BY STR_TO_DATE(queriedAt, '%Y-%m-%d %k:%i:%s') DESC;

SELECT ROUND((likeCount + 0.0) / (viewCount + 0.0), 10) AS likesViewsRatio, 
viewCount, likeCount, dislikeCount, statistics.videoId,
videoTitle, channelTitle, description, publishedAt, regionCode,
favoriteCount, commentCount, duration, durationSeconds, 
dimension, definition, caption, licensedContent, projection, 
relevantTopicIDs, topicCategories, statistics.kind AS statisticsKind, 
statistics.etag AS statisticsEtag, statistics.queriedAt AS statisticsQueriedAt, 
statistics.id AS statisticsID
FROM youtubeProjectDB.statistics
INNER JOIN youtubeProjectDB.search_api
ON search_api.videoId = statistics.videoId
WHERE viewCount > 10000                             
ORDER BY likesViewsRatio DESC;

# Yes, I just briefly looked at only video with a ratio > 1, 1.32, on youtube, 
# he still has 810 likes for 611 views on youtube. Won't shame him but not
# sure how he managed it. It's a short ad that goes for a bit more than a minute. 

# It seemed like an interesting metric - lots of views and a large percentage of 
# viewers are logged in and click like, but practically does not seem to have much
# classification value, if anything finds more sensational videos than useful ones,
# and that despite tweaking viewCount > value.
