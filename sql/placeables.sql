select count(b.owner_id) as PlaceableItems, b.owner_id, g.name, g.guildid, c.char_name, c.id, c.playerid
from buildings as b left outer join characters as c on b.owner_id = c.id left outer join guilds as g on b.owner_id = g.guildid
group by owner_id order by PlaceableItems desc;