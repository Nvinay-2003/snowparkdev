from snowflake.core import Root 
import snowflake.connector
from datetime import timedelta
from snowflake.core.task import Task , StoredProcedureCall
import procedures
from snowflake.core.task.dagv1 import DAG , DAGTask , DAGOperation , CreateMode , DAGTaskBranch
from snowflake.snowpark import Session
from snowflake.snowpark.types import StringType
from snowflake.core.task.context import TaskContext
import os


#conn = snowflake.connector.connect()

conn = snowflake.connector.connect(
     user=os.environ.get('SNOWFLAKE_USER'),
     password=os.environ.get('SNOWFLAKE_PASSWORD'),
     account=os.environ.get("SNOWFLAKE_ACCOUNT"),
     warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
     database=os.environ.get('SNOWFLAKE_DATABASE'),
     schema=os.environ.get('SNOWFLAKE_SCHEMA'),
     role=os.environ.get('SNOWFLAKE_ROLE'))

print("connection established")
print(conn)

root = Root(conn)
print(root)
  
with DAG("dag_copy_emp",schedule=timedelta(days=1),stage_location='@dev_deployment',warehouse="compute_wh",use_func_return_value=True,packages=["snowflake-snowpark-python"]) as dag:
  
  dag_task_1 =  DAGTask("copy_from_s3",StoredProcedureCall(procedures.copy_to_table_proc,\
    packages=["snowflake-snowpark-python"],imports=["@dev_deployment/my_de_project_1/app.zip"],\
    stage_location="@dev_deployment"),warehouse="compute_wh")
  
  schema = root.databases["demo_db"].schemas["public"]
  dag_op = DAGOperation(schema)
  dag_op.deploy(dag,CreateMode.or_replace)