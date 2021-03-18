create view instructionsInOrder as
select g.id, g.Name, c.Instructions, gtp.Priority
FROM garment as g
join garmentconstruction as gc on g.id = gc.garmentID
join construction as c on c.id = gc.ConstructionID
join garmenttypepart as gtp on c.PartID = gtp.PartID
order by gtp.Priority