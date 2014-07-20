# Reza Busheri
# HW2

import cgi
import urllib2
import webapp2
import logging

from google.appengine.ext import db
from google.appengine.api import images

MAIN_HEADER = """
<!DOCTYPE HTML>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="css/main.css">
		<link rel="stylesheet" href="css/jquery.mobile-1.4.2.min.css">
		<script src="js/jquery.js"></script>
		<style type="text/css"></style>
		<script src="js/jquery.mobile-1.4.2.min.js"></script>
		<title>%s</title>
	</head>
	<body class='ui-mobile-viewport ui-overlay-c'>
	<div data-role="page" class="ui-page ui-body-c ui-page-active">
		<div data-role="header" class="ui-header ui-bar-a" role="banner">
"""

FORM_INPUT = """
<div data-role="content" class="ui-content" role="main">
<div class="center-wrapper">
<form action='/add' method='post' enctype='multipart/form-data' data-ajax='false'>
	<label for='fName'>First name:</label>
	<input type='text' name='fName' id='fName' value='%s'><br>

	<label for='lName'>Last name:</label>
	<input type='text' name='lName' id='lName' value='%s'><br>

	<label for='street'>Street</label>
	<input type='text' name='street' id='street' value='%s'><br>

	<label for='city'>City</label>
	<input type='text' name='city' id='city' value='%s'><br>

	<label for='state'>State</label>
	<select name='state' id='state'>
		<option value="AL">Alabama</option>
		<option value="AK">Alaska</option>
		<option value="AZ">Arizona</option>
		<option value="AR">Arkansas</option>
		<option value="CA">California</option>
		<option value="CO">Colorado</option>
		<option value="CT">Connecticut</option>
		<option value="DE">Delaware</option>
		<option value="DC">District Of Columbia</option>
		<option value="FL">Florida</option>
		<option value="GA">Georgia</option>
		<option value="HI">Hawaii</option>
		<option value="ID">Idaho</option>
		<option value="IL">Illinois</option>
		<option value="IN">Indiana</option>
		<option value="IA">Iowa</option>
		<option value="KS">Kansas</option>
		<option value="KY">Kentucky</option>
		<option value="LA">Louisiana</option>
		<option value="ME">Maine</option>
		<option value="MD">Maryland</option>
		<option value="MA">Massachusetts</option>
		<option value="MI">Michigan</option>
		<option value="MN">Minnesota</option>
		<option value="MS">Mississippi</option>
		<option value="MO">Missouri</option>
		<option value="MT">Montana</option>
		<option value="NE">Nebraska</option>
		<option value="NV">Nevada</option>
		<option value="NH">New Hampshire</option>
		<option value="NJ">New Jersey</option>
		<option value="NM">New Mexico</option>
		<option value="NY">New York</option>
		<option value="NC">North Carolina</option>
		<option value="ND">North Dakota</option>
		<option value="OH">Ohio</option>
		<option value="OK">Oklahoma</option>
		<option value="OR">Oregon</option>
		<option value="PA">Pennsylvania</option>
		<option value="RI">Rhode Island</option>
		<option value="SC">South Carolina</option>
		<option value="SD">South Dakota</option>
		<option value="TN">Tennessee</option>
		<option value="TX">Texas</option>
		<option value="UT">Utah</option>
		<option value="VT">Vermont</option>
		<option value="VA">Virginia</option>
		<option value="WA">Washington</option>
		<option value="WV">West Virginia</option>
		<option value="WI">Wisconsin</option>
		<option value="WY">Wyoming</option>
	</select><br>

	<label for='zipCode'>Zip Code</label>
	<input type='text' name='zipCode' id='zipCode' value='%s'><br>

	<label for='phone'>Phone (No /,-, or spaces)</label>
	<input type='text' name='phone' id='phone' maxlength='10' value='%s'><br>

	<label for='email'>Email</label>
	<input type='email' name='email' id='email' value='%s'><br>
	
	<label for='photo'>Photo</label>
	<input type='file' name='photo' id='photo'><br>

	<input type='submit' value='Add Person' data-icon="plus">
</form></div>
"""

MAIN_END = """
	</div></div></body>
</html>
"""

# Model

class User(db.Model):
	fName = db.StringProperty()
	lName = db.StringProperty()
	street = db.StringProperty()
	city = db.StringProperty()
	zipCode = db.StringProperty()
	state = db.StringProperty()
	phone = db.StringProperty()
	email = db.StringProperty()
	photo = db.BlobProperty()

