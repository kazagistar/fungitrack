SELECT Genus,
       Species,
       Variety,
       Edible,
       Color_desc,
       Shape_desc,
       Gill_attatchment_desc,
       Spore_surface_desc,
       Link,
       Description
FROM MUSHROOM
LEFT OUTER JOIN SPORE_COLOR
  ON Color_id = Spore_color_id
LEFT OUTER JOIN CAP_SHAPE
  ON Shape_id = Cap_shape_id
LEFT OUTER JOIN GILL_ATTATCHMENT
  ON GILL_ATTATCHMENT.Gill_attatchment_id = MUSHROOM.Gill_attatchment_id
LEFT OUTER JOIN SPORE_SURFACE
  ON SPORE_SURFACE.Spore_surface_id = MUSHROOM.Spore_surface_id
WHERE Mushroom_id = %s
