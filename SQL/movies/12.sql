-- List the titles of all movies in which both Bradley Cooper and Jennifer Lawrence starred

SELECT m1.title
FROM movies AS m1
INNER JOIN stars AS s1 ON m1.id = s1.movie_id
INNER JOIN people AS p1 ON s1.person_id = p1.id
INNER JOIN stars AS s2 ON m1.id = s2.movie_id
INNER JOIN people AS p2 ON s2.person_id = p2.id
WHERE p1.name = 'Bradley Cooper'
AND p2.name = 'Jennifer Lawrence'
AND p1.id != p2.id;
