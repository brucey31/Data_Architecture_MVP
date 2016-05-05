drop table ab_tests.kinesis_test;

create table ab_tests.kinesis_test (
uid int,
event varchar(50),
timestamp timestamp,
unit varchar(50),
package varchar(15),
price float,
platform varchar(10)
);

select * from 
ab_tests.kinesis_test ;