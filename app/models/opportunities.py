""" Opportunities model

Currently just opportunity"""

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property

from app.models.helpers import Base
from app.models.required_material import RequiredMaterial
from app.models.tag import Tag
from app.models.relationships import tags, opportunities_following
from app.extensions import db

class Opportunity(Base):
    """ Opportunity model to store an opportunity """

    name = Column(String(128), unique = False, nullable = False)
    """ Column to store the name, as a string. """

    description = Column(String(1024), unique = False, nullable = True)
    """ Column to store the description, as a string. """

    organization = Column(String(128), unique = False, nullable = False)
    """ Column to store the organization, as a string. """

    start_time = Column(DateTime, unique = False, nullable = True)
    """ Column to store the start time for the opportunity, as a datetime object. """
    
    end_time = Column(DateTime, unique = False, nullable = True)
    """ Column to store the end time for the opportunity, as a datetime object. """

    hours = Column(Integer, unique = False, nullable = True)
    """ Column to store the hours per week, on average, that an opportunity may entail, as a number. """

    deadline = Column(DateTime, unique = False, nullable = True)
    """ Column to store the deadline for applying to an opportunity, as a datetime object. """

    required_materials = relationship('RequiredMaterial', backref = 'opportunity')
    """ Relationship Column creating the one-to-many relationship for the required material table.  It operates like a list."""

    tags = relationship('Tag',
                        secondary = tags,
                        back_populates = 'opportunities')
    """ Relationship Column to store the many to many to the tags.  It operates like a list. """

    users_following = relationship('User',
                                   secondary = opportunities_following,
                                   back_populates = 'opportunities_following')
    """ Relationship Column to store the many to many to the users.  It operates like a list. """

    link = Column(DateTime, unique = False, nullable = True)
    """ Column to store the link to either information about an opportunity, or the application. """

    def __repr__(self):
        """ __repr__ definition for the Opportunity model

        Should display as (for the opportunity with id 1): <Opportunity ID: 1>
        """
        return '<Opportunity ID: %d>' % self.id

    def add_required_material(self, required_material):
        """ Adds the required material to the user

        :param required_material: The required material to add.
        :type required_material: str
        """

        self.required_materials.append(RequiredMaterial(name = required_material))
        db.session.commit()

    def remove_required_material(self, required_material):
        """ Removes the required material from the user

        Returns true if the user had the required material and successfully deleted it.
        Returns false if the user doesn't have the required_material.

        :param required_material: The required material to remove.
        :type required_material: str
        :returns: bool - true if the required material was successfully deleted, false if the user didn't have the required material
        """
        deleted = False

        for r in self.required_materials:
            if r.name == required_material:
                db.session.delete(r)
                deleted = True
                
        db.session.commit()

        return deleted

    def add_tag(self, tag):
        """ Adds the tag to the opportunity

        :param tag: The tag to add.
        :type tag: str
        """

        self.tags.append(Tag(name = tag))
        db.session.commit()

    def remove_tag(self, tag):
        """ Removes the tag from the user

        Returns true if the opportunity had the tag and successfully deleted it.
        Returns false if the opportunity doesn't have the tag.

        :param tag: The tag to remove.
        :type tag: str
        :returns: bool - true if the tag was successfully deleted, false if the opportunity didn't have the tag
        """
        deleted = False

        for r in self.tags:
            if r.name == tag:
                db.session.delete(r)
                deleted = True
                
        db.session.commit()

        return deleted

    @hybrid_property
    def has_tag(self, tag):
        """ Checks for use in a sql query whether an opportunity has a tag.

        :param self: The opportunity to test
        :type self: app.models.opportunities.Opportunity
        :param tag: The tag to check
        :type tag: str
        :return: bool -- true if the organization has a tag that's equal to tag, false if not.
        """
        
        for t in self.tags.all():
            if t.tag == tag:
                return True
        return False

    @hybrid_property
    def has_tag_list(self, list_of_tags):
        """ Checks for whether any tag in a list of tags has been tagged by the opportunity

        :param self: The opportunity to test
        :type self: app.models.opportunities.Opportunity
        :param list_of_tags: The list of tags to check
        :type list_of_tags: list
        :return: bool -- true if the organization has a tag that's equal to any tag in list_of_tags, false if not.
        """
        
        for tag in list_of_tags:
            for t in self.tags.all():
                if t.tag == tag:
                    return True
        return False

