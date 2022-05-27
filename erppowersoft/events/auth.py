import frappe
from frappe import _
from frappe.utils.data import today, date_diff, get_datetime_str
import json

def successful_login(login_manager):
    """
    on_login verify if site is not expired
    """
    expiry = frappe.db.get_single_value('PS Info', 'site_expiry_date')
    email = frappe.db.get_single_value('PS Info', 'support_email')
    phone = frappe.db.get_single_value('PS Info', 'support_phone')
    print(expiry)
    # with open(frappe.get_site_path('quota.json')) as jsonfile:
    #     parsed = json.load(jsonfile)
    
    # valid_till = parsed['valid_till']
    diff = date_diff(expiry, today())
    if login_manager.user != "Administrator" and diff < 0:
        frappe.throw(_("You site is suspended. Please contact PowerSoft <br> Email: {0} <br>Phone: {1}").format(email,phone), frappe.AuthenticationError)

def user_limit(self, method):
    no_users = frappe.db.get_single_value('PS Info', 'no_of_users')
    print(no_users)
    
    user_list = frappe.get_list('User', filters={'enabled': 1,"name":['not in',['Guest', 'Administrator']]})
    active_users = len(user_list)
    print(active_users)

    email = frappe.db.get_single_value('PS Info', 'support_email')
    phone = frappe.db.get_single_value('PS Info', 'support_phone')
    
    if no_users != 0 and active_users > no_users:
        frappe.throw(_("Allow Users:{0}, Active Users:{1}<br>You have exceeded your Users limit <br> Please disable users or to increase the limit please contact <br> Email: {2} <br> Phone: {3}").format(no_users,active_users,email,phone))