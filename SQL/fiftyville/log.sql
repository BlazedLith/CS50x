-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Query to Identify the Thief
-- We will search for a crime scene report that matches the date and location of the theft.
SELECT *
FROM crime_scene_reports
WHERE year = 2021
  AND month = 7
  AND day = 28
  AND street = 'Humphrey Street';

-- Query to retrieve interview transcripts mentioning the bakery
SELECT * FROM interviews
WHERE transcript LIKE '%bakery%';

-- Query to find ATM transactions matching Eugene's description
SELECT * FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';

-- Query to find people associated with the account numbers from ATM transactions
SELECT DISTINCT p.name, a.account_number
FROM people AS p
JOIN bank_accounts AS a ON p.id = a.person_id
WHERE a.account_number IN (28500762, 28296815, 76054385, 49610011, 16153065, 25506511, 81061156, 26013199);

-- Query to find flights departing on July 29, 2021
SELECT * FROM flights
WHERE year = 2021 AND month = 7 AND day = 29;

-- Query to find the destination cities for the flights on July 29, 2021
SELECT f.id, a.city AS destination_city
FROM flights AS f
JOIN airports AS a ON f.destination_airport_id = a.id
WHERE f.year = 2021 AND f.month = 7 AND f.day = 29;

-- Query to find phone calls made from the bakery on July 28, 2021
SELECT * FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;

-- Check the names of all the callers and match them with those who took flight same day
-- Check the names of the recievers with suspicious callers
-- Enter information and check to see if the names are right