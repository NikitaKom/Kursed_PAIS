Я додав до файлу з кодом папку у вигляди проекту pycharm, щоб вам не потрібно було підключати бібліотеки, але якщо хочете то в коді є все що потрібно

база даних в свою чергу не зберігається єдиним SQL файлом (особливості роботи у PostgreSQL), тому я надам вам запити для її створення у вашій СУБД



-- Database: courseworkdb

CREATE DATABASE courseworkdb
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Russian_Russia.1251'
    LC_CTYPE = 'Russian_Russia.1251'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE "User" (
  UserID SERIAL PRIMARY KEY,
  UserName VARCHAR(25),
  UserLastName VARCHAR(25),
  UserAge INT,
  UserMail VARCHAR(255),
  UserCountry VARCHAR(25),
  UserLanguage VARCHAR(25),
  UserPhone VARCHAR(25),
  RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

CREATE TABLE "Film" (
  FilmID SERIAL PRIMARY KEY,
  FilmName VARCHAR(25),
  FilmDescription TEXT,
  FilmYear INT,
  FilmRating REAL,
  FilmTrailer TEXT,
  FilmPicture BYTEA
  );

CREATE TABLE "Genres" (
  GenerID SERIAL PRIMARY KEY,
  GenerName VARCHAR(25)
  );

CREATE TABLE "FavouriteFilms" (
  UserID INT,
  FilmID INT,
  FOREIGN KEY (UserID) REFERENCES "User" (UserID),
  FOREIGN KEY (FilmID) REFERENCES "Film" (FilmID)
  );

CREATE TABLE "FavouriteGenres" (
  UserID INT,
  GenerID INT,
  FOREIGN KEY (UserID) REFERENCES "User" (UserID),
  FOREIGN KEY (GenerID) REFERENCES "Genres" (GenerID)
  );

CREATE TABLE "FilmGenres" (
    FilmID INT,
    GenerID INT,
    FOREIGN KEY (FilmID) REFERENCES "Film" (FilmID),
    FOREIGN KEY (GenerID) REFERENCES "Genres" (GenerID)
);

INSERT INTO "User" (UserName, UserLastName, UserAge, UserMail, UserCountry, UserLanguage, UserPhone)
VALUES
('Alice', 'Smith', 25, 'alice.smith@example.com', 'USA', 'English', '+1234567890'),
('Bob', 'Brown', 30, 'bob.brown@example.com', 'Canada', 'English', '+1234567891'),
('Charlie', 'Davis', 22, 'charlie.davis@example.com', 'UK', 'English', '+1234567892'),
('Diana', 'Johnson', 28, 'diana.johnson@example.com', 'Australia', 'English', '+1234567893'),
('Ethan', 'Williams', 35, 'ethan.williams@example.com', 'Germany', 'German', '+1234567894');

SELECT * FROM "User";

ALTER TABLE "Film" ALTER COLUMN FilmName TYPE VARCHAR(50);
ALTER TABLE "Film" ALTER COLUMN FilmPicture TYPE TEXT;
INSERT INTO "Film" (FilmName, FilmDescription, FilmYear, FilmRating, FilmTrailer, FilmPicture)
VALUES
('Inception', 'Dom Cobb is a skilled thief, the best in the dangerous art of extraction: stealing valuable secrets from deep within the subconscious during the dream state, when the mind is at its most vulnerable. Cobb’s rare ability has made him a coveted player in industrial espionage, but it has also cost him everything he loves. Now Cobb is offered a chance at redemption. One last job could give him his life back, but only if he can accomplish the impossible - inception. Instead of stealing an idea, Cobb and his team must plant one. However, no amount of planning or skill can prepare the team for the dangerous enemy that seems to predict their every move, a foe only Cobb could have seen coming.', 2010, 8.8, 'https://www.youtube.com/watch?v=YoHD9XEInc0', 'https://c4.wallpaperflare.com/wallpaper/764/590/391/inception-leonardo-dicaprio-movie-posters-2400x3500-entertainment-movies-hd-art-wallpaper-preview.jpg'),
('The Matrix', 'When a hacker known as Neo confronts the startling truth, he learns that the world around him is a lie. The world is controlled by powerful machines that use humanity as a source of energy. Joining the underground resistance led by Morpheus and Trinity, Neo must accept his role as The One to free humanity and battle the agents who seek to suppress those who learn the truth.', 1999, 8.7, 'https://www.youtube.com/watch?v=vKQi3bBA1y8', 'https://m.media-amazon.com/images/M/MV5BN2NmN2VhMTQtMDNiOS00NDlhLTliMjgtODE2ZTY0ODQyNDRhXkEyXkFqcGc@._V1_.jpg'),
('Interstellar', 'As humanity faces extinction, a group of explorers venture beyond our galaxy to find a new home. They discover a wormhole that leads them to distant galaxies where potentially habitable planets exist. Throughout the perilous journey, the crew confronts challenges of time, space, and human destiny. The lead character, former NASA pilot Cooper, leaves his children on Earth and embarks on the most critical mission in human history.', 2014, 8.6, 'https://www.youtube.com/watch?v=zSWdZVtXT7E', 'https://cdn.wallpapersafari.com/83/41/IiWZAE.jpg'),
('The Shawshank Redemption', 'Andy Dufresne, a young and successful banker, is sentenced to life imprisonment for a crime he did not commit. He is sent to Shawshank, the harshest prison in Maine, where he faces brutality, injustice, and hopelessness. Despite these hardships, he doesn’t lose hope and finds a true friend in fellow inmate Ellis "Red" Redding. Over the years, Andy devises an extraordinary escape plan that will become a symbol of hope for all inmates.', 1994, 9.3, 'https://www.youtube.com/watch?v=6hB3S9bIaco', 'https://picfiles.alphacoders.com/139/139366.jpg'),
('The Dark Knight', 'Gotham is once again gripped by turmoil as a mysterious criminal known as the Joker unleashes chaos and violence, threatening the lives of all its citizens. Only Batman can stop him, but to do so, he must overcome his inner fears and doubts. Batman and Commissioner Gordon join forces with District Attorney Harvey Dent to bring an end to the Joker’s reign of terror. However, the Joker proves to be more cunning and dangerous than they ever imagined. A deadly game begins, and Batman must make a difficult choice between truth and justice.', 2008, 9.0, 'https://www.youtube.com/watch?v=EXeTwQWrcwY', 'https://www.originalfilmart.com/cdn/shop/products/dark_knight_2008_graffiti_imax_original_film_art_db3b3ed4-350b-433d-9067-f41bc118b189_5000x.jpg?v=1678127664'),
('Fight Club', 'The life of the narrator is dull and monotonous until he meets the unconventional leader Tyler Durden. Together, they create an underground fight club, which becomes a way to vent aggression and conquer fears. But as the club grows, it turns into something more - a revolution, an attempt to change the world and rid society of all norms and rules. The narrator begins to realize that Tyler is not who he seems, and the club has far-reaching and terrifying consequences.', 1999, 8.8, 'https://www.youtube.com/watch?v=SUXWAEX2jlg', 'https://i.pinimg.com/originals/18/ce/60/18ce608c04434b2da0ce7cc243e7ab0d.jpg'),
('Pulp Fiction', 'A series of intersecting lives of criminals, a boxer, a mobster and his wife, hitmen, and others are entangled in a sequence of criminal events. The film is structured like a mosaic, where each piece comes together to form an engaging and unexpected climax. Quentin Tarantino’s cult classic with brilliant dialogue and an intense atmosphere of the criminal underworld.', 1994, 8.9, 'https://www.youtube.com/watch?v=s7EdQ4FqbhY', 'https://wallpapercat.com/w/full/f/4/e/176568-1872x2500-iphone-hd-pulp-fiction-wallpaper-photo.jpg'),
('Forrest Gump', 'Forrest Gump, a man with a low IQ, finds himself part of significant historical events in the U.S. during the second half of the 20th century. Through his innocence and kindness, he wins the hearts of everyone he meets, meets presidents, goes to war, and achieves success in business. At the same time, he continues to love his childhood friend Jenny and seeks his path to happiness.', 1994, 8.8, 'https://www.youtube.com/watch?v=bLvqoHBptjg', 'https://musicart.xboxlive.com/7/40025100-0000-0000-0000-000000000002/504/image.jpg?w=1920&h=1080'),
('The Godfather', 'The saga of the Corleone mafia family, following Michael Corleone’s rise to power. This exploration into the mafia world reveals themes of honor, brutality, and loyalty to family. Initially reluctant to be involved in the business, Michael gradually becomes the ruthless leader of the clan. His journey to power is marked by betrayals, murders, and conflicts that affect every family member.', 1972, 9.2, 'https://www.youtube.com/watch?v=sY1S34973zA', 'https://images2.alphacoders.com/110/thumb-1920-1108220.jpg'),
('The Lord of the Rings: The Fellowship of the Ring', 'Middle-earth is in danger as the dark lord Sauron seeks to gain control over the world with the One Ring. A young hobbit, Frodo Baggins, inherits the Ring and undertakes the mission to destroy it, to rid the world of evil forever. On his journey, he joins forces with the wizard Gandalf, the elf Legolas, the dwarf Gimli, the brave man Aragorn, and others, forming the Fellowship of the Ring.', 2001, 8.8, 'https://www.youtube.com/watch?v=V75dMMIW2B4', 'https://images.moviesanywhere.com/198e228b071c60f5ad57e5f62fe60029/ff22cad6-2218-414d-b853-3f95d76905c7.jpg');

SELECT * FROM "Film";

INSERT INTO "Genres" (GenerName)
VALUES
('Action'),
('Drama'),
('Sci-Fi'),
('Fantasy'),
('Thriller'),
('Comedy'),
('Adventure'),
('Crime'),
('Romance'),
('Mystery');

INSERT INTO "FavouriteGenres" (UserID, GenerID)
VALUES
(1, 1),  -- Alice likes Action
(1, 3),  -- Alice likes Sci-Fi
(2, 2),  -- Bob likes Drama
(2, 8),  -- Bob likes Crime
(3, 3),  -- Charlie likes Sci-Fi
(3, 4),  -- Charlie likes Fantasy
(4, 1),  -- Diana likes Action
(4, 6),  -- Diana likes Comedy
(5, 2),  -- Ethan likes Drama
(5, 7);  -- Ethan likes Adventure

INSERT INTO "FavouriteFilms" (UserID, FilmID)
VALUES
(1, 1),  -- Alice's favorite: Inception
(1, 2),  -- Alice's favorite: The Matrix
(2, 3),  -- Bob's favorite: Interstellar
(2, 4),  -- Bob's favorite: The Shawshank Redemption
(3, 2),  -- Charlie's favorite: The Matrix
(3, 5),  -- Charlie's favorite: The Dark Knight
(4, 6),  -- Diana's favorite: Fight Club
(4, 7),  -- Diana's favorite: Pulp Fiction
(5, 8),  -- Ethan's favorite: Forrest Gump
(5, 9);  -- Ethan's favorite: The Godfather

INSERT INTO "FilmGenres" (FilmID, GenerID) VALUES 
(1, 1), (1, 3), (1, 5),       -- Inception
(2, 1), (2, 3), (2, 5),       -- The Matrix
(3, 3), (3, 7), (3, 2),       -- Interstellar
(4, 2), (4, 8),               -- The Shawshank Redemption
(5, 1), (5, 5), (5, 8),       -- The Dark Knight
(6, 2), (6, 5),               -- Fight Club
(7, 8), (7, 2), (7, 10),      -- Pulp Fiction
(8, 2), (8, 6), (8, 9),       -- Forrest Gump
(9, 8), (9, 2),               -- The Godfather
(10, 7), (10, 4), (10, 1);    -- The Lord of the Rings: The Fellowship of the Ring

SELECT * FROM "User";
SELECT * FROM "FavouriteFilms";
SELECT * FROM "Genres";