# Pages

class viewPage(webapp2.RequestHandler):
	def get(self):
		self.response.write(MAIN_HEADER % 'View Contacts')
		self.response.write("""
			<h1>Address Book</h1>
		</div>
		<div data-role="navbar">
			<ul>
				<li><a href="#" class="ui-btn-active">View All People</a></li>
				<li><a href="/select">Filter Through People</a></li>
				<li><a href="/enter">Add A Person</a></li>
			</ul>
		</div>""")
		self.response.write("<br><h2 class='ui-header ui-bar-b'>Current Contacts</h2><br>")
		self.response.write("<div class='ui-grid-d'>")
		contacts = User.gql(" ORDER BY lName ASC")
		#User.query(db.AND(User._properties['state'] == 'OK'),User._properties['fName'] == 'Daniel')
		# contacts = User.query()
		# 	self.response.write('<h6>' + str(contact.key) + '</h6>')
		column = 0
		for contact in contacts:
			if column % 5 == 0:
				self.response.write("</div><br><div class='ui-grid-d'>")
				grid = 'a'
			elif column % 5 == 1:
				grid = 'b'
			elif column % 5 == 2:
				grid = 'c'
			elif column % 5 == 3:
				grid = 'd'
			else:
				grid = 'e'
			self.response.write('<div class="ui-block-%s ui-bar-e"><img src="/img?photo=%s" alt="%s"><br>' % (grid, contact.key(), cgi.escape(contact.fName)))
			self.response.write(cgi.escape(contact.fName) + ' ' + cgi.escape(contact.lName) + '<br>')
			self.response.write(cgi.escape(contact.street) + '<br>' + cgi.escape(contact.city) + ', ' + cgi.escape(contact.state) + ' ' + cgi.escape(contact.zipCode) + '<br><br>')
			self.response.write(cgi.escape(contact.phone) + '<br>')
			self.response.write(cgi.escape(contact.email) + '<br>')
			self.response.write('<div data-role="controlgroup">')
			self.response.write('<a href="/update?person=%s" class="ui-bar-b" data-role="button" data-inline="true" data-icon="gear">Update</a>' % contact.key())
			self.response.write('<a href="/delete?person=%s" class="ui-bar-b" data-role="button" data-inline="true" data-icon="delete">Delete</a>' % contact.key())
			self.response.write('</div></div>')
			column = column + 1
		self.response.write(MAIN_END)

class deleteEntry(webapp2.RequestHandler):
	def get(self):
		user = db.get(self.request.get('person'))
		User.delete(user)
		self.response.write("""<meta http-equiv="refresh" content="0.5;URL='/'">""")

class updateEntry(webapp2.RequestHandler):
	def get(self):
		user = db.get(self.request.get('person'))
		self.response.write(MAIN_HEADER % 'Update Contact')
		self.response.write("""
			<h1>Address Book</h1>
		</div>
		<div data-role="navbar">
			<ul>
				<li><a href="">View All</a></li>
				<li><a href="/select">Filter People</a></li>
				<li><a href="/enter">Add Person</a></li>
			</ul>
		</div>""")
		formOutput = (FORM_INPUT % (cgi.escape(user.fName), cgi.escape(user.lName), cgi.escape(user.street), cgi.escape(user.city), cgi.escape(user.zipCode), cgi.escape(user.phone), cgi.escape(user.email)))
		self.response.write(formOutput)
		User.delete(user)
		self.response.write(MAIN_END)

class enterPage(webapp2.RequestHandler):

	def get(self):
		self.response.write(MAIN_HEADER % 'New Entry')
		self.response.write("""
			<h1>Address Book</h1>
		</div>
		<div data-role="navbar">
			<ul>
				<li><a href="/">View All</a></li>
				<li><a href="/select">Filter People</a></li>
				<li><a href="#" class="ui-btn-active">Add Person</a></li>
			</ul>
		</div>""")

		self.response.write(FORM_INPUT % ("", "", "", "", "", "", ""))
		self.response.write(MAIN_END)
		

