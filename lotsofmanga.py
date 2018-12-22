from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

pic_url1 = 'https://res.cloudinary.com/teepublic/image/private/s--UQzJzoi'\
            'i--/t_Preview/b_rgb:ffffff,c_limit,f_jpg,h_630,q_90,w_630/v'\
            '1530849949/production/designs/2861627_0.jpg'
User1 = User(
    name="Monkey D. Luffy",
    email="luffy@onepiece.com",
    picture=pic_url)
session.add(User1)
session.commit()

pic_url2 = 'https://i.pinimg.com/originals/93/67/5d/93675dcc1cbf43f596749'\
            'a7b84ad313d.jpg'

User2 = User(
    name="Roronoa Zoro",
    email="zoro@onepiece.com",
    picture=)
session.add(User2)
session.commit()

# Historical Manga
manga_cat1 = MangaCategory(user_id=1, name="Historical")

session.add(manga_cat1)
session.commit()
description_ = 'Set at the end of the Edo period known as the bakumatsu, '\
                'and the early stages of Miji Restoration, Rurouni Kenshin '\
                'tells story of Kenshin Himura, a former assassin known as '\
                'Hitokiri Battosai during blood-filled transition between '\
                'Edo period and Miji Restoration.After vowing to never take '\
                'another human life, Kenshin wanders Japan protect innocent '\
                'from those who mean them harm to help atone his violent past.'

manga1 = MangaItem(
    user_id=1,
    name="Rurouni Kenshin",
    description=description_,
    manga_category=manga_cat1)

session.add(manga1)
session.commit()

description_ = 'Set in Japan in the 1950s, Rainbow centers around six '\
                'delinquent boys and their mentor, who are sent to the '\
                'Shonan Special Reform School. While there, they learn '\
                'to set their troubled pasts aside and rely on each other, '\
                'while trying to cope with the atrocities and mistreatment '\
                'they are subjected to daily.'

manga2 = MangaItem(
    user_id=1,
    name="Rainbow",
    description=description_,
    manga_category=manga_cat1)

session.add(manga2)
session.commit()

description_ = 'The story centers around the land of Pars, a wealthy kingdom '\
                'that profits as a crossroads between its neighbors, and '\
                'engages in institutionalized slavery. The leader of Pars, '\
                'King Andragoras, holds a legendary reputation of being '\
                'undefeated in battle and hopes to harden his soft-hearted '\
                'son, Arslan, through rigorous military training.'

manga3 = MangaItem(
    user_id=2,
    name="Arslan Senki",
    description=description_,
    manga_category=manga_cat1)

session.add(manga3)
session.commit()

description_ = 'Set in Japans Warring States period, the Sengoku era, '\
                'Vagabond follows Shinmen Takezou, a wild child with a '\
                'violent streak who is shunned by the other members of '\
                'his village. Along with his best friend Matahachi, '\
                'Takezou runs away at seventeen to enlist in the Toyotomi '\
                'army, hoping to find glory on the battlefield. What '\
                'they find is death and destruction, as the Toyotomi '\
                'suffer a crushing defeat at the Battle of Sekigahara, '\
                'and they barely make it off the battlefield alive.'
manga4 = MangaItem(
    user_id=2,
    name="Vagabond",
    description=description_,
    manga_category=manga_cat1)

session.add(manga4)
session.commit()


# Action Manga
manga_cat2 = MangaCategory(
    user_id=1,
    name="Action")

session.add(manga_cat2)
session.commit()

description_ = 'The series focuses on Monkey D. Luffy, a young man who, '\
                'inspired by his childhood idol and powerful pirate Red '\
                'Haired Shanks, sets off on a journey from the East Blue '\
                'Sea to find the famed treasure One Piece and proclaim '\
                'himself the King of the Pirates. In an effort to organize '\
                'his own crew, the Straw Hat Pirates (Mugiwara '\
                'Kaizoku-danhen), Luffy rescues and befriends a swordsman '\
                'named Roronoa Zoro, and they head off in search of the '\
                'One Piece.'
manga1 = MangaItem(
    user_id=2,
    name="One Piece",
    description=description_,
    manga_category=manga_cat2)

session.add(manga1)
session.commit()

description_ = 'The story of Attack on Titan revolves around the adventures '\
                'of Eren Jeager who lives in the town of Shinganshina. ... '\
                'In the ensuing battle,Eren appears to have been killed when '\
                'he sacrificed himself to save Armin from being eaten by a '\
                'bearded Titan.'
manga2 = MangaItem(
    user_id=2,
    name="Attack on Titan",
    description=description_,
    manga_category=manga_cat2)

session.add(manga2)
session.commit()

description_ = 'Gon Freecss aspires to become a Hunter, an exceptional being '\
                'capable of greatness.With his friends and his potential, he '\
                'seeks for his father who left him when he was younger.'
manga3 = MangaItem(
    user_id=1,
    name="Hunter x Hunter",
    description=description_,
    manga_category=manga_cat2)

session.add(manga3)
session.commit()


# Comedy Manga
manga_cat3 = MangaCategory(
    user_id=1,
    name="Comedy")

session.add(manga_cat3)
session.commit()


manga1 = MangaItem(
    user_id=2,
    name="Pho",
    description=description_,
    manga_category=manga_cat3)

session.add(manga1)
session.commit()

manga2 = MangaItem(
    user_id=1,
    name="Chinese Dumplings",
    description=description_,
    manga_category=manga_cat3)

session.add(manga2)
session.commit()

# Romance Manga
manga_cat4 = MangaCategory(
    user_id=1, name="Romance")

session.add(manga_cat4)
session.commit()

description_ = 'At number seven is a romance manga that is not only '\
                'romantic and sweet but also funny and silly! It ss called '\
                'Lovely Complex and it is a series that tickles the '\
                'heart with all the complexities of love. While you are '\
                'reading this manga, you will find yourself slowly falling '\
                'in love with the characters and their charming love-hate '\
                'relationship.'
manga1 = MangaItem(
    user_id=2,
    name="Lovely Complex",
    description=description_,
    manga_category=manga_cat4)

session.add(manga1)
session.commit()

description_ = 'Haruhi Fujioka is a bright scholarship candidate with no '\
                'rank or title to speak of a rare species at Ouran High '\
                'School, an elite academy for students of high pedigree. '\
                'When she opens the door to Music Room number 3 hoping to '\
                'find a quiet place to study, Haruhi unexpectedly stumbles '\
                'upon the Host Club.'
manga2 = MangaItem(
    user_id=1,
    name="Ouran High School Host Club",
    description=description_,
    manga_category=manga_cat4)

session.add(manga2)
session.commit()


# Sport Manga
manga_cat5 = MangaCategory(
    user_id=1,
    name="Sport")

session.add(manga_cat5)
session.commit()

description_ = 'Hanamichi Sakuragi is a delinquent and the leader of a '\
                'gang. Sakuragi is very unpopular with girls, having been '\
                'rejected an astonishing fifty times. In his first year at '\
                'Shohoku High School, he meets Haruko Akagi, the girl of his '\
                'dreams, and is overjoyed when she is not repulsed or scared '\
                'of him like all the other girls he has asked out.'
manga1 = MangaItem(
    user_id=2,
    name="Slam Dunk",
    description=description_,
    manga_category=manga_cat5)

session.add(manga1)
session.commit()

print "added menu items!"
