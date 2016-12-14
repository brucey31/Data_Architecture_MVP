create view snowplow_frontend_events as
select dvce_created_tstamp as timestamp, 
user_id, 
app_id, 
app_version, 
platform_name as platform, 
event, 
interface_language, 
language_learnt, 
role, 
param.*
from snowplow_events event
inner join snowplow_params param 
on trim(param.event_name) = trim(event.event_id);