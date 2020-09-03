# infra
Infrastructre as a code repo


## Getting Started Steps
1. Create an Amazon EKS cluster via AWS CLI
2. Setup Helm for Jupyterhub
3. Configure Jupyterhub using zero-to-k8s Helm Chart
4. ALB Ingress Setup
5. External DNS Setup
6. EFS Setup

## Installation

## 1) AWS Setup
1. Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
2. Use `aws configure` to configure aws CLI 
3.  Create **IAM policy** using aws cli for alb ingress policy
   * `aws iam create-policy \
    --policy-name ALBIngressControllerIAMPolicy \
    --policy-document file://IAM/alb-policy.json` 
4.   Create **IAM policy** using aws cli for external dns policy
   * `aws iam create-policy \
    --policy-name AllowExternalDNSUpdates \
    --policy-document file://IAM/dns-policy.json` 

## 1) EKSCTL setup
1. Install [EKSCTL](https://github.com/weaveworks/eksctl)
2. Install Amazon EKS Vended [KUBECTL](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html)
3. Create a file named _**config.yaml**_ under the _**secrets**_ folder and paste the following keys and their respective values
        
            AWS_ACCESS_KEY_ID: ''
            AWS_SECRET_ACCESS_KEY: ''
4.  Run the _**read_yaml.yaml**_ python script to populate the sensitive data in their respective manifest/config file
5. Open _**cluster.yaml**_ file and make apropriate edits 
6. Run `eksctl create cluster -f cluster.yaml` to create and run cloud formation stacks that sets up your cluster and nodes and creates:
   * security groups
   *  vpc
   *  subnets
   *  eks cluster
   *  ec2 nodes
 * NOTE: This will update your context to point to the eks cluster created by eksctl. Use the following command if required to change your current context:
    * `kubectl config use-context $CONTEXTNAME`

## 2) Helm Setup

1. Install Helm 3: `curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash`
2. Verify: `helm list`
3. Create a namespace for Jupyterhub 
   * `kubectl create namespace $NAMESPACE` 

## 3) Jupyterhub Setup
1. Create random hex string to represent security token
   * `openssl rand -hex 32` 
2. Open the _**z2jh-config.yaml**_ file in the jupyterhub folder 
3. paste the generated random hex as the value for the **secretToken**
4. Add jupyterhub helm chart repo and update the repo
    * `helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/`
    * `helm repo update`
5. Install chart configured by _**z2jh-config.yaml**_ using the following commnad
    * `RELEASE=jupyterhub`
    * `NAMESPACE=jupyterhub`
    * `helm upgrade --install $RELEASE jupyterhub/jupyterhub   --namespace $NAMESPACE --version=0.9.0   --values jupyterhub/z2jh-config.yaml`

## 4) ALB Ingress Setup
1.  Open the _**secrets/jupyter_secrets.yaml**_ file and verify the base64 value for your aws access key id and aws secret access id
   * NOTE: To verify, decode the generated values in the file using the following command 
     * `echo -n '$encodedvalue' | base64 - D` 
2. Deploy the jupyer_secrets.yaml file
    * `kubectl apply -f config/jupyter_secrets.yaml`
3. Edit the _**alb-ingress-controller.yaml**_ file under the **controllers** folder and replace the following values:
   *  `--cluster-name=`
   *  `aws-vpc-id=`
   *  `--aws-region`
   *  `--cluster-name=`
4. Deploy the alb ingress controller
    * `kubectl apply -f roles/rbac-role.yaml` 
    * `kubectl apply -f controllers/alb_ingress_controller.yaml`
5. Verify the alb-ingress-controller creates resources 
    * `kubectl logs -n kube-system $(kubectl get po -n kube-system | egrep -o alb-ingress[a-zA-Z0-9-]+)`
            
            ----------------------------------------------------------------------------
            AWS ALB Ingress controller
            Release:    UNKNOWN
            Build:      UNKNOWN
            Repository: UNKNOWN
            -------------------------------------------------------------------------------

            I0725 11:22:06.464996   16433 main.go:159] Creating API client for http://localhost:8001
            I0725 11:22:06.563336   16433 main.go:203] Running in Kubernetes cluster version v1.8+ (v1.8.9+coreos.1) - git (clean) commit cd373fe93e046b0a0bc7e4045af1bf4171cea395 - platform linux/amd64
            I0725 11:22:06.566255   16433 alb.go:80] ALB resource names will be prefixed with 2f92da62
            I0725 11:22:06.645910   16433 alb.go:163] Starting AWS ALB Ingress controller

