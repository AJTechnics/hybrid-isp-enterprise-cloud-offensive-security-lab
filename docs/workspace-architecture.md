# Workspace Architecture

## Workspace VM

### Name
`ws1`

### OS
Ubuntu Server 24.04 LTS

### User
`lab`

### Access
SSH

## Current role

`ws1` acts as the remote engineering workspace for:

- documentation
- Git operations
- Podman
- toolbox container execution
- future OpenTofu and Ansible runs

## Container runtime

Podman is installed on `ws1`.

## Toolbox container

A reusable toolbox container is being used for:

- OpenTofu
- Ansible
- Python tooling
- Git and SSH utilities

## Principle

Keep the host stable. Run project tooling from the container.
