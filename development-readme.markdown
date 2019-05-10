# Development README

## Database Operations

> **NOTE ON DUMPING AND RELOADING:** Right now, the instructions will lead you
> to creating a text dump. While this is not ideal, it is only because I can't
> get other dump formats to work...yet.

### Dumping the database contents

Assuming the containers are running, it is as simple as

    docker-compose exec db su postgres -c "pg_dump -Fp jorrvaskr" > jorrvaskr.sql

### Reloading database from a dump

> **WARNING:** When you reload a database, ensure that the DB is empty!
> Needless to say, dumping data on a nonempty database is going to cause
> problems.

Assuming the dump is created as above.

0. Edit the SQL dump and add the following line at the top:

    ```sql
    SET session_replication_role = replica;
    ```

1. Run the containers although for this whole operation, only the DB would
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

> **ISSUE:** Given the way Docker and Flask work, switching to a branch with a
> migration ongoing will automatically create the new tables in the database
> which a migration might just be adding.

1. Install virtualenv and create a virtualenv for jorrvaskr.
2. While inside a virtualenv (_outside_ Docker containers) do
    
    ```
    alembic revision -m "revision message"
    ```

3. Edit the resulting file to write your migration.
4. To run, spin up the Docker containers and do

    ```
    docker-compose exec web bash
    ```

   Once inside the container:

    ```
    cd jorrvaskr
    alembic upgrade head
    ```

## Testing

Build the main image (if you haven't already):

    docker build -t jorrvaskr:current .

Then, build the test image:

    docker-compose -f docker-compose-test.yml build

You may now run the tests like so:

    docker-compose -f docker-compose-test.yml run web

More info can be found in `.travis.yml`.