6.  Open the _**jupyter-ingress.config.yaml**_ and update the internet facing subnets in your vpc
7.  in the console update the subnets with the following tags
    *   `kubernetes.io/cluster/$CLUSERNAME: shared`
    *   `kubernetes.io/role/internal-elb: 1 or empty`
    *   `kubernetes.io/role/elb: 1 or empty`
8.  Create a new record by providing a hostname with a valid host zone in Route53
9.  Run the _**jupyter-ingress.yaml**_ file
    * `kubectl apply -f jupyterhub/jupyter-ingress.yaml`  
10. Verify alb-ingress-controller creates appropriate sources
    * `kubectl logs -n kube-system $(kubectl get po -n kube-system | egrep -o 'alb-ingress[a-zA-Z0-9-]+') | grep 'jupyterhub\/jupyterhub'`
11. Check the events of the ingress to see what events have occurred
    * `kubectl describe ing -n jupyterhub jupyterhub`

## 4) External DNS Setup
1.  Open the external-dns.yaml file and update the following args
      - `--source=service`
      - `--source=ingress`
      - `--domain-filter=test-dns.com` 
        - will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones
      - `--provider=aws`
      - `--policy=upsert-only`
        -  would prevent ExternalDNS from deleting any records, omit to enable full synchronization
      - `--registry=txt`
      - `--txt-owner-id=hosted-zone`
2.  Deploy the external DNS
    * `Kubectl apply -f external-dns.yaml`  
3. Verify the that DNS has propogated
    * dig jupyterhub.illumidesk.com
4. Test your url   

## 5) EFS Setup -- IN PROGRES


1. Get the vpc using the following command
    * `aws eks describe-cluster --name cluster_name --query "cluster.resourcesVpcConfig.vpcId" --output text`
2. get the CIDR of VPC using this command
    * `aws ec2 describe-vpcs --vpc-ids vpc-XXXXXXXXXs --query "Vpcs[].CidrBlock" --output text`
3. In console or CLI create a file system EFS for your cluster vpc
4. Under once created add mount targets for the public cluster subnets for each availablity zone
5. For each mount target select the `eks-cluster-sg-$clustername` security group to allow nfs access. 
   * NOTE: SG will have the following description
     * `EKS created security group applied to ENI that is attached to EKS Control Plane master nodes, as well as any managed workloads.` 
6. Open _**efs/efs-pv.yaml**_ and update the nfs server to match the username of your efs file system
   * ` server: fs-xxxx.efs.us-east-2.amazonaws.com`
7.  Apply the efs persistent volume and persistent volume claim
   * `kubectl apply -f efs/efs_pv.yaml`
   *  `kubectl apply -f efs/efs_pvc.yaml`
8. Open _**jupyterhub/z2jh-config.yaml**_ and update the **pvcPath** 
   * `pvcName: "jupyter-shared-volume"` 
9. Upgrade chart configured by _**z2jh-config.yaml**_ using the following commnad
    * `RELEASE=jupyterhub`
    * `NAMESPACE=jupyterhub`
    * `helm upgrade --install $RELEASE jupyterhub/jupyterhub   --namespace $NAMESPACE --version=0.9.0   --values jupyterhub/z2jh-config.yaml`
10. Run `df -HT`in your notebook container to view your mount targets 
