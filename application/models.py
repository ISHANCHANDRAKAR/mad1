from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Customer_Info(db.Model):
	__tablename__ = 'customers'
	customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	email_id = db.Column(db.String(150), unique=True, nullable=False)
	password=db.Column(db.String, nullable=False)
	address = db.Column(db.Text, nullable=True)
	pincode = db.Column(db.String(6), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
	is_blocked = db.Column(db.Boolean, default=False)
	service_requests = db.relationship('ServiceRequested', backref='customers', lazy=True)

	def __repr__(self):
		return f'<Customer {self.name} - {self.email_id}>'

#Second Entity Professionals
class Professional(db.Model):
    __tablename__ = 'professionals'

    # Primary Key
    professional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Basic Information
    name = db.Column(db.String(100), nullable=False)  # Full name of the professional
    email_id = db.Column(db.String(150), unique=True, nullable=False)  # Unique email for login
    password=db.Column(db.String, nullable=False)
    govt_id=db.Column(db.String, nullable=True)
    mobile_no=db.Column(db.Integer, nullable=True)
    #password_hash = db.Column(db.String(128), nullable=False)  # Hashed password

    # Service Details
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)  # Links to the services table
    experience_years = db.Column(db.Integer, nullable=False, default=0)  # Experience in years

    # Address and Location
    address = db.Column(db.Text, nullable=True)  # Optional detailed address
    pincode = db.Column(db.String(6), nullable=False)  # 6-digit Indian pin code

    # Status Information
    approve_status = db.Column(db.Boolean, default=False)  # Defaults to unapproved
    active_status = db.Column(db.Boolean, default=True)  # Active/inactive professional status

    # Additional Information
    total_services_done = db.Column(db.Integer, default=0)  # Tracks the number of completed services
    average_rating = db.Column(db.Float, default=0.0)  # Average rating from customer reviews

    # Metadata
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically sets the creation timestamp

    # Relationships
    service_requests = db.relationship('ServiceRequested', backref='professionals', lazy=True)
    #service = db.relationship('Service', back_populates='professionals', lazy=True)
    #Professional.assigned_requests = db.relationship('ServiceRequest', back_populates='professional', lazy=True)
    # Methods
    #def set_password(self, password):
        #Hash and set the professional's password.
        #self.password_hash = generate_password_hash(password)

    #def check_password(self, password):
        #Verify the professional's password.
        #return check_password_hash(self.password_hash, password)

# Computed Properties
    @property
    def total_services_done(self):
        """Calculate total completed services dynamically."""
        return ServiceRequested.query.filter_by(professional_id=self.professional_id, status='Completed').count()

    @property
    def average_rating(self):
        """Calculate the average rating dynamically."""
        completed_requests = ServiceRequested.query.filter_by(professional_id=self.professional_id, status='Completed').all()
        if not completed_requests:
            return 0.0
        total_rating = sum(request.rating for request in completed_requests if request.rating is not None)
        rated_requests = sum(1 for request in completed_requests if request.rating is not None)
        return total_rating / rated_requests if rated_requests > 0 else 0.0

    def update_rating(self, new_rating):
        """Update the average rating for the professional."""
        if self.total_services_done > 0:
            self.average_rating = ((self.average_rating * self.total_services_done) + new_rating) / (self.total_services_done + 1)
        else:
            self.average_rating = new_rating
        self.total_services_done += 1

    def __repr__(self):
        return f"<Professional {self.name} - {self.email_id}>"

class Service(db.Model):
	__tablename__ = 'services'
	service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	service_name = db.Column(db.String(255), nullable=False, unique=True)
	description = db.Column(db.Text)
	base_price = db.Column(db.Numeric(10, 2), nullable=False)
	time_required = db.Column(db.Integer, nullable=False)
	creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
	professionals = db.relationship('Professional', backref='services', lazy=True)
	service_requests = db.relationship('ServiceRequested', backref='services', lazy=True)
	def __repr__(self):
		return f'<Service {self.service_name} - Price: {self.base_price} - Time: {self.time_required} - Status: {self.service_status}>'

class ServiceRequested(db.Model):
	__tablename__ = 'service_requests'
	request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
	professional_id = db.Column(db.Integer, db.ForeignKey('professionals.professional_id'), nullable=False)
	service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
	requirements = db.Column(db.String(255), nullable=True)
	service_date = db.Column(db.Date, nullable=False)
	service_time = db.Column(db.String(50), nullable=False)
	status = db.Column(db.String(20), nullable=False, default='Pending')
	rating = db.Column(db.Float, nullable=True)
	remarks = db.Column(db.Text, nullable=True)
	date_requested = db.Column(db.DateTime, default=datetime.utcnow)
	def __repr__(self):
		return f'<ServiceRequest {self.request_id} - {self.status}>'