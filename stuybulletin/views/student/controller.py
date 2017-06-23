from app.blueprints import student_mod
from flask import url_for, request, session, current_app, redirect, g, render_template, request
from sqlalchemy import or_, desc
from app.models.opportunities import Opportunity
from app.models.tag import Tag
from app.core.authentication import require_login, require_role
import logging
import json

from app.extensions import db

LOG = logging.getLogger(__name__)

@student_mod.route('/')
@require_login
@require_role('student')
def index():
    """ Student dashboard """
    if 'id' in session and 'token' in session:
        return redirect(url_for("student.controller.opportunities"))
    return render_template("welcome.html")

@student_mod.route('/update_following/<int:id>/<int:to_change>', methods=['POST'])
@require_login
@require_role('student')
def update_following(id = 0, to_change = 0):
    """ Updates whether a user is following a specific opportunity

    :param id: ID of the opportunity to change
    :type id: int
    :param to_change: 1 if adding, 0 if removing
    :type to_change: int
    :returns: 'Success' if success 'Error' if error
    """

    opportunity = Opportunity.query.filter_by(id = id).first()
    
    if not to_change:
        if not opportunity in g.user.opportunities_following:
            g.user.opportunities_following.append(opportunity)
            LOG.debug('Added ' + str(g.user) + ' to the following list of ' + str(opportunity))
            db.session.commit()
            return 'Success'
        else:
            return 'Error'
    else:
        if opportunity in g.user.opportunities_following:
            g.user.opportunities_following.remove(opportunity)
            LOG.debug('Removed ' + str(g.user) + ' from the following list of ' + str(opportunity))
            db.session.commit()
            return 'Success'
        else:
            return 'Error'
    return 'Error'

@student_mod.route('/opportunities')
@student_mod.route('/opportunities/<int:page>')
@require_login
@require_role('student')
def opportunities(page = 1):
    """ Returns all opportunities for a student (paginated) seperated by either tag, but sorted in the recommendation order (see neural net fun times)

    :param page: Page to return
    :type page: int
    """

    if request.method == 'POST':
        if (request.form.getlist('starbox')):
            for i in request.form.getlist('starbox'):
                i.users_following.append(g.user)

        db.session.commit()
        return redirect( url_for("admin.controller.opportunities") )


    #from now on, assume method is GET
    
    #first, deal with search field
    search = ''
    if "search" in request.args:
        search = session["search"] = request.args.get("search")
    else:
        session.pop("search", None)

    opportunities = Opportunity.query.filter(
        or_(Opportunity.name.like('%' + search + '%'),
            Opportunity.description.like('%' + search + '%'),
            Opportunity.organization.like('%' + search + '%')
    ))

    #now, deal with sorting
    sort_by = ''
    if "sort_by" in request.args:
        sort_by = session["sort_by"] = request.args.get("sort_by")
    else:
        session.pop("sort_by", None)

    if sort_by == "alphabetical":
        opportunities = opportunities.order_by("name")
    elif sort_by == "reverse_alphabetical":
        opportunities = opportunities.order_by(desc("name"))
    elif sort_by == "deadline":
        opportunities = opportunities.order_by("deadline")
    elif sort_by == "reverse_deadline":
        opportunities = opportunities.order_by(desc("deadline"))
    else: #Do alphabetical if sort_by is unrecognized
        opportunities = opportunities.order_by("name")

    tags = ["Technology", "Theater", "Volunteer", "Research", "Environment", "Summer", "Hospital", "Math", "Dance"]
    #tags = request.args.get('tags') if 'tags' in request.args else ''

    #finally paginate
    opportunities = opportunities.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    #for i in Opportunity.query.all():
    #    print i.tags

    return render_template("student/student_opportunities.html", opportunities = opportunities, search = search, tags = tags)


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

    opportunities = g.user.opportunities_following.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    #opportunities = g.opportunities_following.paginate(page, current_app.config['ELEMENTS_PER_PAGE'], False)

    return render_template("student/starred_opportunities.html", opportunities = opportunities)


@student_mod.route('/opportunity/<int:op_id>')
@require_login
@require_role('student')
def opportunity(op_id = 0):
    """ Returns a single opportunity to display information

    :param op_id: ID of the opportunity to display information of
    :type op_id: int
    """

    opportunity = Opportunity.query.filter_by(id = op_id).first()
    print "\n" * 10
    print opportunity
    print "\n" * 10
    return render_template("student/student_opportunity.html", opportunity = opportunity)
