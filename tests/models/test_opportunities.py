""" Tests the opportunities.py file

Tests creating an opportunity
Tests all fields for an opportunity
Tests simple querying
Tests __repr__ """

from app.models.opportunities import Opportunity
# This tests all the fields and the general syntax

from tests.models.helpers import create_test_opportunity, create_test_required_material

from app.extensions import db

def test_opportunities():
    """ Base Opportunity tests

    Tests basic creation and saving of a user object, as well as basic querying
    """

    new_opportunity = create_test_opportunity()

    db.session.add(new_opportunity)
    db.session.commit()

    query = db.session.query(Opportunity).filter_by(name = 'testing_name').order_by(Opportunity.id.desc()).first()

    assert query.id == new_opportunity.id

def test_repr():
    """ Tests the __repr__ """

    o = create_test_opportunity()
    db.session.add(o)
    db.session.commit()

    assert str(o) == '<Opportunity ID: %d>' % o.id

def test_required_material_checking():
    """ Basic required material check test
    
    Checks the check_required_material function
    """

    o = create_test_opportunity()
    t = create_test_required_material()

    o.required_materials.append(t)

    assert o.check_required_material(t.name)
    assert not o.check_required_material('')

def test_required_material_adding():
    """ Tests the add_required_material method """

    o = create_test_opportunity()
    o.add_required_material('test')

    assert o.check_required_material('test')
    assert not o.check_required_material('')

def test_required_material_removing():
    """ Tests the remove_required_material method """

    o = create_test_opportunity()
    db.session.add(o)
    db.session.commit()
    
    o.add_required_material('test')

    assert o.remove_required_material('test')
    assert not o.remove_required_material('test')
    assert not o.remove_required_material('')

    db.session.delete(o)
    db.session.commit()

