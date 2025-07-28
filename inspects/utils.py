from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from random import randint
import os
import uuid
from django.conf import settings



# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

# def save_pdf(params:dict):
#     template=get_template('search_location_detail.html')
#     html=template.render(params)
#     response=BytesIO()
#     pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
#     file_name=uuid.uuid4()
#     try:
#         with open(str(settings.BASE_DIR)+f'/static/(file_name).pdf', 'wb+') as output:
#             pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
#     except Exception as e:
#         print(e)
        
#     if pdf.err:
#         return '', False
#     return file_name, True
            


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    #pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, encoding="ISO-8859-1")
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8', link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def render_to_file(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    file_name = "{0}.pdf".format(randint(1, 1000000))
    file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")),"media/temp", file_name)
    with open(file_path, 'wb') as pdf:
        pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
    return file_name

def link_callback(uri, rel):
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
        return path
    return uri

# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template
# from weasyprint import HTML
# from random import randint
# import os
# import uuid
# from django.conf import settings

# def render_to_pdf(template_src, context_dict={}):
#     """
#     Render an HTML template to PDF using WeasyPrint and return as HttpResponse.
#     """
#     # Load and render the HTML template with context
#     template = get_template(template_src)
#     html = template.render(context_dict)
    
#     # Use WeasyPrint to generate the PDF
#     pdf = HTML(string=html).write_pdf()
    
#     # Return the PDF as an HTTP response
#     return HttpResponse(pdf, content_type='application/pdf')

# def render_to_file(template_src, context_dict={}):
#     """
#     Render an HTML template to PDF using WeasyPrint and save it as a file.
#     """
#     # Load and render the HTML template with context
#     template = get_template(template_src)
#     html = template.render(context_dict)
    
#     # Generate a unique file name and file path for saving the PDF
#     file_name = "{0}.pdf".format(randint(1, 1000000))
#     file_path = os.path.join(settings.BASE_DIR, "media/temp", file_name)
    
#     # Generate the PDF and save it to the file path
#     HTML(string=html).write_pdf(target=file_path)
    
#     return file_name

