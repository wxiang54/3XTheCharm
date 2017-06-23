from app.blueprints import admin_mod
from flask import url_for, request, session, current_app, redirect, g, render_template
from sqlalchemy import or_, desc
from datetime import datetime
from app.models.opportunities import Opportunity
from app.core.authentication import require_login, require_role
from app.extensions import db
from collections import OrderedDict
import logging

from datetime import datetime

LOG = logging.getLogger(__name__)

@admin_mod.route('/')
@require_login
@require_role('admin')
def index():
    """ Admin dashboard """
    if 'id' in session and 'token' in session:
        return redirect(url_for("admin.controller.opportunities"))
    return redirect( url_for("auth.controller.login") )

# DONE
@admin_mod.route('/opportunities')
@admin_mod.route('/opportunities/<int:page>')
@require_login
@require_role('admin')
def opportunities(page = 1):
    """ Returns all opportunities for a admin (paginated) seperated by either tag, but sorted in the recommendation order (see neural net fun times)

    :param page: Page to return
    :type page: int
    """

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

    return render_template("admin/admin_opportunities.html", opportunities = opportunities, search = search, tags = tags)


@admin_mod.route('/opportunity/<int:op_id>')
@require_login
@require_role('admin')
def opportunity(op_id = 0):
    """ Returns a single opportunity to display information
        **EDITING AND REMOVING FXN**
    :param op_id: ID of the opportunity to display information of
    :type op_id: int
    """
    opportunity = Opportunity.query.filter_by(id = op_id).first()
    return render_template("admin/admin_opportunity.html", opportunity = opportunity)


# IN PROG
@admin_mod.route('/add-opportunity/', methods=['GET', 'POST'])
@require_login
@require_role('admin')
def add_opportunity(op_id = 0): # init param?
    """ Returns a interface for admins to create opportunities

    Everything is a string
    """
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        organization = request.form['organization']
        
        start_time = str(request.form["start_time"])
        try:
            start_time = datetime(year=int(start_time[:4]), month=int(start_time[5:7]), day=int(start_time[8:10]), hour=int(start_time[11:13]), minute=int(start_time[14:16]))
        except:
            start_time = datetime(year=2020, month=1, day=1, hour=0, minute=0)

        end_time = str(request.form["end_time"])
        try:
            end_time = datetime(year=int(end_time[:4]), month=int(end_time[5:7]), day=int(end_time[8:10]), hour=int(end_time[11:13]), minute=int(end_time[14:16]))
        except:
            end_time = datetime(year=2020, month=1, day=1, hour=0, minute=0)

        try:
            hours = float(request.form['hours'])
        except:
            hours = 0.0
    
        deadline = str(request.form["deadline"])
        try:
            deadline = datetime(year=int(deadline[:4]), month=int(deadline[5:7]), day=int(deadline[8:10]), hour=int(deadline[11:13]), minute=int(deadline[14:16]))
        except:
            deadline = datetime(year=2020, month=1, day=1, hour=0, minute=0)
        
        required_materials_raw = request.form['required_materials']
        tags_raw = request.form['tags']

        required_materials = [mat.strip() for mat in required_materials_raw.split(',')]
        tags = [tag.strip() for tag in tags_raw.split(',')]

        link = request.form['link']
        if link and link[:4] != "http":
            link = "http://" + link

        o = Opportunity(name = name,
                        description = description,
                        organization = organization,
                        start_time = start_time,
                        end_time = end_time,
                        hours = hours,
                        deadline = deadline,
                        link = link)

        for r in required_materials:
            o.add_required_material(r)

        for t in tags:
            o.add_tag(t)

        db.session.add(o)
        db.session.commit()

        # how to get op_id of newest entry?
        opportunity = Opportunity.query.filter_by(id = op_id).first()
        return redirect(url_for("admin.controller.opportunity", op_id = o.id))
    return render_template("admin/admin_add.html")

