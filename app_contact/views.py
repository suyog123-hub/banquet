from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .serializer import Contactserializer
from .models import contact
from config.response import *
from config.pagination import Detailpage
from config.permission import AdminGetOrPostAll
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class contactview(APIView):
    permission_classes =[ AdminGetOrPostAll]
    pagination_class = Detailpage
    def get(self, request):
        
        student = contact.objects.all().order_by('id')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(student, request)
        serializer = Contactserializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        try:
            serializer = Contactserializer(data=request.data)
            
            if serializer.is_valid():
                contact_instance = serializer.save()
                
                try:
                    send_mail(
                        subject='Thank You for Contacting Us',
                        message=f"""
                            Dear {contact_instance.name},

                            Thank you for reaching out to us. We have received your message and will get back to you within 24 hours.

                            Here's a summary of your message:
                            --------------------------------
                            Name: {contact_instance.name}
                            Email: {contact_instance.email}
                            Phone: {contact_instance.phone}
                            Message: {contact_instance.message}
                            --------------------------------

                            Best regards,
                            Sajha Info Tech
                        """,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[contact_instance.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass
                
                return success_response('Your message has been sent successfully. You will receive a confirmation email shortly.', serializer.data)
            
            return validation_error_response(serializer.errors)
            
        except Exception as e:
            return server_error_response()

