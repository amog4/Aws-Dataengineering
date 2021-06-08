try:
    import logging
    import boto3
    from botocore.exceptions import ClientError
except:
    print("Few packages not installed")


logger = logging.getLogger(__name__)

# define job flow 

def run_job_flow(cluster_name, 
                log_s3_url,
                keep_alive,
                applications_to_install,
                job_iam_role,
                service_role,
                security_groups,
                steps,
                emr_client):

    responce = emr_client.run_job_flow()
