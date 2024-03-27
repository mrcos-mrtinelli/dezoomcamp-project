import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# set the enviroment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/lacity-pipeline-service-acct-credential.json'

bucket_name = ''
project_id = ''
table_name = 'active_businesses'

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(active_businesses_table, *args, **kwargs):
    active_businesses_table['location_start_year'] = active_businesses_table['location_start_date'].dt.year

    table = pa.Table.from_pandas(active_businesses_table)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
    table,
    root_path=root_path,
    partition_cols=['location_start_year'],
    filesystem=gcs
)