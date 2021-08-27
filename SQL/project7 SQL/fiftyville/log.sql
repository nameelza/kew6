-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT * FROM crime_scene_reports WHERE street = "Chamberlin Street";

SELECT * FROM interviews WHERE transcript LIKE "%courthouse%";

SELECT * FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28;

SELECT * FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28;

SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28);

SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28));

SELECT * FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28);

SELECT * FROM (SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28))) WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28);

-- We got 5 suspects now

395717|Bobby|(826) 555-1652|9878712108|30G67EN
438727|Victoria|(338) 555-6650|9586786673|8X428L0
449774|Madison|(286) 555-6063|1988161715|1106N58
514354|Russell|(770) 555-1861|3592750733|322W7JE
686048|Ernest|(367) 555-5533|5773159633|94KL13X



SELECT * FROM (SELECT * FROM (SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28))) WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28)) WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE hour < 11 AND month = 7 AND day = 28);

-- Got 3 suspects now

449774|Madison|(286) 555-6063|1988161715|1106N58
514354|Russell|(770) 555-1861|3592750733|322W7JE
686048|Ernest|(367) 555-5533|5773159633|94KL13X

SELECT * FROM passengers WHERE passport_number IN (SELECT passport_number FROM (SELECT * FROM (SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28))) WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28)) WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE hour < 11 AND month = 7 AND day = 28));

18|3592750733|4C
24|3592750733|2C
36|5773159633|4A
36|1988161715|6D
54|3592750733|6C

SELECT * FROM flights WHERE id IN (18, 24, 36, 54);

SELECT * FROM  airports WHERE id = 8;


SELECT people.name, bank_accounts.creation_year, atm_transactions.day, atm_transactions.month, atm_transactions.year, atm_transactions.atm_location, atm_transactions.transaction_type, atm_transactions.amount
FROM (SELECT * FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller IN ("(286) 555-6063", "(770) 555-1861", "(367) 555-5533") AND duration < 60 AND day = 28)) 
INNER JOIN bank_accounts ON bank_accounts.person_id = people.id
INNER JOIN atm_transactions ON atm_transactions.account_number  = bank_accounts.account_number;




SELECT people.name, bank_accounts.creation_year, atm_transactions.day, atm_transactions.month, atm_transactions.year, atm_transactions.atm_location, atm_transactions.transaction_type, atm_transactions.amount
FROM people
INNER JOIN bank_accounts ON bank_accounts.person_id = people.id
INNER JOIN atm_transactions ON atm_transactions.account_number  = bank_accounts.account_number
WHERE people.phone_number IN (SELECT receiver FROM phone_calls WHERE caller IN ("(286) 555-6063", "(770) 555-1861", "(367) 555-5533") AND duration < 60 AND day = 28);



SELECT people.name, courthouse_security_logs.year, courthouse_security_logs.month, courthouse_security_logs.day, courthouse_security_logs.hour, courthouse_security_logs.minute, courthouse_security_logs.activity
FROM people
INNER JOIN courthouse_security_logs ON courthouse_security_logs.license_plate = people.license_plate
WHERE people.license_plate IN (SELECT license_plate FROM (SELECT * FROM (SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28))) WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28)) WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE hour < 11 AND month = 7 AND day = 28));




SELECT people.name, bank_accounts.creation_year, atm_transactions.day, atm_transactions.month, atm_transactions.year, atm_transactions.atm_location, atm_transactions.transaction_type, atm_transactions.amount
FROM people
INNER JOIN bank_accounts ON bank_accounts.person_id = people.id
INNER JOIN atm_transactions ON atm_transactions.account_number  = bank_accounts.account_number
WHERE people.id IN (SELECT id FROM (SELECT * FROM (SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28))) WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28)) WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE hour < 11 AND month = 7 AND day = 28));

-- CHEKING THE TIME OF THE FLIGHTS OUT OF THE CITY ON JULY 29 OF ALL THE SUSPECTS AND LOOKING FOR THE EARLIEST

SELECT people.name, flights.year, flights.month, flights.day, flights.hour, flights.minute, airports.city, airports.full_name
FROM people
INNER JOIN passengers ON passengers.passport_number = people.passport_number
INNER JOIN flights ON flights.id = passengers.flight_id
INNER JOIN airports ON airports.id = flights.destination_airport_id
WHERE people.id IN (SELECT id FROM (SELECT * FROM (SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE atm_location LIKE "%Fifer Street%" AND month = 7 AND day = 28))) WHERE phone_number IN (SELECT caller FROM phone_calls WHERE duration <= 60 AND month = 7 AND day = 28)) WHERE license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE hour < 11 AND month = 7 AND day = 28));

-- CHECKING DESTINATION AIRPORT OF THE MAIN SUSPECT

SELECT people.name, flights.year, flights.month, flights.day, flights.hour, flights.minute, airports.city, airports.full_name
   ...> FROM people
   ...> INNER JOIN passengers ON passengers.passport_number = people.passport_number
   ...> INNER JOIN flights ON flights.id = passengers.flight_id
   ...> INNER JOIN airports ON airports.id = flights.destination_airport_id
   ...> WHERE people.name = "Ernest";

SELECT * FROM phone_calls WHERE caller IN (SELECT phone_number FROM people WHERE name = "Ernest");

-- NAME OF THE ACCOMPLICE
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller IN (SELECT phone_number FROM people WHERE name = "Ernest") AND day = 28 AND duration < 60); 




SELECT people.name, flights.year, flights.month, flights.day, flights.hour, flights.minute, airports.city, airports.full_name
FROM people
INNER JOIN passengers ON passengers.passport_number = people.passport_number
INNER JOIN flights ON flights.id = passengers.flight_id
INNER JOIN airports ON airports.id = flights.destination_airport_id
WHERE people.name = "Ernest";


SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE caller IN (SELECT phone_number FROM people WHERE name = "Ernest") AND day = 28 AND duration < 60); 


