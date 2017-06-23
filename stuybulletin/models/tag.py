""" Tag model

Currently just Tag """

from sqlalchemy import Column, String, ForeignKey, Integer

from stuybulletin.models.helpers import Base
from stuybulletin.models.relationships import tags, tags_following

from sqlalchemy.orm import relationship

from stuybulletin.extensions import db

class Tag(Base):
    """ Tag model to store a tag for an opportunity """

    name = Column(String(64), unique = False, nullable = False)
    """ Column to store the tag, or a description of it, as a string. """

    opportunities = relationship('Opportunity',
                        secondary = tags,
                        back_populates = 'tags')
    """ Relationship Column to store the many to many to opportunities.  It operates like a list. """

    users_following = relationship('User',
                                   secondary = tags_following,
                                   back_populates = 'tags_following')
    """ Relationship Column to store the many to many to users.  It operates like a list. """

    def __repr__(self):
        """ __repr__ definition for the Tag model

        Should display as (for the tag with id 1): <Tag ID: 1>
        """
        return '<Tag ID: %d>' % self.id
