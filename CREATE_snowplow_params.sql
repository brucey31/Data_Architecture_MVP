create table snowplow_params(
event_name varchar(max),
param_1 varchar(max),
param_2 varchar(max),
param_3 varchar(max),
param_4 varchar(max),
param_5 varchar(max),
param_6 varchar(max),
param_7 varchar(max),
param_8 varchar(max),
param_9 varchar(max),
param_10 varchar(max)
) DISTSTYLE KEY
DISTKEY (event_name);