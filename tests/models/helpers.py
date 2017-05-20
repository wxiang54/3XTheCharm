""" Provides helpers for testing the models

create_user() -- returns the created user object
create_role(role) -- returns the created role object
"""

from app.extensions import db
from app.models.users import User
from app.models.permissions import Role
from app.models.opportunities import Opportunity
from app.models.required_material import RequiredMaterial
from app.models.tag import Tag

def create_test_role():
    """ Creates and returns a testing role

    :returns: app.models.permissions.Role the created Role object
    """

    r = Role(role = 'test')

    return r

def create_test_user():
    """ Creates and returns a testing user 
    
    :returns: app.models.user.User the created user object
    """

    u = User(fname = 'testing', lname = 'blah')

    return u

def create_test_opportunity():
    """ Creates and returns a testing opportunity

    :returns: app.models.opportunities.Opportunity the created opportunity object
    """

    o = Opportunity(name = 'testing_name', organization = 'testing_organization')

    return o

def create_test_required_material():
    """ Creates and returns a testing required material

    :returns: app.models.permissions.RequiredMaterial the created RequiredMaterial object
    """

    r = RequiredMaterial(name = 'test')

    return r

def create_test_tag():
    """ Creates and returns a testing tag
    
    :returns: app.models.tag.Tag the created Tag object
    """
    
    t = Tag(name = 'test')

    return t

