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
Species VARCHAR(100),
Variety VARCHAR(100),
Edible BIT,
Spore_color_id INTEGER,
Cap_shape_id INTEGER,
Gill_attatchment_id INTEGER,
Spore_surface_id INTEGER,
Link VARCHAR(50), 
Description TEXT,
Mushroom_id INTEGER NOT NULL AUTO_INCREMENT,
PRIMARY KEY(Mushroom_id)
);

CREATE TABLE MUSHROOM_FIND
(
User_id INTEGER,
Mushroom_id INTEGER,
Found_lat DECIMAL(7,4),
Found_long DECIMAL(7,4),
Found_date DATE,
Quantity INTEGER,
PRIMARY KEY (Mushroom_id, User_id, Found_lat, Found_long, Found_date),
FOREIGN KEY (User_id) REFERENCES APP_USER(User_id)
    ON DELETE CASCADE,
FOREIGN KEY (Mushroom_id) REFERENCES MUSHROOM(Mushroom_id)
    ON DELETE CASCADE
);

CREATE TABLE RECIPE
(
Recipe_id INTEGER NOT NULL AUTO_INCREMENT,
Recipe_name VARCHAR(100),
Recipe_desc TEXT,
PRIMARY KEY(Recipe_id)
);

CREATE TABLE RECIPE_MUSHROOMS
(
Recipe_id INTEGER,
Mushroom_id INTEGER,
FOREIGN KEY (Recipe_id) REFERENCES RECIPE(Recipe_id),
FOREIGN KEY (Mushroom_id) REFERENCES MUSHROOM(Mushroom_id)
);

CREATE TABLE SPORE_COLOR
(
Color_id INTEGER NOT NULL,
Color_desc VARCHAR(20),
PRIMARY KEY(Color_id),
FOREIGN KEY(Color_id) REFERENCES MUSHROOM(Spore_color_id)
);

CREATE TABLE CAP_SHAPE
(
Shape_id INTEGER NOT NULL,
Shape_desc VARCHAR(20),
PRIMARY KEY(Shape_id),
FOREIGN KEY(Shape_id) REFERENCES MUSHROOM(Cap_shape_id)
);

CREATE TABLE GILL_ATTATCHMENT
(
Gill_attatchment_id INTEGER NOT NULL,
Gill_attatchment_desc VARCHAR(20),
PRIMARY KEY(Gill_attatchment_id),
FOREIGN KEY(Gill_attatchment_id) REFERENCES MUSHROOM(Gill_attatchment_id)
);

CREATE TABLE SPORE_SURFACE
(
Spore_surface_id INTEGER NOT NULL,
Spore_surface_desc VARCHAR(20),
PRIMARY KEY(Spore_surface_id),
FOREIGN KEY(Spore_surface_id) REFERENCES MUSHROOM(Spore_surface_id)
);
