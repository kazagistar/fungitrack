CREATE OR REPLACE VIEW MUSHROOM_VIEW AS
SELECT Genus || " " || Species || coalesce("," || Variety, "") AS name,
  Genus, Species, Variety, Edible, Link, Description,
  Color_desc as color,
  Shape_desc as shape,
  Gill_attatchment_desc as gill,
  Spore_surface_desc as spore,
  Mushroom_id as id
FROM MUSHROOM
  LEFT OUTER JOIN SPORE_COLOR ON Spore_color_id = Color_id
  LEFT OUTER JOIN CAP_SHAPE ON Cap_shape_id = Shape_id
  LEFT OUTER JOIN GILL_ATTATCHMENT ON MUSHROOM.Gill_attatchment_id = GILL_ATTATCHMENT.Gill_attatchment_id 
  LEFT OUTER JOIN SPORE_SURFACE ON MUSHROOM.Spore_surface_id = SPORE_SURFACE.Spore_surface_id;
  
CREATE OR REPLACE VIEW MUSHROOM_FIND_VIEW AS
SELECT username, MUSHROOM_FIND.user_id as user_id, mushroom_id, quantity,
  MUSHROOM_VIEW.name as mushroom,
  Found_lat as latitude,
  Found_long as longitude,
  Found_date as date
FROM MUSHROOM_FIND
  JOIN APP_USER ON APP_USER.User_id = MUSHROOM_FIND.User_id
  JOIN MUSHROOM_VIEW ON id = mushroom_id;

