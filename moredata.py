from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from database_setup import MangaCategory, Base, MangaItem, User

engine = create_engine('sqlite:///mangacatelog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Historical Manga
manga_cat1 = MangaCategory(user_id=1, name="Psychological")

session.add(manga_cat1)
session.commit()
description_ = 'After the accident in which she lost her mother, 16 year old'\
                ' Tooru moves in with her grandfather, but due to his home '\
                'being renovated, is unable to continue living with him. '\
                'Claiming she will find someone to stay with but also fearing'\
                ' the criticism of her family and not want to burden any of'\
                ' her friends, Tooru resorts to secretly living on her own in'\
                ' a tent in the woods.'

manga1 = MangaItem(
    user_id=2,
    name="Neon Genesis Evangelion",
    description=description_,
    manga_category=manga_cat1)

session.add(manga1)
session.commit()
