install_k3d:
	curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | TAG=v5.0.0 bash

install_k3d_old:
	curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | TAG=v4.4.4 bash


create_cluster:
	k3d cluster create -p "8081:80@loadbalancer" --k3s-arg "--disable=traefik@server:0" 
	kubectl config use-context k3d-k3s-default
	kubectl cluster-info
	kubectl version

delete_cluster:
	k3d cluster delete

install_kubeflow:
	while ! kustomize build example | kubectl apply -f -; do echo "Retrying to apply resources"; sleep 10; done

apply_fixes:
	kubectl apply -f ~/Documents/Kubeflow/importantlocal/pipelineaccess.yaml
	kubectl apply -f ~/Documents/Kubeflow/importantlocal/kserve-secret.yaml
	kubectl apply -f ~/Documents/Kubeflow/importantlocal/kserve-securityaccount.yaml

argocd:
	kubectl create namespace argocd
	kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
	kubectl port-forward svc/argocd-server -n argocd 8080:443 &
	kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo