#Data models

from flask_sqlalchemy import SQLAlchemy 
#create instance of the database
db=SQLAlchemy()

#First entity
class Customer_Info(db.Model):
	__tablename__="customers"
	 # Primary Key
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Basic Information
    name = db.Column(db.String(100), nullable=False)  # Name cannot be null
    email_id = db.Column(db.String(150), unique=True, nullable=False)  # Unique to avoid duplicates
    # password_hash = db.Column(db.String(128), nullable=False)  # Store hashed passwords
    password=db.Column(db.String, nullable=False)

    # Address and Location
    address = db.Column(db.Text, nullable=True)  # Optional detailed address
    pincode = db.Column(db.String(6), nullable=False)  # Assumes 6-digit Indian pin codes
    
    # Metadata
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically sets the creation date
    is_blocked = db.Column(db.Boolean, default=False)  # Defaults to unblocked

    # Relationships (Optional for linking to service requests)
    # service_requests = db.relationship('ServiceRequested', backref='customer', lazy=True)
    
    #Customer.requests = db.relationship('ServiceRequest', back_populates='customer', lazy=True)
    # Methods
    #def set_password(self, password):
        """Hash and set the user's password."""
        #self.password_hash = generate_password_hash(password)

    #def check_password(self, password):
        """Verify the user's password."""
        #return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Customer {self.name} - {self.email_id}>"


#Second Entity Professionals
class Professional(db.Model):
    __tablename__ = 'professionals'

    # Primary Key
    professional_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Basic Information
    name = db.Column(db.String(100), nullable=False)  # Full name of the professional
    email_id = db.Column(db.String(150), unique=True, nullable=False)  # Unique email for login
    password=db.Column(db.String, nullable=False)
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
    #service_requests = db.relationship('ServiceRequested', backref='professional', lazy=True)
    #Professional.assigned_requests = db.relationship('ServiceRequest', back_populates='professional', lazy=True)
    # Methods
    #def set_password(self, password):
        """Hash and set the professional's password."""
        #self.password_hash = generate_password_hash(password)

    #def check_password(self, password):
        """Verify the professional's password."""
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
    __tablename__ = 'services'  # Table name in the database

    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    service_name = db.Column(db.String(255), nullable=False)  # Name of the service
    description = db.Column(db.Text)  # Description of the service
    base_price = db.Column(db.Numeric(10, 2), nullable=False)  # Base price for the service
    time_required = db.Column(db.Integer, nullable=False)  # Time required in minutes
    #category = db.Column(db.String(100))  # Optional category for the service
    #rating = db.Column(db.Numeric(3, 2), default=0)  # Average rating (optional)
    #total_requests = db.Column(db.Integer, default=0)  # Total service requests made
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())  # Timestamp when service is created
   	#Service.requests = db.relationship('ServiceRequest', back_populates='services', lazy=True)


class ServiceRequested(db.Model):
	__tablename__ = 'service_requests'

    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.professional_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), nullable=False)
	requirements = db.Column(db.String(255), nullable=True)  # Customer's service requirements or special requests
    service_date = db.Column(db.Date, nullable=False)
    service_time = db.Column(db.String(50), nullable=False)  # Store time in a string format (e.g., "10:00 AM")
    status = db.Column(db.String(20), nullable=False, default='Pending')  # Example: "Pending", "In Progress", "Completed"
    rating = db.Column(db.Float, nullable=True)  # Customer rating, optional
    remarks = db.Column(db.Text, nullable=True)  # Remarks or feedback about the professional
	date_requested = db.Column(db.DateTime, default=datetime.utcnow)


    # Relationships
    #service = db.relationship('Service', back_populates='requests')
    #customer = db.relationship('Customer', back_populates='requests')
    #professional = db.relationship('Professional', back_populates='assigned_requests', lazy=True)
    def __repr__(self):
        return f"<ServiceRequest {self.request_id} - {self.status}>"




