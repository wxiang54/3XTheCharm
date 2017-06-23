""" Tests the required_material.py file

Tests the __repr__ function
Other methods pertaining to this class is tested through stuybulletin.models.opportunities.Opportunity
"""

from stuybulletin.extensions import db
from stuybulletin.models.required_material import RequiredMaterial
from tests.models.helpers import create_test_required_material

def test_repr():
    """ Tests the __repr__ """

    r = create_test_required_material()
    db.session.add(r)
    db.session.commit()

    assert str(r) == '<RequiredMaterial ID: %d>' % r.id

    
