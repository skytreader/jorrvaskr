# jorrvaskr

A dashboard/stats collector web app for playing Werewolf.

## How to use

Install docker and docker-compose. Then do,

    docker-compose up

The site is served at port 16981 of your local machine.

Additionally, if this is your first run, you need to have some fixtures in your
database. So do (after `docker-compose up`),

    docker-compose exec web python /jorrvaskr/fixtures.py

## Dumping the database contents

Is as simple as

    docker-compose exec db su postgres -c "pg_dump -Fc jorrvaskr" > jorrvaskr.db

## Testing

Build the main image (if you haven't already):

    docker build -t jorrvaskr:current .

Then, build the test image:

    docker-compose -f docker-compose-test.yml build

You may now run the tests like so:

    docker-compose -f docker-compose-test.yml run web

More info can be found in `.travis.yml`.

## Note

In an attempt to make `docker-compose.yml` and `docker-compose-test.yml` as
similar as possible, the images used by the services declared use the same
context. The slight difference between the main web image and the test web image
means that you need to build with `docker-compose` everytime you either want to
spin up the web app or run the unit tests. Not yet sure if there is a better way
to handle this.

## Compatibility

Use with Google Chrome in Ubuntu. Firefox should work, if with some styling
issues.

If you are unhappy about the state of compatibility, go make a PR. :P

## License

GNU GPLv3
