#!/usr/bin/env bash
set -euo pipefail

secret_dir="${HOME}/.config/homelab-secrets"
pass_file="${secret_dir}/ansible-vault-pass.txt"
hash_file="${secret_dir}/ansible-vault-pass.sha256"

if [[ ! -f "${pass_file}" ]]; then
  echo "Missing password file: ${pass_file}" >&2
  exit 1
fi

if [[ ! -f "${hash_file}" ]]; then
  echo "Missing checksum file: ${hash_file}" >&2
  exit 1
fi

actual_hash=$(sha256sum "${pass_file}" | awk '{print $1}')
expected_hash=$(tr -d '\n\r' < "${hash_file}")

if [[ "${actual_hash}" != "${expected_hash}" ]]; then
  echo "Checksum mismatch for ${pass_file}" >&2
  exit 1
fi

cat "${pass_file}"
