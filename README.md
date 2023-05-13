# Finance app
This is a simple finance app to aggregate expenses across multiple credit cards.

# Local dev
Start with `docker-compose -f docker-compose-dev.yml  up`

Connect to web Docker container:
```
docker exec -it `docker ps -q`  /bin/bash
```

Locally, access the admin console through http://localhost:8080/admin/

Reset a user's account
Method 1
1. Connect to web Docker container as shown above
1. This will apply the standard validations. Run `python manage.py changepassword <user_name>`

Method 2
1. Connect to web Docker container as shown above
1. Start the shell: `python manage.py shell`
1. Run the following commands
```
from django.contrib.auth.models import User # or from expense.models import User
usr = User.objects.get(username='your username')
usr.set_password('raw password')
usr.save()
```

To list super users:
`User.objects.filter(is_superuser=True)`
