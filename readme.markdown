# jorrvaskr

A dashboard/stats collector web app for playing Werewolf.

## How to use

Install docker and docker-compose. Then do,

    docker-compose up

The site is served at port 16981 of your local machine.

Additionally, if this is your first run, you need to have some fixtures in your
database. So do (after `docker-compose up`),

    docker-compose exec web python /jorrvaskr/fixtures.py

## Compatibility

Use with Google Chrome in Ubuntu. Firefox should work, if with some styling
issues.

If you are unhappy about the state of compatibility, go make a PR. :P

## License

GNU GPLv3
