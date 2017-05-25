# TIMELINE

- [ ] 5/22: finish fxnality for
* - [ ] a person to create an opportunity (don't need to differentiate admin and person for now)
* - [ ] viewing a list of opportunities (arbitrarily chosen)
* - [ ] viewing a single opportunity
* - [ ] edit or remove a single opportunity

- [ ] 5/29: finish fxnality for
* - [ ] OAuth integration (this can be pushed back bc it depends on external coop)
* - [ ] tags and required materials
* - [ ] search for opportunities (by tags or querystring)

- [ ] 6/5: (OAuth has to be done by now) finish fxnality for
* - [ ] seperation of current fxnality between student and admin
* - [ ] students to suggest opportunities and for admins to approve them
* - [ ] students to star opportunities

- [ ] Whenever the deadline is
* - [ ] Content Distribution Network
* - [ ] Recommendations

* /student/opportunities and /admin/opportunities
*   - For student, list APPROVED opportunities by neural net recommender system
*     - Could possibly be subdivided into followed tags
*   - For admin, should show a list of unapproved opportunities

* /student/my_opportunities
* OR /admin/my_opportunities
*   - For student: lists opportunities created
*   - For admin: lists opportunities created or approved

* /student/opportunity/<id>
* OR /student/opportunity/<name> but it should redirect to /<id> anyway
*   - Display specific data of a single opportunity

* /student/starred-opportunities
*   - Hmm what could this mean

* /admin/opportunity/<id>
* OR /admin/opportunity/<name>
*   - Same as student but template should have editing/removing fxnality
*   - Should have fxnality to approve an unapproved opportunity

* /admin/add-opportunity
* OR /student/suggest-opportunity
*   - Interface for admins (and students) to create opportunities

* /admin/edit-opportunity/<id> or /<name>
*   - Use AJAX to update info on an opportunity
*   - JS should pass list of field-value pairs:
*     - field: one of many edits: 'name', 'desc', 'date', etc.
*     - value: updated value of field(s)

* /admin/remove-opportunity/<id> or /<name>
*   - Will be a POST request from frontend
*   - ID of opp. to remove can be inferred from request.referrer in flask

* /student/search and /admin/search
*   - Will be a GET request from HTML
*     - Frontend should pass:
*       - list of selected tags selected
*       - search query (string)
*   - Parse keywords and along with tags, return results from DB
