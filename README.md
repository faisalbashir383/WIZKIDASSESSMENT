# Wizkid Assessment


-------

### Environment setup
```shell
$ install python on your machine 
```

Install  & Create virtualenv
```shell
$ pip install virtualenv
$ virtualenv venv
```

### Start Project
Activate virtualenv(mac)
```shell
$ source venv/bin/activate
```
Activate virtualenv (windows)
```shell
$ venv/Scripts/activate
```

``
Install all dependencies
```shell
$ pip install -r requirements.txt
```

Make Migrations
```shell
$ python manage.py makemigrations
```

Run Migration
```shell
$ python manage.py migrate
```

collectstatic
```shell
$ python manage.py collectstatic
```

Run project
```shell
$ python manage.py runserver
```