""" Tests the tag.py file

Tests the __repr__ function
"""

from stuybulletin.extensions import db
from stuybulletin.models.tag import Tag

from tests.models.helpers import create_test_tag

def test_repr():
    """ Tests the __repr__ """

    t = create_test_tag()
    db.session.add(t)
    db.session.commit()

    assert str(t) == '<Tag ID: %d>' % t.id
