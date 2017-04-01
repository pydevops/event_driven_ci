
## salt-master reactor configuration
1. `master.d/reactor.conf`: map event such as application deploy to the reactor sls file
2. `reactor/app-deploy.sls`: state file for deploying new docker image on kubernetes.


## set up k8s for example-flask
1. `kubectl create ns flask`
2. `kubectl -n flask create -f deployment.yaml`
3. `kubectl -n flask create -f service.yaml`


## deploy or rollback via CI
* `ci.sh` shows how to send deploy event to the Salt Event Bus, the data has `app` and `version`

## k8s deployment in essence
[Kubernets deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
e.g. `kubectl -n flask set image deployment/flask-deployment flask=pythonrocks/flask:c40d35954b`
`c40d35954b` is the git commit hash's first 10.

We can run the above k8s deployment logic in any node. 

## GKE note
`kubectl --kubeconfig=kubeconfig --server="https://${K8S_MASTER_IP}" -n flask set image deployment/flask-deployment flask=pythonrocks/flask:c40d35954b`
kubeconfig /var/lib/kubelet/kubeconfig
