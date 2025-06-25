-- List the names of all people who starred in a movie in which Kevin Bacon (born in 1958) also starred, excluding Kevin Bacon himself

SELECT DISTINCT p.name
FROM people AS p
INNER JOIN stars AS s1 ON p.id = s1.person_id
INNER JOIN movies AS m1 ON s1.movie_id = m1.id
WHERE m1.id IN (
    SELECT m2.id
    FROM movies AS m2
    INNER JOIN stars AS s2 ON m2.id = s2.movie_id
    INNER JOIN people AS kb ON s2.person_id = kb.id
    WHERE kb.name = 'Kevin Bacon' AND kb.birth = 1958
)
AND p.name != 'Kevin Bacon';
