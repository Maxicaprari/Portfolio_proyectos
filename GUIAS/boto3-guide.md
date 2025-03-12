# Guía Completa de Boto3 para Data Sources y Data Pipelines

## 1. Introducción a Boto3

### 1.1 ¿Qué es Boto3?
Boto3 es el SDK (Software Development Kit) oficial de AWS para Python. Proporciona una interfaz orientada a objetos y de bajo nivel para interactuar con los servicios de Amazon Web Services. Para ingeniería de datos, Boto3 es crucial ya que permite acceder programáticamente a servicios como S3, Glue, Athena, Redshift, DynamoDB, entre otros.

### 1.2 Ventajas de Boto3 para Data Pipelines
- **Interfaz Python nativa**: Integración fluida con ecosistemas de datos basados en Python
- **Cobertura completa**: Acceso a todos los servicios de AWS relevantes para datos
- **Dos niveles de APIs**:
  - Recursos (alto nivel, orientada a objetos)
  - Clientes (bajo nivel, mapeo directo a las operaciones de API)
- **Soporte para paginación**: Manejo eficiente de grandes conjuntos de datos
- **Soporte para paralelismo**: Operaciones asíncronas y concurrentes
- **Integración con herramientas de desarrollo**: Compatibilidad con entornos como Jupyter, PyCharm, etc.

### 1.3 Casos de uso para Data Engineering
- ETL/ELT con datos en S3, Redshift, DynamoDB
- Procesamiento distribuido con EMR
- Automatización de procesos de datos
- Orquestación con Step Functions y Lambda
- Data lakes con servicios como Glue y Lake Formation
- Streaming de datos con Kinesis
- Análisis ad-hoc con Athena

## 2. Configuración e Instalación

### 2.1 Instalación
```bash
# Instalación básica
pip install boto3

# Instalación con dependencias específicas
pip install boto3[crt]  # Para el modo de transferencia acelerada S3
```

### 2.2 Configuración de credenciales
```python
# Método 1: Configuración explícita
import boto3

session = boto3.Session(
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='us-east-1'
)

# Método 2: Archivo ~/.aws/credentials
"""
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = us-east-1

[project-prod]
aws_access_key_id = PROD_ACCESS_KEY
aws_secret_access_key = PROD_SECRET_KEY
region = us-west-2
"""

# Uso de perfil específico
session = boto3.Session(profile_name='project-prod')

# Método 3: Variables de entorno
# export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
# export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
# export AWS_DEFAULT_REGION=us-east-1

# Método 4: Credenciales temporales con STS
sts_client = boto3.client('sts')
assumed_role = sts_client.assume_role(
    RoleArn="arn:aws:iam::123456789012:role/DataEngineerRole",
    RoleSessionName="AssumedRoleSession"
)
credentials = assumed_role['Credentials']

session = boto3.Session(
    aws_access_key_id=credentials['AccessKeyId'],
    aws_secret_access_key=credentials['SecretAccessKey'],
    aws_session_token=credentials['SessionToken']
)
```

### 2.3 Configuración de sesiones y clientes
```python
# Creación de sesión
session = boto3.Session(region_name='us-east-1')

# Creación de cliente desde sesión
s3_client = session.client('s3')

# Creación de recurso desde sesión
s3_resource = session.resource('s3')

# Método directo (usa configuración predeterminada)
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
```

### 2.4 Configuraciones avanzadas
```python
# Configuración de proxy
s3_client = boto3.client(
    's3',
    region_name='us-east-1',
    config=boto3.session.Config(
        proxies={'http': 'http://proxy.example.com:8080'}
    )
)

# Configuración de timeout y retries
s3_client = boto3.client(
    's3',
    config=boto3.session.Config(
        connect_timeout=5,
        read_timeout=60,
        retries={'max_attempts': 10}
    )
)
```

## 3. Trabajando con Amazon S3 para Data Lakes

