# Guía Completa de Apache Airflow

## 1. Introducción a Apache Airflow

### 1.1 ¿Qué es Apache Airflow?
Apache Airflow es una plataforma de código abierto creada por Airbnb (ahora un proyecto de la Apache Software Foundation) para programar, monitorear y orquestar flujos de trabajo complejos. Permite definir pipelines como código, lo que facilita la creación, programación y monitoreo de flujos de trabajo complejos.

### 1.2 Casos de uso principales
- Procesamiento de datos ETL/ELT
- Orquestación de procesos de machine learning
- Generación y distribución de informes
- Ejecución de trabajos en batch
- Integración con sistemas de terceros
- Automatización de procesos empresariales

### 1.3 Ventajas clave
- **Programación basada en código**: Pipelines como código (Python)
- **Escalabilidad**: Arquitectura distribuida
- **Extensibilidad**: Sistema de plugins y operadores personalizables
- **Interfaz web**: Monitoreo visual y depuración
- **Manejo de dependencias**: Ejecución basada en dependencias entre tareas
- **Retries automáticos**: Recuperación de errores
- **Comunidad activa**: Gran ecosistema de usuarios y contribuidores

## 2. Arquitectura de Airflow

### 2.1 Componentes principales
- **Scheduler**: Orquesta la ejecución de tareas y DAGs
- **Webserver**: Proporciona la interfaz de usuario
- **Metastore**: Base de datos para almacenar metadata (estados, configuraciones, etc.)
- **Executor**: Define cómo se ejecutan las tareas
- **Worker**: Procesa las tareas asignadas por el executor
- **DAG**: Directed Acyclic Graph, el núcleo de la definición de workflows

### 2.2 Flujo de ejecución
1. El scheduler lee los archivos DAG
2. El scheduler crea instancias DAG (DagRuns)
3. El scheduler crea instancias de tareas (TaskInstances)
4. Las tareas pasan a estado "scheduled"
5. El executor asigna tareas a los workers
6. Los workers ejecutan las tareas
7. El executor reporta resultados al scheduler
8. El webserver muestra estado y resultados

### 2.3 Tipos de executors
- **SequentialExecutor**: Ejecuta una tarea a la vez (no para producción)
- **LocalExecutor**: Procesa tareas en paralelo en la máquina local
- **CeleryExecutor**: Distribuye tareas entre múltiples workers
- **KubernetesExecutor**: Ejecuta cada tarea en un pod de Kubernetes
- **DaskExecutor**: Utiliza Dask para ejecución distribuida

## 3. Conceptos Fundamentales

### 3.1 DAGs (Directed Acyclic Graphs)
- Representación del flujo de trabajo
- Define tareas y sus dependencias
- Debe ser acíclico (sin ciclos)
- Configurado con parámetros como schedule_interval, start_date, etc.

### 3.2 Tasks (Tareas)
- Unidad básica de ejecución
- Implementadas mediante operadores
- Tienen un upstream (dependencias) y downstream (dependientes)

### 3.3 Operators (Operadores)
- Encapsulan la lógica de una tarea específica
- Tipos comunes:
  - **BashOperator**: Ejecuta comandos bash
  - **PythonOperator**: Ejecuta funciones Python
  - **EmailOperator**: Envía correos electrónicos
  - **HTTPOperator**: Realiza peticiones HTTP
  - **SQLOperator**: Ejecuta consultas SQL
  - Operadores específicos para proveedores (AWS, GCP, etc.)

### 3.4 Sensors
- Tipo especial de operador que espera por una condición
- Ejemplos: FileSensor, S3KeySensor, ExternalTaskSensor

### 3.5 Hooks
- Interfaces para conectarse a sistemas externos
- Proporcionan abstracción sobre las conexiones

### 3.6 XComs (Cross Communications)
- Mecanismo para intercambiar pequeños mensajes entre tareas
- Almacenados en la base de datos de Airflow

## 4. Instalación y Configuración

### 4.1 Métodos de instalación
- **Pip**: `pip install apache-airflow`
- **Docker**: Imagen oficial de Docker
- **Helm chart**: Para instalación en Kubernetes
- **Astronomer**: Plataforma gestionada basada en Airflow
- **Cloud managed**: Google Cloud Composer, Amazon MWAA

### 4.2 Configuración básica
```ini
[core]
dags_folder = /path/to/dags
base_log_folder = /path/to/logs
executor = LocalExecutor
sql_alchemy_conn = postgresql+psycopg2://user:password@localhost/airflow
load_examples = False

[webserver]
web_server_host = 0.0.0.0
web_server_port = 8080

[scheduler]
child_process_log_directory = /path/to/logs/scheduler
```

### 4.3 Configuración de base de datos
- SQLite (desarrollo)
- PostgreSQL (recomendado para producción)
- MySQL
- MSSQL

