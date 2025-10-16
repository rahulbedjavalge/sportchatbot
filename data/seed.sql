DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS goals;

CREATE TABLE matches (
  id INTEGER PRIMARY KEY,
  sport TEXT NOT NULL,
  tournament TEXT,
  date TEXT NOT NULL,         -- YYYY-MM-DD
  stadium TEXT NOT NULL,
  city TEXT NOT NULL,
  home_team TEXT NOT NULL,
  away_team TEXT NOT NULL,
  home_score INTEGER NOT NULL,
  away_score INTEGER NOT NULL
);

CREATE TABLE goals (
  id INTEGER PRIMARY KEY,
  match_id INTEGER NOT NULL,
  minute INTEGER NOT NULL,
  team TEXT NOT NULL,
  scorer_name TEXT NOT NULL,
  FOREIGN KEY (match_id) REFERENCES matches(id)
);

-- Football (today)
INSERT INTO matches VALUES
(1, 'Football', 'City Cup', date('now'), 'Olympiastadion', 'Berlin',
 'Berlin FC', 'Munich United', 2, 1);

INSERT INTO goals VALUES
(1,1,17,'Berlin FC','Jonas Keller'),
(2,1,54,'Berlin FC','Marco Hahn'),
(3,1,71,'Munich United','Luis Romero');

-- Football
INSERT INTO matches VALUES
(2, 'Football', 'Rhein Main Trophy', '2025-05-10', 'Deutsche Bank Park', 'Frankfurt',
 'Frankfurt Eagles', 'Cologne Lions', 1, 1);
INSERT INTO goals VALUES
(4,2,43,'Frankfurt Eagles','M. Toure'),
(5,2,75,'Cologne Lions','R. Novak');

-- Basketball
INSERT INTO matches VALUES
(3, 'Basketball', 'Euro City Series', '2025-04-21', 'Mercedes-Benz Arena', 'Berlin',
 'Berlin Bears', 'Madrid Royals', 88, 92);

-- Tennis (players as teams)
INSERT INTO matches VALUES
(4, 'Tennis', 'Clay Masters', '2025-06-02', 'Roland Garros - Court Suzanne-Lenglen', 'Paris',
 'A. Petrov', 'L. Duarte', 2, 1);

-- Football
INSERT INTO matches VALUES
(5, 'Football', 'Nordic Challenge', '2025-02-14', 'Ullevi', 'Gothenburg',
 'Gothenburg IF', 'Oslo City', 0, 0);

-- Football
INSERT INTO matches VALUES
(6, 'Football', 'Danube Cup', '2025-03-09', 'Groupama Arena', 'Budapest',
 'Budapest KC', 'Vienna Athletic', 3, 2);
INSERT INTO goals VALUES
(6,6,8,'Budapest KC','A. Szabo'),
(7,6,29,'Vienna Athletic','F. Leitner'),
(8,6,41,'Budapest KC','D. Nagy'),
(9,6,72,'Vienna Athletic','K. Steiner'),
(10,6,85,'Budapest KC','L. Farkas');

-- Football
INSERT INTO matches VALUES
(7, 'Football', 'Baltic Shield', '2025-01-17', 'Daugava Stadium', 'Riga',
 'Riga United', 'Tallinn North', 1, 0);
INSERT INTO goals VALUES
(11,7,63,'Riga United','J. Ozols');
