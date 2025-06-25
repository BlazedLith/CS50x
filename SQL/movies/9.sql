-- List the names of all people who starred in a movie released in 2004, ordered by birth year

SELECT DISTINCT p.name
FROM people AS p
INNER JOIN stars AS s ON p.id = s.person_id
INNER JOIN movies AS m ON s.movie_id = m.id
WHERE m.year = 2004
ORDER BY p.birth;