# DONE
@admin_mod.route('/edit-opportunity-form/<int:op_id>')
@require_login
@require_role('admin')
def edit_opportunity_form(op_id = 0):
    """ Returns a interface for admins to edit opportunities

    :param op_id: ID of the opportunity to edit information of
    :type op_id: int
    """

    opportunity = Opportunity.query.filter_by(id = op_id).first()
    deadline = str(opportunity.deadline)[:10] + "T" + str(opportunity.deadline)[11:]
    start_time = str(opportunity.start_time)[:10] + "T" + str(opportunity.start_time)[11:]
    end_time = str(opportunity.end_time)[:10] + "T" + str(opportunity.end_time)[11:]

    return render_template("admin/admin_edit.html", opportunity = opportunity,
                                                    deadline = deadline,
                                                    start_time = start_time,
                                                    end_time = end_time)

# DONE
@admin_mod.route('/edit-opportunity/<int:op_id>', methods = ["POST"])
@require_login
@require_role('admin')
def edit_opportunity(op_id = 0):
    """ edits the opportunity in the DB
    :param op_id: ID of the opportunity to edit information of
    :type op_id: int
    """

    # NEW VALUES
    name = request.form['name']
    description = request.form['description']
    organization = request.form['organization']

    start_time = str(request.form["start_time"])
    try:
        start_time = datetime(year=int(start_time[:4]), month=int(start_time[5:7]), day=int(start_time[8:10]), hour=int(start_time[11:13]), minute=int(start_time[14:16]))
    except:
        start_time = datetime(year=2020, month=1, day=1, hour=0, minute=0)


    end_time = str(request.form["end_time"])
    try:
        end_time = datetime(year=int(end_time[:4]), month=int(end_time[5:7]), day=int(end_time[8:10]), hour=int(end_time[11:13]), minute=int(end_time[14:16]))
    except:
        end_time = datetime(year=2020, month=1, day=1, hour=0, minute=0)


    try:
        hours = float(request.form['hours'])
    except:
        hours = 0.0
    

    deadline = str(request.form["deadline"])
    try:
        deadline = datetime(year=int(deadline[:4]), month=int(deadline[5:7]), day=int(deadline[8:10]), hour=int(deadline[11:13]), minute=int(deadline[14:16]))
    except:
        deadline = datetime(year=2020, month=1, day=1, hour=0, minute=0)


    required_materials_raw = request.form['required_materials']
    tags_raw = request.form['tags']

    required_materials = [mat.strip() for mat in required_materials_raw.split(',')]
    tags = [tag.strip() for tag in tags_raw.split(',')]
    print required_materials
    print tags
    link = request.form['link']
    if link and link[:4] != "http":
        link = "http://" + link

    """
    start_time = datetime(year = 2017, month = 1, day = 20) # Figure this out
    end_time = datetime(year = 2017, month = 1, day = 20) # Figure this out
    deadline = datetime(year = 2017, month = 1, day = 20) # Figure this out
    """
    # CHANGE DB ENTRY
    opportunity = Opportunity.query.filter_by(id = op_id).first()
    opportunity.name = name
    opportunity.description = description
    opportunity.organization = organization
    opportunity.hours = hours

    names = [mat.name for mat in opportunity.required_materials]

    opportunity.start_time = start_time
    opportunity.end_time = end_time
    opportunity.deadline = deadline

    for r in required_materials:
        if r not in names:
            opportunity.add_required_material(r)
            print "op to add (r)"
            print "[%s]" % r

    for rOrg in names:
        if rOrg not in required_materials or rOrg in names[names.index(rOrg)+1:]:
            opportunity.remove_required_material(rOrg)
            print "opps to remove (rorg):"
            print "[%s]" % rOrg

    print opportunity.required_materials

    names = [tag.name for tag in opportunity.tags]
    for tag in tags:
        if tag not in names or tag in names[names.index(tag)+1:]:
            opportunity.add_tag(tag)

    for tag in names:
        if tag not in tags:
            opportunity.remove_tag(tag)


    opportunity.link = link

    db.session.commit()

    return redirect(url_for("admin.controller.opportunity", op_id = op_id))

# DONE
@admin_mod.route('/remove-opportunity/<int:op_id>')
@require_login
@require_role('admin')
def remove_opportunity(op_id = 0):
    """ Returns a interface for admins to remove opportunities
        :param op_id: ID of the opportunity to remove information of
        :type op_id: int
    """
    opportunity = Opportunity.query.filter_by(id = op_id).first()

    db.session.delete(opportunity)
    db.session.commit()
    return redirect(url_for("admin.controller.opportunities", page = 1))

