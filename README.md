**Welcome!** This is framework for creating custom servers. Can be used as foundation for MMO RPG servers, or web servers. Developed and tested on Python 3.6 on Linux.

## Installation

You need Python 3.6. To install needed dependencies run next command:

```commandline
pip3 install -r requirements.txt
```

You can also install from pypi:

```commandline
pip install idewavecore==0.0.1
```

### Database

Framework contains DB connection builder, that support mysql, postgresql or sqlite. You possible will need to install additional db drivers from dict below:

```python
SUPPORTED_DB_DRIVERS = {
    'mysql': (
        'mysqlconnector',
        'pymysql',
        'pyodbc',
    ),
    'postgresql': (
        'psycopg2',
        'pg8000',
        'pygresql',
    )
}
```

Please find how to install additional db drivers (and how to install and configure db) depending on your platform and operation system.

For example, for `psycopg2` (Linux Mint) you will need to run next commands:

```commandline
sudo aptitude install libpq-dev python-dev
pip3 install psycopg2
```

For `pg8000` (Linux Mint) just run:

```commandline
pip3 install pg8000
```

**Please note!** Possible you will need to install extra dependencies for this drivers depends on your platform and operation system.

## How to use

```python
import asyncio

from idewavecore import Assembler
from idewavecore.session import Storage

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    global_storage = Storage()

    assembler = Assembler(
        global_storage=global_storage,
        config_path='settings.yml'
    )

    servers = assembler.assemble()
    for server in servers:
        server.start()

    loop.run_until_complete(
        asyncio.gather(*[server.get() for server in servers])
    )

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
```

### Config

Config is main part of application. You will use it to describe all your servers and db connections. 

Please look into `settings.yml.dist` for example. You can use any name for config and also you can split config into multiple `.yml` files by using `!inject <path>` custom tag.


#### Storages

Framework use three type of storages: global storage, server storage and session storage. All storages are instances of `Storage`.  

All servers of application connected with global storage. You can modify global storage from any part of your application.

Each server has server storage. Basically it use for broadcast.

Each connection will generate session storage. This type of storage keep client session info.


#### Middlewares

Each server use middlewares. It is special function that can access all types of storages. 

Middlewares can communicate between each other by setting fields inside one of the storages.

Framework contains some predefined middlewares that can be used for common purposes. There middlewares for read, write, broadcast, parse http request, for testing and for encrypt (decrypt) data.

You can implement own middlewares. To use them all you need is create `middlewares` dir inside root of your project and use same structure as native middlewares has.

To allow framework to recognize if middleware is native or not you will need to add `native.` prefix to the path of native middleware. For custom middleware just use its path.


## Gratefulness

I am grateful to all guys who shared their ideas and suggestions, or explained how mmo rpg server works. In particular to Kyoril, sundays and brotalnia. I believe I will extend this list.

Also thanks to MANGOS community for great project and for responsiveness.


### Additional

Some approaches for my framework I took from my another project with similar name https://github.com/sergio-ivanuzzo/idewave-core. But they are not same. 

## Documentation

For now only README, source code and tests. I will update this section when project's wiki will be ready.
