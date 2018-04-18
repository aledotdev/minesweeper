# Minesweeper demo

### Local Install
You need to install pipenv

```
pipenv install
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Api urls:
- List of games played `/api/game/`
- Game Detail `/api/game/<GAME_ID>/`
- Reveal action **POST** `/api/game/<GAME_ID>/action/`
```
{
  "x": <Field_X>,
  "Y": <Field_Y>,
  "csrfmiddlewaretoken": <CSRF TOKEN>
}
```


### App urls
- Game List  `/game/`
- New Game  `/game/new/`
- Play Game   `/game/<GAME_ID>/`


### Demo server
https://minesweeper-aledev.herokuapp.com/game/
User `admin`
password `qweqwe123123`
