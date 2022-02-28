# Sparkify-Amazon-Redshift

ETl pipline leveraging S3, Redshift and Infrastructure as Code (IAC) to (build and) load an analytics Data Warehouse.
The pipeline extracts user activity and song data from json logs stored in S3, stages the data in a Redshift Cluster and transforms the data into a Data Warehouse with star schema.
This Project is part of the Udacity Data Engineering nanodegree. For convenience the infrastructure is set up leveraging Infrasctructure as Code (IAC), using AWS SDK for Python (Boto3).

- [Sparkify-Amazon-Redshift](#sparkify-amazon-redshift)
  - [About](#about)
  - [Raw Data](#raw-data)
  - [Data Warehouse Design](#data-warehouse-design)
  - [ETL Design](#etl-design)
  - [Tech/Framework used](#techframework-used)
  - [Getting Started](#getting-started)
    - [Setting Up the Environment](#setting-up-the-environment)
    - [Credentials](#credentials)
    - [Create Infrastructure using Python SDK](#create-infrastructure-using-python-sdk)
    - [Create DataWarehouse](#create-datawarehouse)
  - [Run ETL Pipeline](#run-etl-pipeline)
  - [Troubleshooting](#troubleshooting)
  - [Files](#files)
  - [Credits and Acknowledgments](#credits-and-acknowledgments)

## About

This project was created for Sparkify, a (fictional) music streaming provider. A continuously, fast growing user base requires Sparkify to leverage the scalability of the cloud. Currently the data resides in S3 as json logs of user activity and json song metadata. To improve the analysis of the user data by the analytics team a Star Schema Data Warehouse is required. The project will build a Data Warehouse, extract the data from S3, stage the data in AWS Redshift and transform & load the data into the Data Warehouse.

## Raw Data

The raw data consists of two data sources, the song data and the log data.
Both data sources are stored in S3:

- Song data `s3://udacity-dend/song_data`
- Log data `s3://udacity-dend/log_data`

## Data Warehouse Design

Star Schema is used to facilitate analytics.

Fact Table:
- songplays

Dimension Tables:
- users
- songs
- time
- artists

## ETL Design

The file `etl.py` contains two steps:

1. Loading/Staging the data into Amazon Redshift as is.
2. Transforming and Loading of the data into the Data Warehouse.

## Tech/Framework used

- AWS S3
- AWS Redshift
- AWS IAM
- Python
- Python SDK for AWS (boto3)

## Getting Started

### Setting Up the Environment

>This project requires an AWS Account.
>It is assumed that [Anaconda](https://anaconda.org/) is installed.

In order to run this project create a virtual environment.

```cmd
conda env create -f environment.yml
```

This will create the virtual environment aws-etl. Activate the environment with the following command.

```cmd
conda activate aws-etl
```

_optional_:
Run the following command to make this environment available in your (base) jupyter notebook.

```cmd
ipython kernel install --name "aws-etl" --user
```

### Credentials

>This project requires an AWS Account.

Rename `dwh_example.cfg` to `dwh.cfg`. Configure accordingly.

For leveraging Infrastructure as Code an IAM user is required.

Creating a new IAM user:

1. Go to [AWS IAM service](https://console.aws.amazon.com/iam/home#/users) and create a new IAM user.
2. Name the user accordingly
3. Choose "Programmatic access" as access type.
4. Select Attach existing policies directly and choose "AdministratorAccess".
5. Add tags according to your company guidelines and create user.

Update dwh.cfg with the `KEY` and `SECRET` of the IAM user.

### Create Infrastructure using Python SDK

Ensure that the environment is activated and that the credentials have been added to `dwh.cfg`. Run `IAC.ipynb` to set up the infrastructure (and to shut it down).
Once the Cluster is available, open an incoming TCP port and test the connection using `IAC.ipynb`.

### Create DataWarehouse

To create the Data Warehouse run:
_ensure that aws-etl environment is active._

```cmd
python create_tables.py
```

## Run ETL Pipeline

To run the ETL pipeline run:

```cmd
python etl.py
```

## Troubleshooting

Checking the Raw Data - modify link accordingly:

<https://s3.console.aws.amazon.com/s3/buckets/udacity-dend?region=us-west-2&tab=objects>

For troubleshooting log into AWS Redshift Query Editor and run: `select * from stl_load_errors;`

## Files

- __README.md__ Documentation of the project.
- __dwh.cfg__ Data Warehouse and ETL Pipeline configuration file.
- __environment.yml__ Conda environment file for creating the environment.
- __create_tables.py__ python file for creating the required Data Warehouse tables.
- __etl.py__ ETL Pipeline file.
- __sql_queries.py__ SQL Queries used for `create_tables.py` and `etl.py`.
- __IAC.ipynb__ Infrastructure As Code for deployment and disposal of the infrastructure.
- __.gitignore__ Python gitignore provided by GitHub and adapted to Project needs. 

## Credits and Acknowledgments

This Project is part of the Udacity Data Engineer Nanodegree.
