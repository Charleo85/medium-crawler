#!/bin/bash

echo 'cleaning up your psql datebase'

psql medium -c "drop table article; drop table stn; drop table paragraph; drop table comment; drop table author; drop table highlight; drop table topic;"
