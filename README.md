# Deb-Parse-Web

#### Challenge:

A small app that exposes some key information about packages in a [Debian control file][1] via a web interface.

I broke this down in two. First, I wrote a [simple parser][2] in Python; then packaged it and distributed it on [PyPi][3]. Lastly, I wrote this Flask web app that depends on that package to demonstrate how it works.
___
__See it in action__
___

## Run it locally

```bash
$ git clone git@github.com:aihaddad/deb-parse-web.git
```
```bash
$ cd deb-parse-web
```
Create a `.env` file with the following information:

```
FLASK_APP=deb_parse_web/app.py
FLASK_DEBUG=1
UPLOAD_FOLDER=deb_parse_web/uploads
```
This app doesn't connect to any database, so you don't have to worry about that.

Next, make sure you have Python >= 3.7 and [`pipenv`][2] installed and:
```bash
$ pipenv install
...
```

and activate the virtual environment:

```bash
$ pipenv shell
...
(deb-parse-web) $
```
Then comes, Flask:
```bash
$ flask run
```
The app should be running on `http://localhost:5000/`

## Usage

You will be greeted with a file input form. Browse and upload your sample control file. You will be redirected to a packages index page at `http://localhost:5000/XXXX/packages/`. You can then check the _clean_ details of every package individually.

`XXXX` is a four-digit randomly generated `recovery_id`, use it to get back to the same results of this specific operation as long as they are alive. It's a rudimentary method I used to store, namespace and subdomain parsed results without relying on a database. This is a demo, so data integrity is not important. In the online version, all files will be only stored on the instance store, so they will be lost when the instance stops.

#### API Endpoints

JSON-formatted results will also be available for your benefit:
```
http://localhost:5000/XXXX/api/packages/raw     -> list of raw package information
http://localhost:5000/XXXX/api/packages/clean   -> list of cleaned-up information; same used by the web app
http://localhost:5000/XXXX/api/packages/list    -> list of just the package names
```

## Development

There are probably a few opportunities for refactoring. I've personally already identified a couple, at least one in this app, and one in the parser package. This is a learning project and to the best of my knowledge, everything works fine for now. So, I will get on with other projects first, and maybe revisit this later.


[1]: https://www.debian.org/doc/debian-policy/ch-controlfields.html
[2]: https://github.com/aihaddad/deb-parse
[3]: https://pypi.org/project/deb-parse/0.1.2rc1/
[4]: https://docs.pipenv.org/en/latest/
