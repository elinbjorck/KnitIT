create view test as
select gt.name, count(gtp.id)
from garmenttype as gt
join garmenttypepart as gtp on gt.id = gtp.garmenttypeid
where gtp.Required = 1
group by gt.id
