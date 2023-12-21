**FastAPI JWT Authentication**

We create an access token and a refresh token. But there is a more secure way to implement this using Refresh Tokens.

**Refresh Token:** It is a unique token that is used to obtain additional access tokens. This allows you to have short-lived access tokens without having to collect credentials every time one expires.

[▶️ Watch Full Video](https://youtu.be/LgFxZhdhgeg?si=psrPGhi3Yg-zCdAh)

> Environment setup
```
> python -m venv venv
> venv\Scripts\activate
> python -m pip install --upgrade pip
> pip install -r requirements.txt
```

> Environment Variables
```
> rename dev.env to .env
```

> Database Migrations
```
> aerich init -t migrations.settings
> aerich init-db
```

> Run Application
```
> python main.py
```