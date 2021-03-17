select p.name, count(c.id)
from part as p
join construction as c on p.ID = c.PartID
group by c.PartID