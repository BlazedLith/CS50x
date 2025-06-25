-- List all movies released in 2010 and their ratings, in descending order by rating

SELECT m.title, r.rating
FROM movies AS m
INNER JOIN ratings AS r ON m.id = r.movie_id
WHERE m.year = 2010
ORDER BY r.rating DESC, m.title;