### 3.1 Operaciones básicas con S3
```python
import boto3

s3 = boto3.client('s3')

# Listar buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(f"Bucket: {bucket['Name']}")

# Crear un bucket
s3.create_bucket(
    Bucket='my-data-lake',
    CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
)

# Listar objetos en un bucket
response = s3.list_objects_v2(Bucket='my-data-lake', Prefix='raw/customers/')
for obj in response.get('Contents', []):
    print(f"Object: {obj['Key']}, Size: {obj['Size']} bytes")

# Subir un archivo
s3.upload_file(
    Filename='local_data.csv',
    Bucket='my-data-lake',
    Key='raw/customers/data.csv'
)

# Descargar un archivo
s3.download_file(
    Bucket='my-data-lake',
    Key='raw/customers/data.csv',
    Filename='downloaded_data.csv'
)

# Eliminar un objeto
s3.delete_object(
    Bucket='my-data-lake',
    Key='raw/customers/old_data.csv'
)
```

### 3.2 Uso de recursos de alto nivel para S3
```python
s3 = boto3.resource('s3')

# Acceder a un bucket
bucket = s3.Bucket('my-data-lake')

# Listar objetos
for obj in bucket.objects.filter(Prefix='raw/customers/'):
    print(f"Object: {obj.key}, Size: {obj.size} bytes")

# Subir un archivo
bucket.upload_file('local_data.csv', 'raw/customers/data.csv')

# Descargar un archivo
bucket.download_file('raw/customers/data.csv', 'downloaded_data.csv')

# Acceder a un objeto específico
obj = s3.Object('my-data-lake', 'raw/customers/data.csv')
content = obj.get()['Body'].read().decode('utf-8')
```

### 3.3 Operaciones avanzadas con S3
```python
# Copiar objetos entre buckets
s3.copy_object(
    CopySource={'Bucket': 'source-bucket', 'Key': 'source-key'},
    Bucket='target-bucket',
    Key='target-key'
)

# Generar URL prefirmada (para acceso temporal)
presigned_url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-data-lake', 'Key': 'confidential/report.pdf'},
    ExpiresIn=3600  # 1 hora
)

# Configurar versionado en un bucket
s3.put_bucket_versioning(
    Bucket='my-data-lake',
    VersioningConfiguration={'Status': 'Enabled'}
)

# Listar versiones de un objeto
versions = s3.list_object_versions(
    Bucket='my-data-lake',
    Prefix='raw/customers/data.csv'
)
```

### 3.4 Manejo eficiente de datos grandes
```python
# Transferencia multiparte para archivos grandes
from boto3.s3.transfer import TransferConfig

config = TransferConfig(
    multipart_threshold=1024 * 25,  # 25 MB
    max_concurrency=10,
    multipart_chunksize=1024 * 25,  # 25 MB
    use_threads=True
)

s3.upload_file(
    'massive_dataset.parquet',
    'my-data-lake',
    'processed/customers_all.parquet',
    Config=config
)

# Streaming de datos a S3
import io
import pandas as pd

df = pd.DataFrame({'id': range(1000), 'value': range(1000)})
buffer = io.BytesIO()
df.to_parquet(buffer)
buffer.seek(0)

s3.put_object(
    Bucket='my-data-lake',
    Key='processed/customers_stream.parquet',
    Body=buffer.getvalue()
)

# Streaming de datos desde S3
obj = s3.get_object(Bucket='my-data-lake', Key='processed/customers_stream.parquet')
df = pd.read_parquet(io.BytesIO(obj['Body'].read()))
```

### 3.5 S3 Select para consultas en el servidor
```python
# Consultar directamente datos CSV en S3
response = s3.select_object_content(
    Bucket='my-data-lake',
    Key='raw/customers/large_file.csv',
    ExpressionType='SQL',
    Expression="SELECT s.id, s.name FROM S3Object s WHERE s.age > 30",
    InputSerialization={'CSV': {'FileHeaderInfo': 'Use'}},
    OutputSerialization={'CSV': {}}
)

# Procesar resultados
for event in response['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)

# Consultar datos Parquet
response = s3.select_object_content(
    Bucket='my-data-lake',
    Key='processed/customers.parquet',
    ExpressionType='SQL',
    Expression="SELECT * FROM S3Object s LIMIT 10",
    InputSerialization={'Parquet': {}},
    OutputSerialization={'JSON': {}}
)
```

## 4. AWS Glue para Catálogo y ETL

