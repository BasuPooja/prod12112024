
import logging
import traceback
middleware_data = {}
logger = logging.getLogger(__name__)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def extract_browser_and_os(user_agent_string):
    # Check if user agent string is provided
    if not user_agent_string:
        return 'Unknown', 'Unknown'

    # List of common browser names
    browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera', 'Internet Explorer']

    # List of common operating systems
    operating_systems = ['Windows', 'Macintosh', 'Linux', 'Android', 'iOS']

    browser_name = 'Unknown'
    browser_version = 'Unknown'
    os_name = 'Unknown'

    # Iterate through the list of browsers
    for browser in browsers:
        if browser in user_agent_string:
            # Extract browser name
            browser_name = browser

            # Extract browser version (assuming it follows the browser name)
            version_index = user_agent_string.find(browser) + len(browser) + 1
            browser_version = user_agent_string[version_index:].split(' ')[0]
            break

    # Iterate through the list of operating systems
    for os in operating_systems:
        if os in user_agent_string:
            # Extract OS name
            os_name = os
            break

    return f'{browser_name} {browser_version}', os_name

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent_string = request.META.get('HTTP_USER_AGENT', 'Unknown')
        browser_details, os_details = extract_browser_and_os(user_agent_string)
        client_ip = get_client_ip(request)
        global middleware_data
        middleware_data['browser_details'] = browser_details
        middleware_data['os_details'] = os_details

        if 'user_id' in request.session:
            middleware_data['user_id'] = request.session['user_id']
        else:
            middleware_data['user_id'] = request.user
        middleware_data['ip'] = client_ip

        response = self.get_response(request)
        return response

from django.utils.timezone import now
class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Get current datetime
        current_datetime = now().strftime('%Y-%m-%d %H:%M:%S')
        # Get the log message using the getMessage() method
        # log_message = record.getMessage()

        # If it's an exception record, add exception details
        if record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            # Format exception details
            exception_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            # Construct log message with exception details
            log_message = f"{record.getMessage()}\nException: {exception_details}"
        else:
            log_message = record.getMessage()
        
        # fetch data from the global variable
        browser_details = middleware_data.get('browser_details', 'Unknown')
        os_details = middleware_data.get('os_details', 'Unknown')
        user_id = middleware_data.get('user_id', 'Unknown')
        ip = middleware_data.get('ip', 'Unknown')
        
        formatted_message = f'Date:- {current_datetime}, Username:- {user_id}, ip:- {ip}, Browser: {browser_details}, OS: {os_details} \nLog Message: {log_message}'
        
        return formatted_message
  


