# Development README

## Database Operations

> **NOTE ON DUMPING AND RELOADING:** Right now, the instructions will lead you
> to creating a text dump. While this is not ideal, it is only because I can't
> get other dump formats to work...yet.

### Dumping the database contents

Assuming the containers are running, it is as simple as

    docker-compose exec db su postgres -c "pg_dump -Fp jorrvaskr" > jorrvaskr.sql

### Reloading database from a dump

Assuming the dump is created as above.

0. Edit the SQL dump and add the following line at the top:

    ```sql
    SET session_replication_role = replica;
    ```

1. Run the containers althought for this whole operation, only the DB would
actually matter:

    ```
    docker-compose up
    ```

2. Copy the dump into the DB container:

    ```
    docker cp <path_to_dbdump> jorrvaskr_db_1:/tmp
    ```

3. Then, restore from file:

    ```
    docker-compose exec db su postgres -c "psql -d jorrvaskr < /tmp/jorrvaskr.sql"
    ```

### Creating migrations

1. Install virtualenv and create a virtualenv for jorrvaskr.
2. While inside a virtualenv (_outside_ Docker containers) do
    
    ```
    alembic revision -m "revision message"
    ```

3. To run, spin up the Docker containers and do

## Testing

Build the main image (if you haven't already):

    docker build -t jorrvaskr:current .

Then, build the test image:

    docker-compose -f docker-compose-test.yml build

You may now run the tests like so:

    docker-compose -f docker-compose-test.yml run web

More info can be found in `.travis.yml`.

### Note

In an attempt to make `docker-compose.yml` and `docker-compose-test.yml` as
similar as possible, the images used by the services declared use the same
context. The slight difference between the main web image and the test web image
means that you need to build with `docker-compose` everytime you either want to
spin up the web app or run the unit tests. Not yet sure if there is a better way
to handle this.
