## set up k8s for example-flask
1. `kubectl create ns flask`
2. `kubectl -n flask create -f deployment.yaml`
3. `kubectl -n flask create -f service.yaml`
