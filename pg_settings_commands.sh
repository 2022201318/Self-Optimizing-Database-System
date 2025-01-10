echo "
maintenance_work_mem = '1GB'
work_mem = '64MB'
shared_buffers = '1GB'
effective_cache_size = '2GB'
autovacuum_max_workers = 4
max_parallel_workers = 8
max_parallel_workers_per_gather = 8
random_page_cost = 1.1
seq_page_cost = 0.2
fsyncmkdir -p
" >> ~/tmp_master_dir_polardb_pg_1100_bld/postgresql.conf

# Reload PostgreSQL configuration
pg_ctl reload -D ~/tmp_master_dir_polardb_pg_1100_bld
# 或者使用以下命令来重启 PostgreSQL
pg_ctl restart -m fast -D ~/tmp_master_dir_polardb_pg_1100_bld