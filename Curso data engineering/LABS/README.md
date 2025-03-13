## LABS

# DATA PIPELINE USING AWS SERVICES
The first lab guides you through setting up and running a data pipeline using AWS services.
I started by populating a MySQL database with data, then deployed an AWS Glue Job to extract, transformed, and loaded (ETL) the data into an S3 bucket. Terraform was used for Infrastructure as Code (IaC) to automate deployment. Finally, I analyzed the processed data using Amazon Athena, visualizing results through a Jupyter Notebook dashboard.
**This hands-on exercise demonstrates the integration of cloud-based ETL processes with analytical querying.**










#####excercise 1

data_quality_task = GreatExpectationsOperator(
        task_id="data_quality",
        data_context_root_dir="./dags/gx",
        
        # Set `data_asset_name` value equal to `"train_easy_destiny"`
        None="None",
        dataframe_to_validate=pd.read_parquet(
            f"s3://{Variable.get('bucket_name')}/work_zone/data_science_project/datasets/"
            f"{vendor_name}/train.parquet"
        ),
        
        # Set the `execution_engine` parameter equal to `"PandasExecutionEngine"`
        None="None",
        expectation_suite_name=f"de-c2w4a1-expectation-suite",
        
        # Set `return_json_dict` as `True` to return a json-serializable dictionary
        None=None,
        
        # Set `fail_task_on_validation_failure` as `True` 
        # to fail the Airflow task if the Great Expectation validation fails
        None=None,
    )