### 4.4 Configuración de seguridad
- Autenticación: LDAP, OAuth, Password
- Autorización: Roles y permisos
- Conexiones cifradas
- Variables secretas

## 5. Creación de DAGs y Tareas

### 5.1 Estructura básica de un DAG
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'tutorial',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    t2 = BashOperator(
        task_id='sleep',
        bash_command='sleep 5',
        retries=3,
    )

    t1 >> t2  # Define dependencia: t1 debe ejecutarse antes que t2
```

### 5.2 Definición de dependencias
```python
# Método 1: Operador bitshift
task1 >> task2 >> task3

# Método 2: Método set_downstream/set_upstream
task1.set_downstream(task2)
task3.set_upstream(task2)

# Dependencias múltiples
task1 >> [task2, task3] >> task4
```

### 5.3 Operadores comunes

#### BashOperator
```python
from airflow.operators.bash import BashOperator

task = BashOperator(
    task_id='echo_hello',
    bash_command='echo "Hello World"',
    dag=dag,
)
```

#### PythonOperator
```python
from airflow.operators.python import PythonOperator

def my_python_function(ds, **kwargs):
    print(f"Execution date is {ds}")
    return "Hello from Python"

task = PythonOperator(
    task_id='python_function',
    python_callable=my_python_function,
    dag=dag,
)
```

#### SQLOperator (usando PostgresOperator)
```python
from airflow.providers.postgres.operators.postgres import PostgresOperator

task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_default',
    sql='''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    ''',
)
```

### 5.4 Sensores
```python
from airflow.sensors.filesystem import FileSensor

file_sensor = FileSensor(
    task_id='wait_for_file',
    filepath='/path/to/file',
    poke_interval=30,  # Intervalo en segundos para verificar
    timeout=60 * 60,   # Timeout después de una hora
    mode='poke',       # Modo de operación (poke, reschedule)
)
```

### 5.5 Parámetros de DAGs

#### schedule_interval
```python
# Opciones comunes:
dag = DAG(
    'example',
    schedule_interval='0 0 * * *',  # Cron expression: diariamente a medianoche
    # Alternativas:
    # schedule_interval='@daily',    # Presets: @once, @hourly, @daily, @weekly, @monthly, @yearly
    # schedule_interval=timedelta(days=1),  # Object timedelta
)
```

#### catchup
```python
dag = DAG(
    'example',
    start_date=datetime(2021, 1, 1),
    catchup=False,  # No ejecutar DAGs pendientes históricos
)
```

#### max_active_runs
```python
dag = DAG(
    'example',
    max_active_runs=1,  # Limita a una ejecución activa a la vez
)
```

## 6. Características Avanzadas

### 6.1 TaskFlow API (Airflow 2.0+)
```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    schedule_interval='@daily',
    start_date=datetime(2021, 1, 1),
    catchup=False,
)
def taskflow_example():
    
    @task()
    def extract():
        data = {"a": 1, "b": 2}
        return data
    
    @task()
    def transform(data):
        return {k: v * 10 for k, v in data.items()}
    
    @task()
    def load(data):
        print(f"Result: {data}")
    
    # Define el flujo
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)

dag_instance = taskflow_example()
```

### 6.2 Variables de Airflow
```python
from airflow.models import Variable

# En la interfaz web: Admin > Variables
# En código:
my_var = Variable.get("my_key")
my_json_var = Variable.get("my_json_key", deserialize_json=True)
```

### 6.3 Conexiones
```python
from airflow.hooks.base import BaseHook

# En la interfaz web: Admin > Connections
conn = BaseHook.get_connection('my_conn_id')
conn_uri = conn.get_uri()
```

### 6.4 Pools
- Limitan ejecuciones concurrentes para grupos de tareas
- Configuración en interfaz web: Admin > Pools
```python
task = BashOperator(
    task_id='limited_task',
    bash_command='echo "Running in pool"',
    pool='limited_pool',
    pool_slots=1,  # Slots utilizados por la tarea
)
```

### 6.5 Branching
```python
from airflow.operators.python import BranchPythonOperator

def _choose_branch(**context):
    if context['execution_date'].day == 1:
        return 'task_for_first_day'
    else:
        return 'task_for_other_days'

branch_task = BranchPythonOperator(
    task_id='branch_task',
    python_callable=_choose_branch,
)

first_day_task = BashOperator(
    task_id='task_for_first_day',
    bash_command='echo "First day of month"',
)

other_days_task = BashOperator(
    task_id='task_for_other_days',
    bash_command='echo "Not first day"',
)

branch_task >> [first_day_task, other_days_task]
```

### 6.6 SubDAGs
```python
from airflow.operators.subdag import SubDagOperator

