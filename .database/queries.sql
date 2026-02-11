--CREATE TABLE Reviews (
  --  id INTEGER PRIMARY KEY AUTOINCREMENT,
   -- user_id INTEGER,
   -- review_date TEXT NOT NULL,
   -- rating INTEGER,
--    movie_title TEXT NOT NULL,
 --   review_text TEXT,
 --   FOREIGN KEY (user_id) REFERENCES Users(id) );


--CREATE TABLE Users (
 --   id INTEGER PRIMARY KEY AUTOINCREMENT,
  --  username TEXT NOT NULL,
  --  password TEXT NOT NULL);

--INSERT INTO Users (username, password) VALUES
--('adyan',  'scrypt:32768:8:1$ZIUB1D5ICNI2GZ5w$4de3cadd75e3f03617e0c7423a3aab85a84fd9dea009295ce41d438e52da3cbc0b64def6ecbaaef13255c4918585c15e6c313d8d98d64f37c37d22b3e25bf04e'),
--('arain', 'scrypt:32768:8:1$YfnN0EtmRGYdDphU$6803d35904ca054bc23232df87abd76ec9fe75eae8fe21301146f8bcfc1649715a787e218cb2a7463ab1d11b4e0186cf0541144aaf554d022cd9fc9395b2cae8'),
--('sazid', 'scrypt:32768:8:1$LaSx68XLEuZ1TWJU$0aa3b35c461bcf8343554773d6a3957b7b22af7a902403b5f7e1574d42b4e7630959b483af7a5d22e3bc1659ccd6eb1209917c8537417fddc1e6960bb43a4b04'),
--('rafqat',    'scrypt:32768:8:1$FdOgvhXqmAAY5465$192fa886bc701dd88b4b73be9ee356af23c83fc9918fcfa8cb40cbc65ff3c31f0d99ac02fd12f6c2b218ef8a518055b1391ef02a5456daa277711d7ee5c02a05'),
--('ehan',   'scrypt:32768:8:1$19yCXh84aS6I31Z3$9cf8bf32640359830b8bac6a8f8ea46ca4c6f78dbc607769ea887c9415bd7c8754dad12cdc41c9570fa849b3a26a0d55aedaca2f770ac7ea74342f5728686109');

--INSERT INTO Reviews (user_id, review_date, rating, movie_title, review_text) VALUES
--(1, '2026-01-28', 5, 'Marty Supreme',
 --'Amazing movie with strong character development and a chaotic but grounded story. The soundtrack was also excellent.'),

--(1, '2026-01-28', 5, 'Forrest Gump',
 --'One of my top movies of all time. Emotional, inspiring, and timeless.'),

--(1, '2026-01-10', 5, 'Chainsaw Man',
 --'Rewatched the series. Great characters and intense pacing. Very entertaining overall.'),

--(2, '2025-09-28', 5, 'Superman',
-- 'Rewatched this and it still holds up well. Strong cast and powerful themes throughout.'),

--(2, '2025-01-20', 3, 'Despicable Me 4',
 --'The Minions were fun, but the overall story was weaker compared to earlier films.'),

--(3, '2024-12-14', 1, 'Ant-Man and the Wasp: Quantumania',
 --'Disappointing movie with weak villains and an uninteresting story.'),

--(3, '2024-11-17', 5, 'Scott Pilgrim vs. the World',
-- 'Very creative visuals, great action scenes, and strong character development.'),

--(4, '2024-11-17', 3, 'Venom',
 --'Pretty good for an origin movie. Enjoyable action and an interesting main character.'),

--(4, '2025-06-03', 4, 'Blade Runner',
 --'Visually impressive and thought-provoking. Some scenes were strange but overall a strong film.'),

--(5, '2025-07-20', 3, 'Final Destination Bloodlines',
 --'Solid horror movie with intense scenes and a decent main character.');

-- ALTER TABLE Reviews ADD COLUMN poster_filename TEXT;

-- ALTER TABLE Reviews ADD COLUMN poster_url TEXT;

--SELECT Reviews.*, Users.username
--FROM Reviews
--JOIN Users ON Reviews.user_id = Users.id
--ORDER BY Reviews.id DESC;

--SELECT Reviews.*, Users.username
--FROM Reviews
--JOIN Users ON Reviews.user_id = Users.id
--WHERE Reviews.rating >= 4
--ORDER BY Reviews.id DESC;

--SELECT Reviews.*, Users.username
--FROM Reviews
--JOIN Users ON Reviews.user_id = Users.id
--WHERE Users.username = 'adyan'
--ORDER BY Reviews.id DESC;

--UPDATE Reviews
--SET rating = 5, review_text = 'Updated review text'
----WHERE id = 1 AND user_id = 2;

--DELETE FROM Reviews
--WHERE id = 1 AND user_id = 2;
