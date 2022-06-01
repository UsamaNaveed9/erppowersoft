from concurrent.futures.process import _python_exit
import email
import frappe
from frappe import _
from frappe.utils.data import today, date_diff, get_datetime_str
import json

def successful_login(login_manager):
    """
    on_login verify if site is not expired
    """

    #get email and phone and expiry date from PS Info
    expiry = frappe.db.get_single_value('PS Info', 'site_expiry_date')
    email = frappe.db.get_single_value('PS Info', 'support_email')
    phone = frappe.db.get_single_value('PS Info', 'support_phone')
    #print(expiry)
    
    diff = date_diff(expiry, today())
    if login_manager.user != "Administrator" and diff < 0:
        frappe.throw(_("Your account has been suspended as your subscription has expired. <br> Contact our billing & sales team as per below details and make payment to renew your subscription <br> Email: {0} <br>Phone: {1}").format(email,phone), frappe.AuthenticationError)

def user_limit(self, method):
    #get no of users from ps info
    allow_users = frappe.db.get_single_value('PS Info', 'no_of_users')
    #print(allow_users)
    
    #get list of active user
    user_list = frappe.get_list('User', filters={'enabled': 1,"name":['not in',['Guest', 'Administrator']]})
    active_users = len(user_list)
    #print(active_users)

    #get email and phone from PS Info
    email = frappe.db.get_single_value('PS Info', 'support_email')
    phone = frappe.db.get_single_value('PS Info', 'support_phone')
    
    if allow_users != 0 and active_users > allow_users:
        frappe.throw(_("Purchased User Licenses: {0}, Creating {1} User<br>You cannot create additional user as you have reached the limit of active user count you have purchased.<br> Please disable some of the active users to create additional user or contact our sales & billing team as per below details and make payment for additional users.<br> Email: {2} <br> Phone: {3}").format(allow_users,active_users,email,phone))
        

# Company    
def company_limit(self, method):
    '''Validates Company limit'''

    #get no of companies from ps info
    allowed_companies = frappe.db.get_single_value('PS Info', 'no_of_companies')
    #print(allowed_companies)
  
    # Calculating total companies
    total_company = len(frappe.db.get_all('Company',filters={}))
    #print(total_company)
    
    #get email and phone from PS Info
    email = frappe.db.get_single_value('PS Info', 'support_email')
    phone = frappe.db.get_single_value('PS Info', 'support_phone')

    # Validation
    if allowed_companies != 0 and total_company >= allowed_companies:
        frappe.throw(_("Purchased Subsidiary Licenses: {}<br>You have {} company(s).<br>You cannot create additionl company/subsidiary as you have reached the limit of active subsidiaries subscription you have purchased.<br>Please disable some of the active subsidiaries if not required or contact our sales & billing team as per below details and make payment for subsidiary.<br>Email: {}<br> Phone: {}").format(allowed_companies, total_company,email,phone))

