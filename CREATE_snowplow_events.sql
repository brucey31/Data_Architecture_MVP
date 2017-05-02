drop table snowplow_events;
CREATE TABLE snowplow_events (
	-- App
	app_id varchar(255) encode text255,
	platform varchar(255) encode text255,
	-- Date/time
	etl_tstamp timestamp,
	collector_tstamp timestamp not null,
	dvce_created_tstamp timestamp,
	-- Event
	event_type varchar(128) encode text255,
	event_id varchar(max) not null unique,
	txn_id int,
	-- Namespacing and versioning
	name_tracker varchar(128) encode text255,
	v_tracker varchar(100) encode text255,
	v_collector varchar(100) encode text255 not null,
	v_etl varchar(100) encode text255 not null,
	-- User and visit
	user_id varchar(255) encode runlength,
	user_ipaddress varchar(45) encode runlength,
	user_fingerprint varchar(50) encode runlength,
	domain_userid varchar(36) encode runlength,
	domain_sessionidx smallint,
	network_userid varchar(38),
	-- Location
	geo_country char(2) encode runlength,
	geo_region char(2) encode runlength,
	geo_city varchar(75) encode runlength,
	geo_zipcode varchar(15) encode runlength,
	geo_latitude double precision encode runlength,
	geo_longitude double precision encode runlength,
	geo_region_name varchar(100) encode runlength,
	-- IP lookups
	ip_isp varchar(100) encode runlength,
	ip_organization varchar(100) encode runlength,
	ip_domain varchar(100) encode runlength,
	ip_netspeed varchar(100) encode runlength,
	-- Page
	page_url varchar(4096),
	page_title varchar(2000),
	page_referrer varchar(4096),
	-- Page URL components
	page_urlscheme varchar(16) encode text255,
	page_urlhost varchar(255) encode text255,
	page_urlport int,
	page_urlpath varchar(3000) encode text32k,
	page_urlquery varchar(6000),
	page_urlfragment varchar(3000),
	-- Referrer URL components
	refr_urlscheme varchar(16) encode text255,
	refr_urlhost varchar(255) encode text255,
	refr_urlport int,
	refr_urlpath varchar(6000) encode text32k,
	refr_urlquery varchar(6000),
	refr_urlfragment varchar(3000),
	-- Referrer details
	refr_medium varchar(25) encode text255,
	refr_source varchar(50) encode text255,
	refr_term varchar(255) encode raw,
	-- Marketing
	mkt_medium varchar(255) encode text255,
	mkt_source varchar(255) encode text255,
	mkt_term varchar(255) encode raw,
	mkt_content varchar(500) encode raw,
	mkt_campaign varchar(255) encode text32k,
	-- Custom structured event
	event varchar(1000),
	interface_language varchar(1000) ,
	language_learnt varchar(1000) ,
	application_id varchar(max) ,
	user_agent varchar(max),
	-- Ecommerce
	role varchar(max) encode raw,
	idfa varchar(max) ,
	environment varchar(max),
	platform_name varchar(max),
	app_version varchar(max),
	tr_city varchar(255) encode text32k,
	tr_state varchar(255) encode text32k,
	tr_country varchar(255) encode text32k,
	ti_orderid varchar(255) encode raw,
	ti_sku varchar(255) encode text32k,
	ti_name varchar(255) encode text32k,
	ti_category varchar(255) encode text255,
	ti_price varchar(max),
	ti_quantity int,
	-- Page ping
	pp_xoffset_min float,
	pp_xoffset_max integer,
	pp_yoffset_min integer,
	pp_yoffset_max integer,
	-- User Agent
	useragent varchar(1000) encode text32k,
	-- Browser
	br_name varchar(50) encode text255,
	br_family varchar(max),
	br_version varchar(50) encode text255,
	br_type varchar(50) encode text255,
	br_renderengine varchar(50) encode text255,
	br_lang varchar(255),
	br_features_pdf boolean,
	br_features_flash varchar(max),
	br_features_java boolean,
	br_features_director boolean,
	br_features_quicktime boolean,
	br_features_realplayer boolean,
	br_features_windowsmedia boolean,
	br_features_gears boolean ,
	br_features_silverlight boolean,
	br_cookies boolean,
	br_colordepth varchar(12) encode text255,
	br_viewwidth integer,
	br_viewheight integer,
	-- Operating System
	os_name varchar(50) encode text255,
	os_family varchar(50)  encode text255,
	os_manufacturer varchar(50)  encode text255,
	os_timezone varchar(255)  encode text255,
	-- Device/Hardware
	dvce_type varchar(50)  encode text255,
	dvce_ismobile varchar(250),
	dvce_screenwidth integer,
	dvce_screenheight integer,
	-- Document
	doc_charset varchar(128) encode text255,
	doc_width integer,
	doc_height integer,

	-- Currency
	tr_currency char(3) encode bytedict,
	tr_total_base dec(18, 2),
	tr_tax_base varchar(max),
	tr_shipping_base dec(18, 2),
	ti_currency char(3) encode bytedict,
	ti_price_base dec(18, 2),
	base_currency char(3) encode bytedict,

	-- Geolocation
	geo_timezone varchar(64),

	-- Click ID
	mkt_clickid varchar(128) encode raw,
	mkt_network varchar(64) encode text255,

	-- ETL tags
	etl_tags varchar(500) encode lzo,

	-- Time event was sent
	dvce_sent_tstamp timestamp,

	-- Referer
	refr_domain_userid varchar(36),
	refr_dvce_tstamp timestamp,

	-- Session ID
	domain_sessionid char(36) encode raw,

	-- Derived timestamp
	derived_tstamp timestamp,

	-- Event schema
	event_vendor varchar(max) encode lzo,
	event_name varchar(max) encode lzo,
	event_format varchar(max) encode lzo,
	event_version varchar(max) encode lzo,

	-- Event fingerprint
	event_fingerprint varchar(max) encode lzo,

	-- True timestamp
	true_tstamp varchar(max),
	version varchar(max),
	bs varchar(max),
	bs2 varchar(max),

	CONSTRAINT event_id_080_pk PRIMARY KEY(event_id)
)
DISTSTYLE KEY
DISTKEY (user_id)
SORTKEY (event_id, collector_tstamp);
