#! /usr/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dbname>"
    exit;
fi

# Database prep
cd sql
psql -f create_tables.sql $1 
cd ..

# Install the wsgi files
cp -R src/* $HOME/wsgi
