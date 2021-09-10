select ap.id, c.char_name, c.playerid, c.id, g.name, g.guildid, 'TeleportPlayer ' || ap.x || ' ' || ap.y || ' ' || ap.z 
from actor_position as ap 
inner join buildings as b on ap.id = b.object_id 
left outer join characters as c on c.id = b.owner_id 
left outer join guilds as g on g.guildid = b.owner_id 
inner join building_instances as bi on bi.object_id = b.object_id 
where bi.instance_id = '0' and bi.object_id not in (select object_id from building_instances where instance_id = '1')
and ap.class like '%found%';