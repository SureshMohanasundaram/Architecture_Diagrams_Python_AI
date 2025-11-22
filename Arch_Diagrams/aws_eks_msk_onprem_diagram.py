from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Router
from diagrams.onprem.database import Database
from diagrams.onprem.client import Client
from diagrams.onprem.storage import Storage

DOT_OUT = "diagrams/aws_eks_msk_onprem_diagrams"

def build():
    with Diagram("AWS EKS + MSK + On-Prem SQL (stylized)", filename=DOT_OUT, show=False, direction="LR"):
        internet = Client("Internet")

        with Cluster("AWS VPC"):
            with Cluster("Public Subnets"):
                alb = Server("ALB\n(Application Load Balancer)")

            with Cluster("Private Subnets"):
                eks = Server("EKS Cluster\n(Spring Boot MS)")
                msk = Server("Amazon MSK\n(Kafka)")
                ecr = Storage("ECR\n(Container Registry)")
                s3 = Storage("S3\n(Artifacts / Backups)")

        with Cluster("On-Prem Data Center"):
            onprem_router = Router("VPN / Direct Connect")
            onprem_sql = Database("On-Prem SQL Server")
            kafka_bridge = Server("Kafka Bridge / Gateway")

        # CI/CD and tooling (outside VPC but associated)
        gitlab = Server("GitLab CI/CD")
        artifactory = Server("JFrog Artifactory")
        terraform = Server("Terraform (IaC)")

        # Flows
        internet >> alb >> eks
        eks >> Edge(label="Kafka (TLS)") >> msk
        eks >> Edge(label="Pull images") >> ecr
        eks >> s3
        eks >> Edge(style="dashed", label="JDBC over VPN") >> onprem_router >> onprem_sql

        gitlab >> Edge(label="Push images") >> ecr
        gitlab >> Edge(label="Publish packages") >> artifactory
        gitlab >> terraform
        artifactory >> eks
        kafka_bridge >> Edge(style="dashed") >> msk


if __name__ == "__main__":
    build()