### 4.1 Trabajando con el catálogo de datos
```python
glue = boto3.client('glue')

# Crear una base de datos
glue.create_database(
    DatabaseInput={
        'Name': 'retail_data',
        'Description': 'Database for retail data analytics'
    }
)

# Listar bases de datos
databases = glue.get_databases()
for db in databases['DatabaseList']:
    print(f"Database: {db['Name']}")

# Crear una tabla
glue.create_table(
    DatabaseName='retail_data',
    TableInput={
        'Name': 'customers',
        'StorageDescriptor': {
            'Columns': [
                {'Name': 'id', 'Type': 'int'},
                {'Name': 'name', 'Type': 'string'},
                {'Name': 'email', 'Type': 'string'}
            ],
            'Location': 's3://my-data-lake/raw/customers/',
            'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
            'SerdeInfo': {
                'SerializationLibrary': 'org.apache.hadoop.hive.serde2.OpenCSVSerde',
            }
        },
        'TableType': 'EXTERNAL_TABLE',
    }
)

# Actualizar esquema de tabla
glue.update_table(
    DatabaseName='retail_data',
    TableInput={
        'Name': 'customers',
        'StorageDescriptor': {
            'Columns': [
                {'Name': 'id', 'Type': 'int'},
                {'Name': 'name', 'Type': 'string'},
                {'Name': 'email', 'Type': 'string'},
                {'Name': 'signup_date', 'Type': 'date'}  # Nueva columna
            ],
            # Resto de configuración igual
        }
    }
)

# Obtener detalles de tabla
table = glue.get_table(DatabaseName='retail_data', Name='customers')
print(f"Tabla: {table['Table']['Name']}")
print(f"Ubicación: {table['Table']['StorageDescriptor']['Location']}")
```

### 4.2 Ejecución de crawlers
```python
# Crear un crawler
glue.create_crawler(
    Name='retail_customers_crawler',
    Role='arn:aws:iam::123456789012:role/GlueServiceRole',
    DatabaseName='retail_data',
    Targets={
        'S3Targets': [
            {'Path': 's3://my-data-lake/raw/customers/'}
        ]
    },
    Schedule='cron(0 0 * * ? *)',  # Diariamente a medianoche
    SchemaChangePolicy={
        'UpdateBehavior': 'UPDATE_IN_DATABASE',
        'DeleteBehavior': 'LOG'
    }
)

# Iniciar crawler manualmente
glue.start_crawler(Name='retail_customers_crawler')

# Verificar estado del crawler
response = glue.get_crawler(Name='retail_customers_crawler')
print(f"Estado: {response['Crawler']['State']}")

# Listar crawlers
crawlers = glue.get_crawlers()
for crawler in crawlers['Crawlers']:
    print(f"Crawler: {crawler['Name']}, Estado: {crawler['State']}")
```

### 4.3 Trabajando con Glue ETL Jobs
```python
# Crear un job de ETL
job_name = 'customer_data_transform'
glue.create_job(
    Name=job_name,
    Role='arn:aws:iam::123456789012:role/GlueServiceRole',
    Command={
        'Name': 'glueetl',
        'ScriptLocation': 's3://my-scripts/glue/customer_transform.py',
        'PythonVersion': '3'
    },
    DefaultArguments={
        '--job-language': 'python',
        '--job-bookmark-option': 'job-bookmark-enable',
        '--TempDir': 's3://my-data-lake/temp/',
        '--source_database': 'retail_data',
        '--source_table': 'customers',
        '--target_path': 's3://my-data-lake/processed/customers/'
    },
    MaxRetries=2,
    Timeout=2880,  # 48 horas
    GlueVersion='3.0',
    NumberOfWorkers=5,
    WorkerType='G.1X'
)

# Iniciar ejecución de job
job_run_id = glue.start_job_run(JobName=job_name)['JobRunId']
print(f"Job iniciado con ID: {job_run_id}")

# Obtener estado de ejecución
response = glue.get_job_run(JobName=job_name, RunId=job_run_id)
print(f"Estado: {response['JobRun']['JobRunState']}")

# Listar todas las ejecuciones de un job
job_runs = glue.get_job_runs(JobName=job_name)
for run in job_runs['JobRuns']:
    print(f"Run ID: {run['Id']}, Estado: {run['JobRunState']}")
```

