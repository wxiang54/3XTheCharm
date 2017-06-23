""" A file to store all the tables for any and all many to many relationships """
from stuybulletin.models.helpers import Base

from sqlalchemy import Column, Integer, ForeignKey, Table, UniqueConstraint

tags = Table('tags',
             Base.metadata,
             Column('opportunity.id', Integer, ForeignKey('opportunity.id')),
             Column('tag.id', Integer, ForeignKey('tag.id')),
             UniqueConstraint('opportunity.id', 'tag.id', name = 'UC_opportunity.id_tag.id'))
""" Table setting up the many to many relationship between opportunities and tags """

tags_following = Table('tags_following',
                      Base.metadata,
                      Column('tag.id', Integer, ForeignKey('tag.id')),
                      Column('user.id', Integer, ForeignKey('user.id')),
                      UniqueConstraint('tag.id', 'user.id', name = 'UC_tag.id_user.id'))
""" Table setting up the many to many relationship between users and tags """

opportunities_following = Table('opportunities_following',
                                Base.metadata,
                                Column('opportunity.id', Integer, ForeignKey('opportunity.id')),
                                Column('user.id', Integer, ForeignKey('user.id')),
                                UniqueConstraint('opportunity.id', 'user.id', name = 'UC_opportunity.id_user.id'))
""" Table setting up the many to many relationship between opportunities and users """