def create_subdag(parent_dag_id, child_dag_id, start_date, schedule_interval):
    with DAG(
        f"{parent_dag_id}.{child_dag_id}",
        start_date=start_date,
        schedule_interval=schedule_interval,
    ) as dag:
        # Definir tareas del subdag
        # ...
        return dag

subdag_task = SubDagOperator(
    task_id='subdag_task',
    subdag=create_subdag('parent_dag', 'subdag_task', start_date, schedule_interval),
)
```

### 6.7 Triggers
```python
task = BashOperator(
    task_id='conditional_task',
    bash_command='echo "Run conditionally"',
    trigger_rule='one_success',  # Opciones: all_success, all_failed, one_failed, one_success, none_failed, etc.
)
```

### 6.8 XComs
```python
# Emisor (PythonOperator)
def push_xcom(**context):
    # Método 1:
    context['task_instance'].xcom_push(key='my_value', value=42)
    # Método 2 (valor de retorno automáticamente guardado en XCom):
    return {"result": 42}

# Receptor
def pull_xcom(**context):
    # Obtener de tarea específica:
    value = context['task_instance'].xcom_pull(task_ids='push_task', key='my_value')
    # O usando valor de retorno:
    result = context['task_instance'].xcom_pull(task_ids='push_task')
    print(f"Value: {value}, Result: {result}")
```

## 7. Patrones y Mejores Prácticas

### 7.1 Organización de DAGs
```
dags/
├── common/
│   ├── __init__.py
│   ├── operators.py
│   └── helpers.py
├── data_pipelines/
│   ├── __init__.py
│   ├── customer_etl.py
│   └── product_etl.py
└── reporting/
    ├── __init__.py
    └── daily_reports.py
```

### 7.2 Versionado y tests
- Mantener DAGs en control de versiones (Git)
- Utilizar tests unitarios para operadores personalizados
- Implementar tests de integración para DAGs completos
- Considerar CI/CD para despliegue automático

### 7.3 Patrones de diseño
- **Factory Pattern**: Para generación dinámica de DAGs
- **Template Pattern**: Para reutilizar estructuras de DAGs
- **Observer Pattern**: Para implementar callbacks

### 7.4 Estrategias de monitoreo
- Alertas por email en fallos
- Integración con sistemas de monitoreo (Prometheus, Grafana)
- Logs centralizados

### 7.5 Manejo de errores
```python
task = PythonOperator(
    task_id='task_with_retry',
    python_callable=function_that_may_fail,
    retries=3,
    retry_delay=timedelta(minutes=5),
    retry_exponential_backoff=True,
    max_retry_delay=timedelta(hours=1),
    email_on_failure=True,
    email=['team@example.com'],
)
```

### 7.6 Estrategias de backfill
```bash
# Ejecutar manualmente DAGs históricos
airflow dags backfill \
    -s 2021-01-01 \
    -e 2021-01-10 \
    --reset_dagruns \
    dag_id
```

## 8. Airflow en Entornos de Producción

### 8.1 Escalabilidad
- Usar Celery o Kubernetes para ejecutores distribuidos
- Implementar balanceo de carga para webservers
- Optimizar la base de datos (indexación, particionado)
- Considerar caches para reducir carga en la base de datos

### 8.2 Alta disponibilidad
- Múltiples schedulers (Airflow 2.0+)
- Base de datos replicada
- Webservers redundantes
- Monitoreo y alertas

### 8.3 Seguridad
- RBAC (Role-Based Access Control)
- Encriptación de conexiones y variables
- Aislamiento de tareas (especialmente en entornos compartidos)
- Auditoría de acciones

### 8.4 Gestión de recursos
- Usar pools para limitar acceso a recursos externos
- Configurar timeouts para evitar tareas bloqueadas
- Monitorear uso de memoria y CPU
- Implementar concurrency limits

### 8.5 Estrategias de despliegue
- Blue/Green deployment
- Canary releases
- Separación de entornos (desarrollo, testing, producción)

## 9. Operadores Específicos por Proveedor

### 9.1 AWS
```python
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.amazon.aws.operators.emr import EmrCreateJobFlowOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

s3_task = S3CreateBucketOperator(
    task_id='create_bucket',
    bucket_name='my-bucket',
    aws_conn_id='aws_default',
)
```

### 9.2 Google Cloud
```python
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

bq_task = BigQueryExecuteQueryOperator(
    task_id='execute_query',
    sql='SELECT * FROM `project.dataset.table` LIMIT 10',
    use_legacy_sql=False,
    gcp_conn_id='google_cloud_default',
)
```

### 9.3 Bases de datos
```python
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

