""" Tests the auth views defined in views/auth/controller.py """

from flask import current_app

def test_index():
    """ Tests /auth/ """
    assert '302 FOUND' == current_stuybulletin.test_client().get('/auth/').status
