CREATE TABLE APP_USER
(
Username VARCHAR(20) UNIQUE,
Password VARCHAR(15),
User_description TEXT,
Home_Location_lat DECIMAL(7,4),
Home_Location_long DECIMAL(7,4),
PRIMARY KEY (Username)
);

CREATE TABLE MUSHROOM
(
Genus VARCHAR(20),
Species VARCHAR(100),
Variety VARCHAR(100),
Edible BIT,
Spore_color_id INT,
Cap_shape_id INT,
Gill_attatchment_id INT,
Spore_surface_id INT,
Kuo_link VARCHAR(50), 
Description TEXT,
Mushroom_id int NOT NULL AUTO_INCREMENT,
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
Recipe_id INT NOT NULL AUTO_INCREMENT,
Recipe_name VARCHAR(100),
Recipe_desc TEXT,
PRIMARY KEY(Recipe_id)
);

CREATE TABLE RECIPE_MUSHROOMS
(
Recipe_id INT,
Mushroom_id INT,
FOREIGN KEY (Recipe_id) REFERENCES RECIPE(Recipe_id),
FOREIGN KEY (Mushroom_id) REFERENCES MUSHROOM(Mushroom_id)
);

CREATE TABLE SPORE_COLOR
(
Color_id INT NOT NULL,
Color_desc VARCHAR(20),
PRIMARY KEY(Color_id),
FOREIGN KEY(Color_id) REFERENCES MUSHROOM(Spore_color_id)
);

CREATE TABLE CAP_SHAPE
(
Shape_id INT NOT NULL,
Shape_desc VARCHAR(20),
PRIMARY KEY(Shape_id),
FOREIGN KEY(Shape_id) REFERENCES MUSHROOM(Cap_shape_id)
);

CREATE TABLE GILL_ATTATCHMENT
(
Gill_attatchment_id INT NOT NULL,
Gill_attatchment_desc VARCHAR(20),
PRIMARY KEY(Gill_attatchment_id),
FOREIGN KEY(Gill_attatchment_id) REFERENCES MUSHROOM(Gill_attatchment_id)
);

CREATE TABLE SPORE_SURFACE
(
Spore_surface_id INT NOT NULL,
Spore_surface_desc VARCHAR(20),
PRIMARY KEY(Spore_surface_id),
FOREIGN KEY(Spore_surface_id) REFERENCES MUSHROOM(Spore_surface_id)
);
