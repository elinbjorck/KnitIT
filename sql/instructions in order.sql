SELECT g.id, c.Instructions, gtp.Priority
FROM garment AS g
JOIN garmentconstruction as gc on g.id = gc.garmentID
join construction as c on c.id = gc.ConstructionID
join garmenttypepart as gtp
on gtp.PartID = c.PartID and gtp.GarmentTypeID = g.GarmentTypeID
order by gtp.Priority

