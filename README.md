# Pinterest Data Pipeline Project

## Table of Contents

1. [Project Overview](#project-overview)
2. [Batch Processing: Configuring the EC2 Kafka Client](#batch-processing-configuring-the-ec2-kafka-client)
3. [Batch Processing: Connecting MSK Cluster to S3 Bucket](#batch-processing-connecting-msk-cluster-to-s3-bucket)
4. [Batch Processing: Configuring an API in API Gateway](#batch-processing-configuring-an-api-in-api-gateway)
5. [Batch Processing: Databricks](#batch-processing-databricks)
6. [Batch Processing: Spark on Databricks](#batch-processing-spark-on-databricks)
7. [Batch Processing: Databricks Workloads on AWS MWAA](#batch-processing-databricks-workloads-on-aws-mwaa)
8. [Stream Processing: Kinesis Stream Data and Read Using Databricks](#stream-processing-kinesis-stream-data-and-read-using-databricks)

## 1. Project Overview

The Pinterest Data Pipeline project is a comprehensive data engineering initiative designed to streamline the collection, processing, and analysis of data from the Pinterest platform. Leveraging various AWS services and data processing tools, this project aims to create an end-to-end data pipeline that seamlessly handles both batch and stream processing of Pinterest data. Key components include Amazon MSK for stream processing, Amazon S3 for data storage, Databricks for data transformation, AWS MWAA for workflow orchestration, and AWS API Gateway for data ingestion. By setting up Kinesis Data Streams and configuring REST APIs, this project ensures real-time data ingestion and processing. The pipeline also includes data cleaning and storage in Delta Tables, enabling efficient querying and analytics. This project simplifies the complex task of managing Pinterest data, making it accessible and actionable for data-driven insights.

## 2. Batch Processing: Configuring the EC2 Kafka Client

### 2.1 Creating Key Pair File
1. Navigate to the AWS Parameter Store and locate EC2 instance's key pair.
2. Copy the key pair's value, including BEGIN and END headers.
3. Paste the content into a new file with a .pem extension.

### 2.2 Connecting to EC2 Instance
1. Navigate to the EC2 console and identify EC2 instance.
2. Save the .pem file using the format: KeyPairName.pem.
3. Follow SSH connection instructions provided on the EC2 console.

### 2.3 Installing Kafka and IAM MSK Authentication Package
1. Install Kafka on EC2 machine.
2. Install the IAM MSK Authentication Package on the EC2 machine.

### 2.4 Configuring IAM for MSK Authentication
1. In the AWS IAM console, copy access role's Role ARN.
2. Add a principal to the role's trust policy with the EC2 instance's ARN.

### 2.5 Configuring client.properties File
1. Modify the client.properties file in the kafka_folder/bin directory.
2. Use AWS IAM authentication for cluster authentication.

### 2.6 Creating Kafka Topics
1. Retrieve Bootstrap servers and Zookeeper connection strings from MSK Management Console.
2. Create three topics: .pin, .geo, and .user.
3. Replace BootstrapServerString in Kafka create topic command.
4. Set CLASSPATH environment variable properly.

## 3. Batch Processing: Connecting MSK Cluster to S3 Bucket
1. Go to AWS S3 console and find the S3 bucket for the MSK cluster.
2. Download Confluent.io Amazon S3 Connector on EC2 client.
3. Copy the connector to the S3 bucket.
4. Access the MSK Connect console.
5. Create a custom plugin and connector with specific settings.
6. Set IAM role for authentication.
7. Data flowing through MSK cluster will be stored in the designated S3 bucket.

## 4. Batch Processing: Configuring an API in API Gateway
1. Create a resource in API Gateway for PROXY integration.
2. Set up HTTP ANY method for the resource.
3. Define Endpoint URL with the correct PublicDNS from the EC2 machine.
4. Deploy the API and note the Invoke URL.
5. Install Confluent package for Kafka REST Proxy on EC2 client.
6. Allow REST proxy IAM authentication to MSK cluster.
7. Launch the REST proxy on the EC2 client machine.

## 5. Batch Processing: Databricks
1. Mount S3 bucket to Databricks. `mount_s3.ipynb`
2. When reading JSON data from S3, specify the complete path.
3. Create three DataFrames: df_pin, df_geo, and df_user.
4. Batch Processing: Spark on Databricks
5. Transform and query data using `clean_dataframe_and_analysis.ipynb`.

## 6. Batch Processing: Databricks Workloads on AWS MWAA
1. Ensure AWS account has MWAA access.
2. Create an API token in Databricks for MWAA connection.
3. Set up MWAA-Databricks connection.
4. Install Python dependency for Databricks connection in MWAA.
5. Create an Airflow DAG for Databricks Notebook execution.
6. Upload DAG file `121ca9f7ce2b_dag.py` to mwaa-dags-bucket.
7. Manually trigger the DAG for testing.

## 7. Stream Processing: Kinesis Stream Data and Read Using Databricks
1. Ensure AWS account has access to AWS Kinesis.
2. Create three Kinesis Data streams.
3. Configure REST API for Kinesis actions invocation.
4. Update IAM role for API methods.
5. Use `user_posting_emulation_streaming.py` to send data to API.
6. Read, clean and write data to tables using `streaming_data.ipynb`.