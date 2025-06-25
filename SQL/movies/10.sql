-- List the names of all people who have directed a movie that received a rating of at least 9.0

SELECT DISTINCT p.name
FROM people AS p
INNER JOIN directors AS d ON p.id = d.person_id
INNER JOIN ratings AS r ON d.movie_id = r.movie_id
WHERE r.rating >= 9.0;
