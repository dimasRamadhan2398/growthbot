#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE tenant_db;
    CREATE DATABASE catalog_db;
    CREATE DATABASE order_db;
    CREATE DATABASE crm_db;
    CREATE DATABASE kb_db;
EOSQL
