SELECT MUSHROOM.Mushroom_id, Found_lat, Found_long, Found_date, Quantity, Genus, Species, Variety 
FROM MUSHROOM_FIND 
JOIN MUSHROOM ON MUSHROOM.Mushroom_id = MUSHROOM_FIND.Mushroom_id
WHERE 6378.1 * SQRT(
                     POW(
                         (RADIANS(%s - Found_long)) 
                         * COS(RADIANS(Found_lat + %s) / 2)
                      ,2) 
                      + POW(RADIANS(%s - Found_lat),2)) < %s