### 4.4 Definiendo particiones dinámicamente
```python
# Crear una tabla particionada
glue.create_table(
    DatabaseName='retail_data',
    TableInput={
        'Name': 'sales',
        'StorageDescriptor': {
            'Columns': [
                {'Name': 'transaction_id', 'Type': 'string'},
                {'Name': 'customer_id', 'Type': 'int'},
                {'Name': 'amount', 'Type': 'double'}
            ],
            'Location': 's3://my-data-lake/raw/sales/',
            'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
            'SerdeInfo': {
                'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe',
            }
        },
        'PartitionKeys': [
            {'Name': 'year', 'Type': 'string'},
            {'Name': 'month', 'Type': 'string'},
            {'Name': 'day', 'Type': 'string'}
        ],
        'TableType': 'EXTERNAL_TABLE',
    }
)

# Agregar una partición
glue.create_partition(
    DatabaseName='retail_data',
    TableName='sales',
    PartitionInput={
        'Values': ['2023', '01', '15'],
        'StorageDescriptor': {
            'Location': 's3://my-data-lake/raw/sales/year=2023/month=01/day=15/',
            # Resto de la configuración igual a la tabla
        }
    }
)

# Agregar múltiples particiones
partitions = [
    {
        'Values': ['2023', '01', '16'],
        'StorageDescriptor': {
            'Location': 's3://my-data-lake/raw/sales/year=2023/month=01/day=16/',
            # Resto de configuración
        }
    },
    {
        'Values': ['2023', '01', '17'],
        'StorageDescriptor': {
            'Location': 's3://my-data-lake/raw/sales/year=2023/month=01/day=17/',
            # Resto de configuración
        }
    }
]

glue.batch_create_partition(
    DatabaseName='retail_data',
    TableName='sales',
    PartitionInputList=partitions
)
```

## 5. Amazon Athena para Análisis de Datos

### 5.1 Ejecución de consultas con Athena
```python
athena = boto3.client('athena')
s3_output = 's3://my-query-results/athena/'

# Ejecutar consulta
query = "SELECT * FROM retail_data.customers LIMIT 10"
response = athena.start_query_execution(
    QueryString=query,
    QueryExecutionContext={
        'Database': 'retail_data'
    },
    ResultConfiguration={
        'OutputLocation': s3_output
    }
)

query_execution_id = response['QueryExecutionId']
print(f"Query ID: {query_execution_id}")

# Verificar estado de la consulta
def get_query_status(query_id):
    response = athena.get_query_execution(QueryExecutionId=query_id)
    return response['QueryExecution']['Status']['State']

# Esperar a que la consulta termine
import time
status = get_query_status(query_execution_id)
while status in ['QUEUED', 'RUNNING']:
    time.sleep(1)
    status = get_query_status(query_execution_id)

if status == 'SUCCEEDED':
    # Obtener resultados
    results = athena.get_query_results(QueryExecutionId=query_execution_id)
    
    # Procesar resultados
    headers = [col['Label'] for col in results['ResultSet']['ResultSetMetadata']['ColumnInfo']]
    rows = results['ResultSet']['Rows'][1:]  # Primera fila son encabezados
    
    # Convertir a DataFrame de Pandas
    import pandas as pd
    data = []
    for row in rows:
        values = [field.get('VarCharValue', '') for field in row['Data']]
        data.append(dict(zip(headers, values)))
    
    df = pd.DataFrame(data)
    print(df.head())
else:
    print(f"La consulta falló con estado: {status}")
```

### 5.2 Gestión de consultas programadas
```python
# Crear un grupo de trabajo
athena.create_work_group(
    Name='data_analysts',
    Configuration={
        'ResultConfiguration': {
            'OutputLocation': 's3://my-query-results/data_analysts/'
        },
        'EnforceWorkGroupConfiguration': True,
        'PublishCloudWatchMetricsEnabled': True,
        'BytesScannedCutoffPerQuery': 10737418240,  # 10 GB
        'RequesterPaysEnabled': False
    },
    Description='Workgroup for data analysts team'
)

# Ejecutar consulta en un grupo de trabajo específico
response = athena.start_query_execution(
    QueryString="SELECT * FROM retail_data.sales WHERE year='2023' AND month='01'",
    QueryExecutionContext={
        'Database': 'retail_data'
    },
    ResultConfiguration={
        'OutputLocation': 's3://my-query-results/athena/'
    },
    WorkGroup='data_analysts'
)

# Listar consultas en un grupo de trabajo
queries = athena.list_query_executions(WorkGroup='data_analysts')
for query_id in queries.get('QueryExecutionIds', []):
    details = athena.get_query_execution(QueryExecutionId=query_id)
    query = details['QueryExecution']
    print(f"Query: {query_id}")
    print(f"SQL: {query['Query']}")
    print(f"Estado: {query['Status']['State']}")
    print(f"Tiempo: {query['Statistics']['TotalExecutionTimeInMillis']} ms")
    print(f"Datos escaneados: {query['Statistics']['DataScannedInBytes']} bytes")
```

