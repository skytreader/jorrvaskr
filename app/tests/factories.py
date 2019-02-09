from app import db
from app.models import (
    GameType,
    Player,
    GameSession,
    GameSessionRecord,
    Faction,
    FactionTally,
    WinLog,
    WinWeight
)
from faker import Faker

import factory
import random


fake = Faker()


class GameTypeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GameType
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    label = factory.LazyAttribute(
        lambda x: random.choice(("One Night", "Ultimate"))
    )

class PlayerFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Player
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    name = factory.LazyAttribute(lambda x: fake.first_name())

class GameSessionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GameSession
        sqlalchemy_session = db.session
    
    id = factory.Sequence(lambda n: n)
    game_type = factory.SubFactory(GameTypeFactory)
    # TODO Do we really want to LazyAttribute games_played? It seems more
    # prudent to leave this out and ensure that users of this factory always
    # specify a games_played, in order to not run afoul of DB constraints due to
    # too much automation.
    games_played = factory.LazyAttribute(lambda x: random.randint(0, 1000))

class GameSessionRecordFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = GameSessionRecord
        sqlalchemy_session = db.session

    game_session = factory.SubFactory(GameSessionFactory)
    player = factory.SubFactory(PlayerFactory)
