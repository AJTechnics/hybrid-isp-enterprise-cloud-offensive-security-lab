# OpenTofu Runbook

## Start toolbox
podman run --rm -it -v ~/workspace:/workspace localhost/lab-toolbox

## Navigate
cd /workspace/hybrid-isp-enterprise-cloud-offensive-security-lab/opentofu/environments/lab-core

## Common commands
tofu fmt -recursive
tofu init
tofu validate
tofu plan
tofu apply

