#!/usr/bin/env bash

# This probably should be a wrapper around cfssl, not openssl. Probably.

set -Eeuo pipefail

setup_colors() {
  if [[ -t 2 ]] && [[ -z "${NO_COLOR-}" ]] && [[ "${TERM-}" != "dumb" ]]; then
    NOFORMAT='\033[0m' RED='\033[0;31m' GREEN='\033[0;32m' ORANGE='\033[0;33m' BLUE='\033[0;34m' PURPLE='\033[0;35m' CYAN='\033[0;36m' YELLOW='\033[1;33m'
  else
    NOFORMAT='' RED='' GREEN='' ORANGE='' BLUE='' PURPLE='' CYAN='' YELLOW=''
  fi
}

msg() {
  echo >&2 -e "${1-}"
}

succ() {
	msg "${GREEN}${1-}${NOFORMAT}"
}

warn() {
	msg "${ORANGE}${1-}${NOFORMAT}"
}

err() {
	msg "${RED}${1-}${NOFORMAT}"
	exit 1
}

setup_colors

# script logic here

msg "FAST KEYS GENERATION UTILITY"

if [ "$#" -ne 1 ]; then
	err "Please pass hostname as the first argument (and no more)"
else
	if ! echo "$1" | grep -q -P '(?=^.{4,253}$)(^(?:[a-zA-Z0-9](?:(?:[a-zA-Z0-9\-]){0,61}[a-zA-Z0-9])?\.)+([a-zA-Z]{2,}|xn--[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])$)'; then
		err "Provided hostname does not look like a hostname!"
	fi
	HOSTNAME=$1
fi

if [ ! -d .secrets ]; then
	msg "No ${GREEN}.secrets${NOFORMAT} exists, creating"
	mkdir .secrets
fi

msg "Generating host key"
if ssh-keygen -q -N "" -t rsa -b 4096 -f .secrets/ssh_host_rsa_key; then
	succ "Generated host key successfully"
else
	err "Failed to generate host key!"
fi

msg "Generating CA"
if openssl genrsa -aes256 -out .secrets/ca-key.pem 4096; then
	succ "Generated private CA key successfully"
else
	err "Failed to generate private CA key!"
fi

if openssl req -new -x509 -days 365 -key .secrets/ca-key.pem -sha256 -out .secrets/ca.pem; then
	succ "Generated public CA key"
else
	err "Failed to generate private CA key!"
fi

msg "Generating server's keys"

if openssl genrsa -out .secrets/server-key.pem 4096; then
	succ "Generated private server key"
else
	err "Failed to generate private server key"
fi

msg "Generating CSR"
if openssl req -subj "/CN=$HOSTNAME" -sha256 -new -key .secrets/server-key.pem -out .secrets/server.csr; then
	succ "Generated CSR"
else
	err "Failed to generate CSR!"
fi

msg "Generating server's CNF"
echo "subjectAltName = DNS:$HOSTNAME,DNS:localhost,IP:127.0.0.1" >> .secrets/extfile.cnf
echo "extendedKeyUsage = serverAuth" >> .secrets/extfile.cnf

msg "Generating server's certificate"
if openssl x509 -req -days 365 -sha256 -in .secrets/server.csr -CA .secrets/ca.pem -CAkey .secrets/ca-key.pem -CAcreateserial -out .secrets/server-cert.pem -extfile .secrets/extfile.cnf; then
	succ "Generated server's certificate"
else
	err "Failed to generate server's certificate"
fi

msg "Generating client's key"
if openssl genrsa -out .secrets/key.pem 4096; then
	succ "Generated client's key!"
else
	err "Failed to generate client's keys"
fi

msg "Generating client's CNF"
echo "extendedKeyUsage = clientAuth" > .secrets/extfile-client.cnf

msg "Generating client's CSR"
openssl req -subj '/CN=client' -new -key .secrets/key.pem -out .secrets/client.csr

msg "Generating client's cert"
if openssl x509 -req -days 365 -sha256 -in .secrets/client.csr -CA .secrets/ca.pem -CAkey .secrets/ca-key.pem -CAcreateserial -out .secrets/cert.pem -extfile .secrets/extfile-client.cnf; then
	succ "Generated client's cert"
else
	err "Failed to generate client's cert"
fi

msg "Removing CSRs and CNFs"
rm -v .secrets/client.csr .secrets/server.csr .secrets/extfile.cnf .secrets/extfile-client.cnf

msg "Chmoding certs"
chmod -v 0400 .secrets/ca-key.pem .secrets/key.pem .secrets/server-key.pem

succ "Done my part, know you may want to do something like:"
msg "${BLUE}sudo systemctl edit --full docker${NOFORMAT}"
succ "...and replace ${RED}ExecStart${NOFORMAT} with something like\n${BLUE}dockerd --tlsverify --tlscacert=ca.pem --tlscert=server-cert.pem --tlskey=server-key.pem -H=127.0.0.1:2376${NOFORMAT}"
succ "And use docker client as a\n${BLUE}docker --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem -H=$HOSTNAME:2376 version${NOFORMAT}"
