import boto3


def report(session: boto3.session.Session):
    client = session.client("ec2")
    response = client.describe_regions()
    regions = len(response["Regions"])
    print(f"found {regions} regions")

    client = session.client("ssm")
    response = client.describe_parameters(MaxResults=50)
    parameters = len(response["Parameters"])
    print(f"found {parameters} parameters")

    client = session.client("rds")
    response = client.describe_db_clusters()
    clusters = len(response["DBClusters"])
    print(f"found {clusters} rds clusters")
    return regions, parameters, clusters


if __name__ == "__main__":
    session = boto3.session.Session()
    print(report(session))
