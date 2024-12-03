#App routes
from flask import Flask,render_template,request,flash,url_for,redirect
from flask import current_app as app
from .models import *
#Many controllers/routers here 

@app.route("/")
def home():
	return render_template("index.html")


@app.route("/login", methods=["GET","POST"])
def signing():
	if request.method=="POST":
		username=request.form.get("user_name")
		pwd=request.form.get("password")

		customer=Customer_Info.query.filter_by(email_id=username, password=pwd).first()
		professional=Professional.query.filter_by(email_id=username, password=pwd).first()

		if username == "admin@homeease.in" and pwd == "admin":
			#return render_template("admin_dashboard.html")
			return redirect(url_for("admin_dashboard", name=username))

		elif customer:
			return render_template("customer_dashboard.html", name=name)
		elif professional:
			return render_template("professional_dashboard.html", name=name)
		else:
			return render_template("login.html",msg='Invalid User Credentials....please try again')

	return render_template("login.html",msg='')


@app.route("/customer_register",methods=["GET","POST"])
def customer_signup():
	if request.method=="POST":
		uname=request.form.get("email")
		password=request.form.get("password")
		name=request.form.get("name")
		mobile_no=request.form.get("mobile_no")
		address=request.form.get("location")
		pincode=request.form.get("pincode")

		usr=Customer_Info.query.filter_by(email_id=uname).first()
		if usr:

			return render_template("customer_registration.html",msg="The Mail is Already registered!!!")
			flash("User Already Exist")


		new_customer=Customer_Info(email_id=uname,password=password,name=name,address=address,pincode=pincode)
		db.session.add(new_customer)
		db.session.commit()
		return render_template("login.html", msg='Registration Successful, try login now....')

	return render_template("customer_registration.html", msg='')


@app.route("/professional_register",methods=["GET","POST"])
def professional_signup():
	if request.method=="POST":
		prof_uname=request.form.get("email")
		password=request.form.get("password")
		name=request.form.get("name")
		mobile_no=request.form.get("mobile_no")
		address=request.form.get("location")
		pincode=request.form.get("pincode")
		govt_id=request.form.get("govt_id")
		service_id=request.form.get("service_id")
		experience_years=request.form.get("experience")

		existing_user = Professional.query.filter_by(email_id=prof_uname).first()
		if existing_user:
			return render_template("professional_registration.html",msg="This Mail is Already registered!!!")

		#usr=Professional.query.filter_by(email_id=prof_uname)
		#if usr:

			#return render_template("professional_registration.html",msg="This Mail is Already registered!!!")
			#flash("User Already Exist")
		new_professional=Professional(email_id=prof_uname,password=password,name=name,address=address,pincode=pincode,mobile_no=mobile_no,govt_id=govt_id,service_id=service_id,experience_years=experience_years)
		db.session.add(new_professional)
		db.session.commit()
		return render_template("login.html", msg='Submission Successful, Registration Under Verification....')
	return render_template("professional_registration.html", msg='')

#Common route for admin dashboard
@app.route("/admin")
def admin_dashboard():
	pending_requests=Professional.query.filter_by(approve_status=0).all()

        # Query to get professionals with their service names
	professionals = db.session.query(Professional, Service.service_name).join(Service, Professional.service_id == Service.service_id).filter(Professional.approve_status == 0).all()
	return render_template("admin_dashboard.html",pending_requests=pending_requests,professionals=professionals)
	
# Fetch the pending requests for the professional's service

#Common route for Service dashboard
@app.route("/admin/services")
def admin_services():
	services = Service.query.all()
	return render_template("services.html", services=services)

#Common route for Customer Dashboard
#@app.route("/cutomer")

#adding new services
@app.route("/admin/services/add", methods=["GET","POST"])
def add_service():
	if request.method=="POST":
		service_name=request.form.get("service_name")
		description=request.form.get("description")
		base_price=request.form.get("base_price")
		time_required=request.form.get("time_required")
		new_service=Service(service_name=service_name,description=description,base_price=base_price,time_required=time_required)
		db.session.add(new_service)
		db.session.commit()
		flash("Service Added Successfully!")
		return redirect(url_for("admin_services"))

	return redirect(url_for("admin_services"))
