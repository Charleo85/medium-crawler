#!/bin/bash

echo 'cleaning up your psql datebase'

psql mediumpro -c "drop table article; drop table sentence; drop table paragraph; drop table comment; drop table author; drop table highlight; drop table topic;"