pg_task = PostgresOperator(
    task_id='postgres_query',
    sql="INSERT INTO table (col) VALUES ('value')",
    postgres_conn_id='postgres_conn',
)
```

### 9.4 Transferencia de datos
```python
from airflow.providers.apache.hive.transfers.mysql_to_hive import MySqlToHiveOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator

transfer_task = MySqlToHiveOperator(
    task_id='mysql_to_hive',
    mysql_conn_id='mysql_conn',
    hive_conn_id='hive_conn',
    sql='SELECT * FROM source_table',
    hive_table='target_db.target_table',
)
```

## 10. Extendiendo Airflow

### 10.1 Operadores personalizados
```python
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

class MyCustomOperator(BaseOperator):
    @apply_defaults
    def __init__(self, my_parameter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_parameter = my_parameter
    
    def execute(self, context):
        self.log.info(f"Executing with parameter: {self.my_parameter}")
        # Lógica de implementación
        return "Result from custom operator"
```

### 10.2 Hooks personalizados
```python
from airflow.hooks.base import BaseHook

class MyServiceHook(BaseHook):
    def __init__(self, conn_id='my_service_default'):
        super().__init__()
        self.conn_id = conn_id
        self.connection = self.get_connection(conn_id)
    
    def get_conn(self):
        # Implementar lógica de conexión
        return MyServiceClient(
            host=self.connection.host,
            port=self.connection.port,
            username=self.connection.login,
            password=self.connection.password
        )
    
    def execute_action(self, action_params):
        client = self.get_conn()
        return client.execute(action_params)
```

### 10.3 Plugins
```python
from airflow.plugins_manager import AirflowPlugin
from operators.my_custom_operator import MyCustomOperator
from hooks.my_service_hook import MyServiceHook

class MyCompanyPlugin(AirflowPlugin):
    name = 'my_company_plugin'
    operators = [MyCustomOperator]
    hooks = [MyServiceHook]
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []
    appbuilder_views = []
    appbuilder_menu_items = []
```

### 10.4 Macros personalizados
```python
def my_custom_macro(value):
    return f"Processed: {value.upper()}"

# En el DAG
dag = DAG(
    'with_custom_macros',
    user_defined_macros={
        'custom_macro': my_custom_macro
    }
)

# Uso en template
task = BashOperator(
    task_id='use_macro',
    bash_command='echo "{{ custom_macro(\'hello\') }}"',
    dag=dag
)
```

## 11. Solución de Problemas Comunes

### 11.1 Problemas de rendimiento
- Demasiados DAGs/tareas
- Consultas de base de datos ineficientes
- Problemas con serialización de XComs grandes
- Schedulers sobrecargados

### 11.2 Estrategias de depuración
- Ejecución aislada con `airflow tasks test`
- Logging mejorado
- Uso de Airflow CLI para inspección
- Entornos de desarrollo local

### 11.3 Problemas comunes y soluciones
- **Tarea bloqueada**: Revisar dependencias, configurar timeouts
- **Scheduler lento**: Optimizar DB, reducir parsing de DAGs
- **Consumo excesivo de memoria**: Optimizar XComs, verificar leaks
- **Tareas no programadas**: Verificar dependencias y catchup settings

### 11.4 Comandos útiles
```bash
# Comprobar sintaxis de DAG
python dagfile.py

# Listar tareas de un DAG
airflow tasks list dag_id

# Verificar árbol de tareas
airflow tasks list dag_id --tree

# Probar tarea específica
airflow tasks test dag_id task_id 2023-01-01

# Comprobar conexiones
airflow connections get conn_id

# Reiniciar tarea fallida
airflow tasks clear dag_id -t task_id -s 2023-01-01 -e 2023-01-02
```

## 12. Evolución de Airflow

### 12.1 Novedades en Airflow 2.x
- TaskFlow API
- Scheduler escalable
- Rediseño de interfaz de usuario
- Rendimiento mejorado
- Nuevos operadores y providers

### 12.2 Tendencias y futuro
- Mayor integración con ecosistemas de datos
- Mejoras en UI/UX
- Mejor compatibilidad con computación en la nube
- Más capacidad para manejar datos grandes
- Mayor enfoque en ML y AI workflows

## 13. Recursos

### 13.1 Documentación oficial
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow GitHub Repository](https://github.com/apache/airflow)

### 13.2 Comunidad
- [Apache Airflow Slack](https://apache-airflow.slack.com/)
- [Airflow Stack Overflow](https://stackoverflow.com/questions/tagged/airflow)
- [Mailing Lists](https://airflow.apache.org/community/)

### 13.3 Tutoriales y blogs
- [Airflow Medium publication](https://medium.com/apache-airflow)
- [Astronomer Guides](https://www.astronomer.io/guides/)
- [Awesome Apache Airflow](https://github.com/jghoman/awesome-apache-airflow)
