dbname=$1
dbuser=$2
dbhost=$3
# note hostname ignored now to avoid password prompt
psql -U $dbuser -t -d $dbname -c "SELECT 'DROP TABLE ' || n.nspname || '.' ||
c.relname || ' CASCADE;' FROM pg_catalog.pg_class AS c LEFT JOIN
pg_catalog.pg_namespace AS n ON n.oid = c.relnamespace WHERE relkind =
'r' AND n.nspname NOT IN ('pg_catalog', 'pg_toast') AND
pg_catalog.pg_table_is_visible(c.oid)"  >/tmp/droptables
psql -U $dbuser -d $dbname -f /tmp/droptables
