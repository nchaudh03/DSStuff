"""
Creating a Kubernetes Deployment
"""
import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service
from pulumi_kubernetes.helm.v3 import Chart, LocalChartOpts,ChartOpts,FetchOpts
from pulumi_kubernetes.helm.v3 import Release, ReleaseArgs, RepositoryOptsArgs
from pulumi_kubernetes.kustomize import Directory
import json
import configparser


def get_secrets():
    config = configparser.RawConfigParser()
    config.read("/home/nchaudh03/.aws/credentials")
    data = {
        'AWS_ACCESS_KEY_ID' : config.get('default', 'aws_access_key_id'),
        'AWS_SECRET_ACCESS_KEY' : config.get('default', 'aws_secret_access_key')
    }
    return data


secrets = get_secrets()

AWS_USERNAME = secrets['AWS_ACCESS_KEY_ID']
AWS_PASSWORD = secrets['AWS_SECRET_ACCESS_KEY']

POSTGRES_USERNAME = "thisismyusername"
POSTGRES_PASS = "thisismypassword"
POSTGRES_DATABASE = "mlflow"
POSTGRES_HOST = "postgres-postgresql.default.svc.cluster.local" #service-name.namespace.svc.cluster.local


MLFLOW_BUCKET = "mlflowv2"



# Postgres DB for mlops
postgre = Chart(
    "postgres",
    ChartOpts(
        chart="postgresql",
        version="11.9.7",
        fetch_opts=FetchOpts(
            repo="https://charts.bitnami.com/bitnami",
        ),
        values= {
                    "auth": {
                        "username" : POSTGRES_USERNAME,
                        "password" : POSTGRES_PASS,
                        "database" : POSTGRES_DATABASE
                    }
                }

    ),
)

"""
# Minio <S3 Storage>
MINIO_BUCKET = "mlflow,metaflow"
MINIO_URL = "http://minio.default.svc.cluster.local:9000"
minio = Chart(
    "minio",
    ChartOpts(
        chart="minio",
        version="11.10.7",
        fetch_opts=FetchOpts(
            repo="https://charts.bitnami.com/bitnami",
        ),
        values= {
                    "auth": {
                        "rootUser" : MINIO_USERNAME,
                        "rootPassword" : MINIO_PASSWORD,
                    },
                    "defaultBuckets" : MINIO_BUCKET,
                    "ingress" : {
                        "enabled" : True,
                        "hostname" : "minio.localhost"
                    },
                    "apiIngress" : {
                        "enabled" : True,
                        "hostname" : "minio-api.localhost"
                    },
                }

    ),
)
"""

#-------------------For Mlflow Pod Environmnet----------------------------------------#
# Below env variables need to be set
# AWS_ACCESS_KEY_ID: 
# AWS_SECRET_ACCESS_KEY: "minio_key"
# postgres database must be used
#------------------------------------------------------------------------------------#


mlflow = Chart(
    "mlflow",
    LocalChartOpts(
        path="./Charts/mlflow",
        values= {
        "backendStore": {
                "postgres" : {
                        "username" : POSTGRES_USERNAME,
                        "password" : POSTGRES_PASS,
                        "host" : POSTGRES_HOST,
                        "port" : 5432,
                        "database" : POSTGRES_DATABASE
                }
        },
        "ingress" : {
            "enabled" : True,
            "hosts" : [{"host" : "mlflow.localhost"}],
        },
        "service" : {"type" : "ClusterIP"},
        "defaultArtifactRoot" : f"s3://{MLFLOW_BUCKET}",
        "minio" : {
            "enabled" : True,
            #"path" : MINIO_URL,
            "access_key_id" : AWS_USERNAME,
            "secret_access_key" : AWS_PASSWORD
        }
    },

    ),
)

#-------------------For metaflow Pod Environmnet----------------------------------------#
# Below env variables need to be set for the UI
# Ingress Need to Be enabled for the service and ui
# AWS_ACCESS_KEY_ID: 
# AWS_SECRET_ACCESS_KEY: "minio_key"
# postgres info needs to be added to both service and ui
# Sample metflow config
#{
#    "METAFLOW_BATCH_JOB_QUEUE": "metaflow-queue",
#    "METAFLOW_ECS_S3_ACCESS_IAM_ROLE": "arn:aws:iam::649929059614:role/metaflow-s3",
#    "METAFLOW_DATASTORE_SYSROOT_S3": "s3://metaflow",
#    "METAFLOW_DATATOOLS_SYSROOT_S3": "s3://metaflow/data",
#    "METAFLOW_DEFAULT_DATASTORE": "s3",
#    "METAFLOW_DEFAULT_METADATA": "service",
#    "METAFLOW_SERVICE_INTERNAL_URL": "http://metaflow-metaflow-service.default.svc.cluster.local:8080/",
#    "METAFLOW_SERVICE_URL": "http://metaflowservice.localhost:3001/",
#    "METAFLOW_KUBERNETES_SECRETS": "aws-secret",
#    "METAFLOW_KUBERNETES_NAMESPACE": "default",
#    "METAFLOW_KUBERNETES_SERVICE_ACCOUNT": "default"
#}
# For batch i added these policies to the user [AWSBatchFullAccess ,AmazonECSTaskExecutionRolePolicy , AmazonECS_FullAccess ,  AmazonS3FullAccess ]
# I also created a new role metaflo-s3 which was defined as AWS Service ---- ECS ---- ECS Task, this is the arn i put in the mlflow config
# I also created a job queue and compute queue using ec2 spots, coudent get fargate to work. 
#------------------------------------------------------------------------------------#
metaflow = Chart(
    "metaflow",
    LocalChartOpts(
        path="./Charts/metaflow",
        values = {
            "metaflow-service" : {
                "metadatadb" : {
                    "user" : POSTGRES_USERNAME,
                    "password" : POSTGRES_PASS,
                    "name": POSTGRES_DATABASE, 
                    "host" : POSTGRES_HOST
                },
                "ingress" : {
                    "enabled" : True,
                    "hosts" : [{"host": "metaflowservice.localhost",
                                "paths": [{'path' : "/",
                                           "pathType" : "ImplementationSpecific"
                                           }]
                               }]
                },
            },
            "metaflow-ui" : {
                "metadatadb" : {
                    "user" : POSTGRES_USERNAME,
                    "password" : POSTGRES_PASS,
                    "name": POSTGRES_DATABASE,
                    "host" : POSTGRES_HOST
                },
                "ingress" : {
                    "enabled" : True,
                    "hosts" : [{"host": "metaflow.localhost"}],
                },
                "env" : [{"name" : 'AWS_ACCESS_KEY_ID', "value" : AWS_USERNAME}, #TURN THIS INTO SECRET
                         {"name" : 'AWS_SECRET_ACCESS_KEY', "value" : AWS_PASSWORD} #TURN THIS INTO SECRET
                         ]
            },
            "postgresql" : {
                "enabled" : False,
            }
        }
    ),
)


## Jenkins
jenkins = Chart(
    "jenkins",
    ChartOpts(
        chart="jenkins",
        version="4.3.23",
        fetch_opts=FetchOpts(
            repo="https://charts.jenkins.io",
        ),
        values = {'controller': {'ingress': {'enabled': True, 'hostName': 'jenkins.localhost'}}},
    ),
)

