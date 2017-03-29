# https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format
# http://stackoverflow.com/questions/12776075/searching-data-between-dates-stored-in-varchar-in-mysql#12776356

# The following contains the required date format stuff to query on the datetime columns that are
# just VARCHAR strings. Performance with these small tables is very fast, but if it got a lot 
# bigger it might need the column as DATETIME types

SELECT * FROM youtubeProjectDB.search_api 
WHERE STR_TO_DATE(publishedAt, '%Y-%m-%d %k:%i:%s') 
BETWEEN STR_TO_DATE('01/01/2017', '%d/%m/%Y')
AND STR_TO_DATE('31/01/2017', '%d/%m/%Y');

