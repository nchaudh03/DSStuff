create_cluster:
	k3d cluster create mlops --api-port 6550 -p "3001:80@loadbalancer" --agents 2

delete_cluster:
	k3d cluster delete mlops

install_aws_cli:
	curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
	unzip awscliv2.zip
	sudo ./aws/install