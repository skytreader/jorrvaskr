# jorrvaskr

A dashboard/stats collector web app for playing Werewolf.

## How to use

Install docker and docker-compose. Then do,

    docker-compose up

The site is served at port 16981 of your local machine.

Additionally, if this is your first run, you need to have some fixtures in your
database. So do (after `docker-compose up`),

    docker-compose exec web python /jorrvaskr/fixtures.py

## License

GNU GPLv3
