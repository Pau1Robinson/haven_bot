SELECT pb.name AS Owner, COUNT(bi.instance_id) AS 'Pieces'
from buildings as b 
INNER JOIN building_instances bi ON bi.object_id = b.object_id
INNER JOIN ( SELECT guildid AS pb_id, name FROM guilds
UNION SELECT id, char_name 
FROM characters ) pb ON b.owner_id = pb_id 
where owner_id in (select guildid from guilds 
where guildid not in (select distinct guild from characters 
where lastTimeOnline > strftime('%s', 'now', '100 days') and guild is not null)
UNION select id from characters 
where lastTimeOnline < strftime('%s', 'now', '100 days') and guild is null) GROUP BY Owner ORDER BY Pieces DESC;