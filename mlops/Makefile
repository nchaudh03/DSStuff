install_k3d:
	curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash


install_kubectl:
	 curl -LO https://dl.k8s.io/release/v1.26.0/bin/linux/amd64/kubectl
	 sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
	 rm kubectl

install_helm:
	curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
	chmod 700 get_helm.sh
	./get_helm.sh
	rm ./get_helm.sh

install_pulumi:
	curl -fsSL https://get.pulumi.com | sh
	source ~/.bashrc
	pulumi login --local

install_aws_cli:
	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
	unzip awscliv2.zip
	sudo ./aws/install
	rm awscliv2.zip
	rm -rd aws  

create_cluster:
	k3d cluster create mlops --api-port 6550 -p "3001:80@loadbalancer" --agents 2

delete_cluster:
	k3d cluster delete mlops

get_jenkins_password:
	kubectl exec --namespace default -it svc/jenkins -c jenkins -- /bin/cat /run/secrets/additional/chart-admin-password

