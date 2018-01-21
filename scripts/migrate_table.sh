#!/bin/bash

echo 'migrating your psql datebase'

psql medium -c "ALTER TABLE highlight ADD COLUMN startOffset int, ADD COLUMN endOffset int, ADD COLUMN corrParagraphID int;"
python3 insert2DB.py
psql medium -c "ALTER TABLE highlight DROP COLUMN corrstnmediumids;"