### 5.3 Creación de vistas en Athena
```python
# Crear una vista
view_query = """
CREATE OR REPLACE VIEW retail_data.active_customers AS
SELECT c.id, c.name, c.email
FROM retail_data.customers c
JOIN retail_data.sales s ON c.id = s.customer_id
WHERE s.year = '2023' AND s.month = '01'
GROUP BY 1, 2, 3
HAVING COUNT(*) > 0
"""

athena.start_query_execution(
    QueryString=view_query,
    QueryExecutionContext={
        'Database': 'retail_data'
    },
    ResultConfiguration={
        'OutputLocation': 's3://my-query-results/athena/'
    }
)

# Consultar la vista
query = "SELECT * FROM retail_data.active_customers LIMIT 10"
# Ejecutar como en ejemplos anteriores
```

### 5.4 Consultas parametrizadas
```python
def run_parametrized_query(year, month, min_amount):
    # Usar SQL parametrizado evitando inyección SQL
    query = f"""
    SELECT 
        customer_id, 
        COUNT(*) as transaction_count, 
        SUM(amount) as total_amount
    FROM 
        retail_data.sales
    WHERE 
        year = '{year}' AND 
        month = '{month}' AND
        amount >= {min_amount}
    GROUP BY 
        customer_id
    ORDER BY 
        total_amount DESC
    LIMIT 100
    """
    
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': 'retail_data'},
        ResultConfiguration={'OutputLocation': 's3://my-query-results/athena/'}
    )
    return response['QueryExecutionId']

# Ejecutar para parámetros específicos
query_id = run_parametrized_query('2023', '01', 100.0)
```

## 6. Amazon Redshift para Data Warehousing

### 6.1 Conexión y operaciones básicas
```python
redshift = boto3.client('redshift-data')
cluster_id = 'my-redshift-cluster'
database = 'retail_warehouse'
db_user = 'admin'

# Ejecutar consulta SQL
response = redshift.execute_statement(
    ClusterIdentifier=cluster_id,
    Database=database,
    DbUser=db_user,
    Sql="SELECT * FROM customers LIMIT 10"
)

statement_id = response['Id']
print(f"Statement ID: {statement_id}")

# Verificar estado de la consulta
status_response = redshift.describe_statement(Id=statement_id)
status = status_response['Status']
print(f"Estado: {status}")

# Obtener resultados cuando esté listo
if status == 'FINISHED':
    results = redshift.get_statement_result(Id=statement_id)
    
    # Procesar resultados
    columns = [col['name'] for col in results['ColumnMetadata']]
    rows = []
    for record in results['Records']:
        row = {}
        for i, col in enumerate(columns):
            row[col] = record[i].get('stringValue', 
                       record[i].get('longValue', 
                       record[i].get('doubleValue')))
        rows.append(row)
    
    import pandas as pd
    df = pd.DataFrame(rows)
    print(df.head())
```

### 6.2 Carga y descarga de datos con Redshift
```python
# Copiar datos de S3 a Redshift
copy_query = f"""
COPY customers
FROM 's3://my-data-lake/processed/customers/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftLoadRole'
FORMAT AS PARQUET;
"""

redshift.execute_statement(
    ClusterIdentifier=cluster_id,
    Database=database,
    DbUser=db_user,
    Sql=copy_query
)

# Descargar datos de Redshift a S3
unload_query = f"""
UNLOAD ('SELECT * FROM customers WHERE signup_date >= ''2023-01-01''')
TO 's3://my-data-lake/exports/new_customers/'
IAM_ROLE 'arn:aws:iam::123456789012:role/RedshiftUnloadRole'
FORMAT PARQUET
PARTITIONED BY (signup_date);
"""

redshift.execute_statement(
    ClusterIdentifier=cluster_id,
    Database=database,
    DbUser=db_user,
    Sql=unload_query
)
```

