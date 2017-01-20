drop view snowplow_frontend_events;


create view snowplow_frontend_events as
select dvce_created_tstamp as timestamp,
user_id as uid,
app_id,
app_version,
platform_name as platform,
event,
interface_language,
language_learnt,
role,
param.*
from snowplow_events event
left join snowplow_params param
on trim(param.event_name) = trim(event.event_id);