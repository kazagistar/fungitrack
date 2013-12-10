SELECT MUSHROOM.Mushroom_id, Found_lat, Found_long, Found_date, Quantity, Genus, Species, Variety 
FROM MUSHROOM_FIND JOIN MUSHROOM ON MUSHROOM.Mushroom_id = MUSHROOM_FIND.Mushroom_id
WHERE (ACOS(SIN(%s)
           * SIN(Found_lat) 
           + COS(%s) 
           * COS(Found_long) 
           * COS(%s - Found_long)
           ) * 6378.1) < %s;