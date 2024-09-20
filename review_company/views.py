from django.shortcuts import render
from review_company.models import Review


def company_reviews_page(request, company_name):
    reviews = Review.objects.filter(company__name=company_name).first()
    return render(request, 'Reviews.html', {'reviews': reviews, 'title': company_name})
