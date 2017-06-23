""" RequiredMaterial model

Currently just RequiredMaterial """

from sqlalchemy import Column, String, ForeignKey, Integer

from stuybulletin.models.helpers import Base
from stuybulletin.extensions import db

class RequiredMaterial(Base):
    """ RequiredMaterial model to store a required material """

    name = Column(String(64), unique = False, nullable = False)
    """ Column to store the required material, or a descirption of it, as a string. """

    opportunity_id = Column(Integer, ForeignKey('opportunity.id'))
    """ Column storing the ForeignKey for the opportunity. """

    def __repr__(self):
        """ __repr__ defition for the RequiredMaterial model

        Should display as (for the required material with id 1): <RequiredMaterial ID: 1>
        """
        return '<RequiredMaterial ID: %d>' % self.id