class uploadAll(webapp2.RequestHandler):
	def post(self):
		newPerson = User()
		newPerson.fName = self.request.get('fName')
		newPerson.lName = self.request.get('lName')
		newPerson.street = self.request.get('street')
		newPerson.city = self.request.get('city')
		newPerson.zipCode = self.request.get('zipCode')
		newPerson.state = self.request.get('state')
		newPerson.phone = self.request.get('phone')
		newPerson.email = self.request.get('email')
		photo = images.resize(self.request.get('photo'), 64, 64)
		newPerson.photo = db.Blob(photo)

		newPerson.put()
		self.response.write("""<meta http-equiv="refresh" content="0.5;URL='/'">""")

class selectEntry(webapp2.RequestHandler):
	def get(self):
		self.response.write(MAIN_HEADER % 'Select Entries')
		self.response.write("""
			<h1>Address Book</h1>
		</div>
		<div data-role="navbar">
			<ul>
				<li><a href="/">View All</a></li>
				<li><a href="/select" class="ui-btn-active">Filter People</a></li>
				<li><a href="/enter">Add Person</a></li>
			</ul>
		</div>""")
		self.response.write("""
			<div data-role="content" class="ui-content" role="main">
			<div class="center-wrapper">
			<br>
			<form action='/query' method='post' data-ajax='false'>
				<select name='query' id='query'>
					<option value='fName'>First Name</option>
					<option value='lName'>Last Name</option>
					<option value='street'>Street</option>
					<option value='city'>City</option>
					<option value='state'>State</option>
					<option value='zipCode'>Zip Code</option>
					<option value='phone'>Phone Number</option>
					<option value='email'>Email</option>
				</select>
				<label for='value'>Query Field</label>
				<input type='text' name='value' id='value'>

				<input type='submit' value='Query' data-icon="search">
			</form>
			</div>
			""")
		self.response.write(MAIN_END)

class filterQuery(webapp2.RequestHandler):
	def post(self):
		self.response.write(MAIN_HEADER % 'Query Results')
		queryField = self.request.get('query')
		queryValue = self.request.get('value')
		queryString = (" WHERE %s = '%s' ") % (queryField, queryValue)
		#contacts = User.gql("WHERE fName = 'Elmer'")
		contacts = User.gql(queryString)
		self.response.write("""
			<h1>Address Book</h1>
		</div>
		<div data-role="navbar">
			<ul>
				<li><a href="/">View All</a></li>
				<li><a href="/select">Filter People</a></li>
				<li><a href="/enter">Add Person</a></li>
			</ul>
		</div>""")
		self.response.write("<br><h2 class='ui-header ui-bar-b'>Results</h2><br>")
		self.response.write("<div class='ui-grid-d'>")
		column = 0
		for contact in contacts:
			if column % 5 == 0:
				self.response.write("</div><br><div class='ui-grid-d'>")
				grid = 'a'
			elif column % 5 == 1:
				grid = 'b'
			elif column % 5 == 2:
				grid = 'c'
			elif column % 5 == 3:
				grid = 'd'
			else:
				grid = 'e'
			self.response.write('<div class="ui-block-%s ui-bar-e"><img src="/img?photo=%s" alt="%s"><br>' % (grid, contact.key(), cgi.escape(contact.fName)))
			self.response.write(cgi.escape(contact.fName) + ' ' + cgi.escape(contact.lName) + '<br>')
			self.response.write(cgi.escape(contact.street) + '<br>' + cgi.escape(contact.city) + ', ' + cgi.escape(contact.state) + ' ' + cgi.escape(contact.zipCode) + '<br><br>')
			self.response.write(cgi.escape(contact.phone) + '<br>')
			self.response.write(cgi.escape(contact.email) + '<br>')
			self.response.write('<div data-role="controlgroup">')
			self.response.write('<a href="/update?person=%s" class="ui-bar-b" data-role="button" data-inline="true" data-icon="gear">Update</a>' % contact.key())
			self.response.write('<a href="/delete?person=%s" class="ui-bar-b" data-role="button" data-inline="true" data-icon="delete">Delete</a>' % contact.key())
			self.response.write('</div></div>')
			column = column + 1

# Application to display image

class image(webapp2.RequestHandler):
    def get(self):
        user = db.get(self.request.get('photo'))
        if user.photo:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(user.photo)
        else:
            self.response.out.write('No image')

application = webapp2.WSGIApplication([
	('/', viewPage),
	('/enter', enterPage),
	('/add', uploadAll),
	('/query', filterQuery),
	('/update', updateEntry),
	('/delete',deleteEntry),
	('/select',selectEntry),
	('/img', image), ], debug=True)