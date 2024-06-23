from django.shortcuts import render, redirect
from .models import product_model
from .forms import product_form
from .scan import  begin_scan, recommend_products_by_user_features, disease_scan, begin_disease_scan
from django.contrib.auth import logout
from django.contrib.auth.models import User


def skincare_scan(request):#This is the view for the homepage which will recommend skincare products 
    
        user = request.user.username
        print(user)
        if request.method == 'POST':
            form = product_form(request.POST)
            if form.is_valid():
                user_attrs = begin_scan() #A dictionary of all the users facial attributes that returned from the scan
                Concerns = form.cleaned_data['Concerns']# Adds the concern the user had (Acne, aging, etc.) and takes that into account when recommending
                print(Concerns)
                
                     
                     
                user_attrs['Concerns'] = Concerns
                print(user_attrs)
                recommend = recommend_products_by_user_features(user_attrs['Skin_tone'],
                                       user_attrs['Skin_type'],user_attrs['Eye_color'], user_attrs['Hair_color'], user_attrs['Concerns'])
                print(recommend)
                
                product_titles = recommend['Product']
                product_category = recommend['Category']
                product_url = recommend['Product_Url']
                product_brand = recommend['Brand']
                model = product_model()
                model.user = user
                model.product_1_title = product_titles.iloc[0]
                model.product_1_category = product_category.iloc[0]
                model.product_1_link = product_url.iloc[0]
                model.product_1_brand = product_brand.iloc[2]
                model.product_2_title = product_titles.iloc[1]
                model.product_2_category = product_category.iloc[1]
                model.product_2_link = product_url.iloc[1]
                model.product_2_brand = product_brand.iloc[2]
                model.product_3_title = product_titles.iloc[2]
                model.product_3_category = product_category.iloc[2]
                model.product_3_link = product_url.iloc[2]
                model.product_3_brand = product_brand.iloc[2]
                model.product_4_title = product_titles.iloc[3]
                model.product_4_category = product_category.iloc[3]
                model.product_4_link = product_url.iloc[3]
                model.product_4_brand = product_brand.iloc[3]
                model.save()

                #It will save the top 4 recommended products and save them in a database, 
                #that way even if the user logs out, they can always view what they were recommended, unless if they redo the scan                                    
                context = {
                    'saved_products': product_model.objects.all(),
                    'form': form
                    }
                
                return render(request, 'main.html', context=context)
        else: 
            form = product_form()
            context = {
                'form': form,
                'saved_products': product_model.objects.all()
                }
            return render(request, 'main.html', context=context)
    
def disease_scan(request):#The view for the disease detection function, go to scan.py to see what begin_disease_scan() does
    if(request.GET.get('startBtn')):
        results = begin_disease_scan()
        return render(request, 'detection.html', {'results': results})
    
    return render(request, 'detection.html')
          
def logoutview(request):
    logout(request)
    return render(request, 'registration/login.html')
