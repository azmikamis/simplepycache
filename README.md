# simplepycache

Simple server to illustrate caching with expiry.

### Installation

```sh
$ git clone git@github.com:azmikamis/simplepycache.git
$ cd simplepycache
$ python server.py
```

### Client API

The server exposes a REST API interact with the cache.

* POST - to add a key and a corresponding value to the cache
* GET - to retrieve a value from the cache
* PUT - to set expiry duration to a key

### Examples

To add `keya` with value of `valuea` to the cache

```sh
$ curl -sXPOST -d'{"key":"keya","value":"valuea"}' -H'Content-type:application/json' 'http://localhost:8000/'
```

To retrieve the value from `keya`

```sh
$ curl -sXGET -H'Content-type:application/json' 'http://localhost:8000/keya'
```

To set `keya` with an expiry value of `15` seconds  

```sh
$ curl -sXPUT -d'{"key":"keya","duration":"15"}' -H'Content-type:application/json' 'http://localhost:8000/'
```