### 6.3 Ejecutar consultas en lotes
```python
# Ejecutar múltiples consultas en batch
queries = [
    "UPDATE customers SET status = 'active' WHERE last_purchase_date >= CURRENT_DATE - INTERVAL '30' DAY;",
    "UPDATE customers SET status = 'inactive' WHERE last_purchase_date < CURRENT_DATE - INTERVAL '90' DAY;",
    "INSERT INTO customer_metrics SELECT customer_id, COUNT(*), SUM(amount) FROM sales GROUP BY 1;"
]

batch_response = redshift.batch_execute_statement(
    ClusterIdentifier=cluster_id,
    Database=database,
    DbUser=db_user,
    Sqls=queries
)

for statement_id in batch_response['Ids']:
    print(f"Statement ID en batch: {statement_id}")
```

### 6.4 Administración de clusters
```python
redshift_client = boto3.client('redshift')

# Describir clusters
clusters = redshift_client.describe_clusters()
for cluster in clusters['Clusters']:
    print(f"Cluster: {cluster['ClusterIdentifier']}")
    print(f"Estado: {cluster['ClusterStatus']}")
    print(f"Tipo de nodo: {cluster['NodeType']}")
    print(f"Nodos: {cluster['NumberOfNodes']}")

# Modificar un cluster (escalamiento)
redshift_client.resize_cluster(
    ClusterIdentifier=cluster_id,
    NodeType='dc2.8xlarge',
    NumberOfNodes=8,
    Classic=False
)

# Crear snapshot
redshift_client.create_cluster_snapshot(
    SnapshotIdentifier='pre-etl-snapshot',
    ClusterIdentifier=cluster_id,
    Tags=[
        {'Key': 'Purpose', 'Value': 'Pre-ETL-Backup'},
        {'Key': 'Environment', 'Value': 'Production'}
    ]
)

# Listar snapshots
snapshots = redshift_client.describe_cluster_snapshots(
    ClusterIdentifier=cluster_id
)
for snapshot in snapshots['Snapshots']:
    print(f"Snapshot: {snapshot['SnapshotIdentifier']}")
    print(f"Estado: {snapshot['Status']}")
    print(f"Tamaño: {snapshot['TotalBackupSizeInMegaBytes']} MB")
```

## 7. DynamoDB para Procesamiento NoSQL

### 7.1 Operaciones básicas
```python
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('customer_activity')

# Crear tabla
dynamodb_client = boto3.client('dynamodb')
dynamodb_client.create_table(
    TableName='customer_activity',
    KeySchema=[
        {'AttributeName': 'customer_id', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}    # Sort key
    ],
    AttributeDefinitions=[
        {'AttributeName': 'customer_id', 'AttributeType': 'S'},
        {'AttributeName': 'timestamp', 'AttributeType': 'N'}
    ],
    BillingMode='PROVISIONED',
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Insertar ítem
table.put_item(
    Item={
        'customer_id': 'C123456',
        'timestamp': int(time.time()),
        'event_type': 'page_view',
        'page': '/products',
        'device': 'mobile',
        'session_id': 'abcdef123456'
    }
)

# Obtener ítem
response = table.get_item(
    Key={
        'customer_id': 'C123456',
        'timestamp': 1625097600
    }
)
if 'Item' in response:
    item = response['Item']
    print(f"Event: {item.get('event_type')} on page {item.get('page')}")

# Actualizar ítem
table.update_item(
    Key={
        'customer_id': 'C123456',
        'timestamp': 1625097600
    },
    UpdateExpression='SET time_spent = :t, conversion = :c',
    ExpressionAttributeValues={
        ':t': 120,
        ':c': True
    },
    ReturnValues='UPDATED_NEW'
)

# Consultar ítems
response = table.query(
    KeyConditionExpression=boto3.dynamodb.conditions.Key('customer_id').eq('C123456') &
                          boto3.dynamodb.conditions.Key('timestamp').between(1625097600, 1625184000),
    FilterExpression=boto3.dynamodb.conditions.Attr('event_type').eq('purchase')
)