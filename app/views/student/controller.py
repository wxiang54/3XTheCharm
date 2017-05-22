from app.blueprints import student_mod
from flask import url_for, request, session, current_app, redirect, g, render_template

from app.models.opportunities import Opportunity

from app.core.authentication import require_login, require_role

import logging

LOG = logging.getLogger(__name__)

@student_mod.route('/')
@require_login
@require_role('student')
def index():
    """ Student dashboard """
    
    return 'student_index'

@student_mod.route('/opportunities')
@student_mod.route('/opportunities/<int:page>')
@require_login
@require_role('student')
def opportunities(page = 1):
    """ Returns all opportunities for a student (paginated) seperated by either tag, but sorted in the recommendation order (see neural net fun times) 

    :param page: Page to return
    :type page: int
    """

    # Implement the whole suggestion thing
    opportunities = Opportunity.query.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    #fillerdata
    #keys = ["name", "description", "organization", "start_time", "end_time", "hours", "deadline", "required_materials", "tags", "users_following", "link"]
    #filler = {key: "%s%03d" % (key,i) for key in keys}
    
    return render_template("opportunities.html", opportunities = opportunities)

@student_mod.route('/my_opportunities/<int:page>')
@require_login
@require_role('student')
def my_opportunities(page = 1):
    """ Returns all opportunities that a user has suggesterd 
    
    :param page: Page to return
    :type page: int
    """

    # Implement this in the database first
    
    return 'student.controller.my_opportunities'

@student_mod.route('/starred_opportunities/<int:page>')
@require_login
@require_role('student')
def starred_opportunities(page = 1):
    """ Returns all the opportunities that a user is specifically following
    
    Two sections:
     - Opportunities that the user specifically followed
     - Opportunities in the tags selected by the user (is this necessary?)

    :param page: Page to return
    :type page: int
    """

    opportunities = g.opportunities_following.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)
    
    return 'student.controller.starred_opportunities'

@student_mod.route('/opportunity/<int:op_id>')
@require_login
@require_role('student')
def opportunity(op_id = 0):
    """ Returns a single opportunity to display information
    
    :param op_id: ID of the opportunity to display information of
    :type op_id: int
    """

    opportunity = Opportunity.query.filter_by(id = op_id).first()
    return opportunity
    print opportunity
    return 'student.controller.opportunity'

@student_mod.route('/search/<int:page>')
@require_login
@require_role('student')
def search(page = 1):
    """ Returns a paginated list of opportunities as pursuant to the search parameters given by the GET parameters
    
    The paramaters should be:
     - search (str) the string to search for
     - tags (str) the tags (as a comma seperated list) to search for

    :param page: Page to return
    :type page: int
    """

    return 'student.controller.search'

        

