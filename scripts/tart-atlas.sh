#!/bin/bash

cleanup () {
  # stop service and clean up here
  echo "stopping atlas deployment"
  atlas deployments stop MyMongo --type local 2>/dev/null
  echo "stopping podman containers"
  podman stop --all

  exit 0
}

trap "cleanup" EXIT
# 2>/dev/null is used to silence output about listing atlas instances other than local
PODMAN_HAS_MONGO_CONTAINER=$(podman ps --all 2>/dev/null | grep 'MyMongo')
PODMAN_HAS_MONGO_NETWORK=$(podman network ls  2>/dev/null | grep 'mdb-local-MyMongo')
DEPLOYMENT_INFO=$(atlas deployments list  2>/dev/null | grep 'MyMongo')

if [[ $PODMAN_HAS_MONGO_CONTAINER ]]; then
    # If missing network, create it (happens after docker compose down)
    if ! [[ $PODMAN_HAS_MONGO_NETWORK ]]; then
      # silence the update check
      atlas config set skip_update_check true 2>/dev/null
      echo "creating podman network:"
      podman network create mdb-local-MyMongo
    fi
    # Restart a deployment
    echo "starting podman containers"
    podman start --all
fi

if [[ $DEPLOYMENT_INFO ]]; then
    atlas deployments start MyMongo --type local 2>/dev/null
else
    # silence the update check
    atlas config set skip_update_check true 2>/dev/null
    atlas deployments setup MyMongo --type local --username root --password root --port 27017 --bindIpAll --force 2>/dev/null
fi

sleep infinity &
wait $!