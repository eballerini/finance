# Finance app
This is a simple finance app to aggregate expenses across multiple credit cards.

# Local dev
Start with `docker-compose -f docker-compose-dev.yml  up`

Connect to web Docker container:
```
docker exec -it `docker ps -q`  /bin/bash
```

Locally, access the admin console through http://localhost:8080/admin/