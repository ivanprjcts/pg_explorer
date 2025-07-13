from django.db import models


class PgClass(models.Model):
    """
    In Postgres, pg_class is a system catalog table that stores information about tables, indexes, sequences, views,
    and other relation-like objects in the database.

    It is one of the core system tables used internally by Postgres to manage metadata about database objects.
    """
    id = models.BigAutoField(primary_key=True, db_column='oid')
    name = models.CharField(max_length=63, db_column='relname')  # max postgres identifier length
    namespace = models.BigIntegerField(db_column='relnamespace')    # references pg_namespace.oid
    type = models.BigIntegerField(db_column='reltype')
    owner = models.BigIntegerField(db_column='relowner')
    kind = models.CharField(
        max_length=1,
        db_column='relkind',
        help_text='r = ordinary table, i = index, S = sequence, t = TOAST table, v = view, m = materialized view, '
                  'c = composite type, f = foreign table, p = partitioned table, I = partitioned index'
        )
    tuples = models.FloatField(db_column='reltuples')
    pages = models.IntegerField(db_column='relpages')
    rel_all_visible = models.IntegerField(db_column='relallvisible')
    has_index = models.BooleanField(db_column='relhasindex')
    is_partition = models.BooleanField(db_column='relispartition')

    class Meta:
        managed = False
        db_table = 'pg_class'
