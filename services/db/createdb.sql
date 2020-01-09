create schema results;
set schema results;

drop table if exists experiments cascade;

create table experiments(
    id bigserial,
    host_id integer,
    software_id int,
    name text,              -- TPC-H, ATRAF, TPC-DS, or any other benchmark description
    changeset char(40),
    sf float,               -- in GB
	policy  text,           -- horizontal, vertical number of channels etc
	dbname string,
    tags varchar(256),
    comment text,           
    start_time timestamp,
    end_time timestamp,
    inserted_at timestamp default NOW
);


-- Each experiment has many executions: For one TPC-H SF-10 experiment there
-- might be 22 queries * 5 runs of each query = 110 rows in this table.
drop table if exists executions cascade;
create table executions (
    id bigserial,
    experiment_id bigint,
	query_id int,               -- FK refers to query table
    description text,           -- A description as simple as "Q1", or as elaborative as "mclient -d SF-10 q1.sql"
    repeat int,                 -- Which repeated execution is this?
    sqlparser float,
    maloptimizer float,
    execution float,
    clk float,                  -- in seconds
	trace string                -- Either a blob or a pointer to the fs
);

drop table if exists query cascade;
create table query (
	id serial,
	experiment_id bigint,
    name string,
	query_text text,
	explain text,
	plan text
);

drop table if exists software cascade;
create table software(
    id serial,
    commercial_name varchar(128),
    version varchar(128)            -- Could be something like Nov2019-SP1, 12.1, or a SHA-1
);

drop table if exists hosts cascade;
create table hosts(
    id serial,
    host_name text,
	ram float,              -- in GB
	cpu string,             -- CPU model
    num_cores int,          
	disk_type string,       -- maybe a new datatype
    description string
);

alter table experiments
add constraint hostkey foreign key (host_id) references hosts(id)
on delete cascade;

alter table experiments
add constraint softwarekey foreign key (software_id) references software(id)
on delete cascade;

alter table executions
add constraint execution_experimentkey foreign key (experiment_id) references experiments(id)
on delete cascade;

alter table executions
add constraint querykey foreign key (query_id) references query(id);

alter table query 
add constraint query_experimentkey foreign key (experiment_id) references experiments(id)
on delete cascade;

-- legacy
-- create table timings.tpch (
--     benchmark string,
--     sf float,
--     changeset string,
--     dbname string,
--     query integer,
--     run integer,
--     sqlparser float,
--     maloptimizer float,
--     execution float,
--     clk float,
--     modifier string,
--     hostname string default NULL,
--     inserted_at timestamp default NOW
-- );

-- alter table timings.tpch add constraint "tblnm_uc" UNIQUE ("changeset");
