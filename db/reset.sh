#!/bin/bash
rm -f app.db
sqlite3 app.db < db_create.sql