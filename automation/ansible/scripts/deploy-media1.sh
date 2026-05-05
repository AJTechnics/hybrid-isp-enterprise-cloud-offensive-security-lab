#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ansible_dir="$(cd -- "${script_dir}/.." && pwd)"

vault_helper="${ansible_dir}/scripts/get-vault-pass.sh"
vault_file="${ansible_dir}/inventories/lab/vault.yml"
inventory_file="${ansible_dir}/inventories/lab/hosts.yml"
playbook_file="${ansible_dir}/playbooks/deploy-minecraft.yml"

if [[ ! -x "${vault_helper}" ]]; then
  echo "Missing or non-executable vault helper: ${vault_helper}" >&2
  exit 1
fi

# Validate secret file presence and checksum before deployment.
"${vault_helper}" >/dev/null

cd "${ansible_dir}"

ansible-playbook \
  -i "${inventory_file}" \
  "${playbook_file}" \
  --limit media1 \
  -e "@${vault_file}" \
  "$@"
