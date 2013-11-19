CREATE TABLE APP_USER
(
Username VARCHAR(32) UNIQUE,
User_id INTEGER NOT NULL AUTO_INCREMENT,
User_description TEXT,
Home_Location_lat DECIMAL(7,4),
Home_Location_long DECIMAL(7,4),
PRIMARY KEY (User_id)
);

CREATE TABLE MUSHROOM
(
Genus VARCHAR(20),
Species VARCHAR(20),
Variety VARCHAR(20),
Edible BIT,
SporeColor VARCHAR(20),
CapShape VARCHAR(20),
Description VARCHAR(1000),
Mushroom_id INTEGER NOT NULL AUTO_INCREMENT,
PRIMARY KEY(Mushroom_id)
);

CREATE TABLE MUSHROOM_FIND
(
User_id INT,
Mushroom_id INT,
Found_lat DECIMAL(7,4),
Found_long DECIMAL(7,4),
Found_date DATE,
Quantity INT,
PRIMARY KEY (Mushroom_id, User_id, Found_lat, Found_long, Found_date),
FOREIGN KEY (User_id) REFERENCES APP_USER(User_id)
    ON DELETE CASCADE,
FOREIGN KEY (Mushroom_id) REFERENCES MUSHROOM(Mushroom_id)
    ON DELETE CASCADE
);

CREATE TABLE RECIPE
(
Recipe_id INTEGER NOT NULL AUTO_INCREMENT,
Recipe_name VARCHAR(20),
Recipe_desc VARCHAR(500),
Mushroom_id INT,
FOREIGN KEY (Mushroom_id) REFERENCES MUSHROOM(Mushroom_id),
PRIMARY KEY(Recipe_id)
);
