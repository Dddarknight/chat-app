# chat-app

The app provides the backend service for the chat.
The API endpoints are described in API Documentaion (Swagger), that can be found at /docs.
After registration, the user can log in (/login) and then join the particular room and begin to chat.
The chat server is implemented with the python-socketio tool.
The informaion about entered and left rooms, about messages and users' likes is stored in the database (PostgreSQL). 


## Links
This project was built using these tools:
| Tool | Description |
|----------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | "Web framework for building APIs with Python" |
| [python-socketio](https://python-socketio.readthedocs.io/en/latest/index.html) | "Implements Socket.IO clients and servers that can run standalone or integrated with a variety of Python web frameworks." |
| [PostgreSQL](https://www.postgresql.org/) |  "An open source object-relational database system" |
| [SQLAlchemy](https://www.sqlalchemy.org/) |  "The Python SQL toolkit and Object Relational Mapper" |
| [Alembic](https://alembic.sqlalchemy.org/en/latest/) |  "A lightweight database migration tool for usage with the SQLAlchemy" |
| [poetry](https://python-poetry.org/) |  "Python dependency management and packaging made easy" |
| [Py.Test](https://pytest.org) | "A mature full-featured Python testing tool" |


## Installation
**Copy a project**
```
$ git clone git@github.com:Dddarknight/chat-app.git
$ cd chat-app 
```

**Set up environment variables**
``` 
$ touch .env

# You have to fill .env file. See .env.example.
# You will have to fill username and password fields for PostgreSQL. If you don't have these credentials, please follow the instructions in the official documentation.
# Also you have to choose environment variables, such as HOST, PORT for usage with or without Docker. See .env.example.

# To get a SECRET_KEY for FastAPI run:
$ openssl rand -hex 32
```

**Set up the environment**
```
$ pip install poetry
$ make install
```

**Launch API server**
```
$ make run
```

**Working with Docker**
```
# If you haven't used Docker earlier, you should follow the installation instruction on the official website (https://docs.docker.com/engine/install/).
# Then:
$ sudo apt install docker-compose

#Launch:
$ docker compose up --build
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)