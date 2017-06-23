""" Tests the users.py file 

Tests creating a user
Tests all fields for a user
Tests simple querying
Tests role setting and checking
Tests __repr__
"""

from stuybulletin.extensions import db
from stuybulletin.models.users import User
from tests.models.helpers import create_test_user, create_test_role

def test_users():
    """ Basic User tests

    Tests basic creation and saving of a user object, as well as basic querying 
    """
    
    new_user = create_test_user()

    db.session.add(new_user)
    db.session.commit()

    query = db.session.query(User).filter_by(email = 'testing@stuy.edu').order_by(User.id.desc()).first()

    assert query.id == new_user.id

def test_role_checking():
    """ Basic role check test
    
    Checks the check_role function
    """

    u = create_test_user()
    r = create_test_role()

    u.roles.append(r)

    assert u.check_role(r.role)
    assert not u.check_role('')

def test_role_adding():
    """ Tests the add_role method """

    u = create_test_user()
    u.add_role('test')

    assert u.check_role('test')
    assert not u.check_role('')

def test_role_removing():
    """ Tests the remove_role method """

    u = create_test_user()
    db.session.add(u)
    db.session.commit()
    
    u.add_role('test')

    assert u.remove_role('test')
    assert not u.remove_role('test')
    assert not u.remove_role('')

    db.session.delete(u)
    db.session.commit()

def test_repr():
    """ Tests the __repr__ """

    u = create_test_user()
    db.session.add(u)
    db.session.commit()

    assert str(u) == '<User ID: %d>' % u.id

