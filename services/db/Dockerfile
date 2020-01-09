FROM monetdb/monetdb

COPY createdb.sql .

RUN rm -rf ${DB_FARM}/benchmarks

RUN monetdbd start $DB_FARM \
    && monetdb create benchmarks \
    && monetdb release benchmarks \
    && mclient -d benchmarks createdb.sql 

EXPOSE 50000

CMD ["monetdbd", "start", "-n", "/var/monetdb5/dbfarm"]