from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Watches
from .forms import WatchForm
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RatingCommentForm    
from django.contrib.auth.decorators import login_required


# Create your views here.
def home (request):
    # watches = Watches.objects.all()
    brands= Watches.objects.values_list('brand', flat=True).distinct()
    selected_brand = request.GET.get('q')
    if selected_brand:
        watches = Watches.objects.filter(brand=selected_brand)
    else:
        watches= Watches.objects.all()
    
    context ={'watch_list':watches, 'brands':brands}
    return render(request,'HomePage/home.html', context)

def ShowProduct(request,pk):
    # print(pk, name)
    # watches = Watches.objects.all()
    # for watch in watches:
    #     if watch.id==int(pk):
    #         break
    selected_watch = get_object_or_404(Watches,pk=pk)
    rate = selected_watch.average_rating()
    reviews =selected_watch.ratings.all()
    context = {"product":selected_watch, "reviews":reviews,"avrg_rate":rate}
    return render(request, 'product.html',context)
                      
# @login_required
# def add_rating_comment(request, product_id):
#     watch = get_object_or_404(Watches, product_id)
#     user =request.user
#     if request.method =='POST':
#         form = RatingCommentForm(request.POST)
#         if form.is_valid():
#             rating_form = form.save(commit=False)
#             rating_form.user = request.user
#             rating_form.product = watch
#             rating_form.save()
#             return redirect('product',pk=product_id)
#     else:
#         form = RatingCommentForm()
#         context = {'form':form, 'product':product}
#     return render(request,'HomePage/comment.html', context)


from django.views import View
from HomePage.models import RatingComment
class AddRatingComment(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        print("User authenticated:", request.user.is_authenticated)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, pk):
        product = get_object_or_404(Watches, pk=pk)
        form =RatingCommentForm(request.POST)
        rating_comment = None 
        if form.is_valid():      
            rating_comment = form.save(commit=False)
            rating_comment.product = product
            if request.user.is_authenticated:
                rating_comment.user = request.user  # Associate the logged-in user
            else:
                print("User is not authenticated, skipping user assignment")               
            rating_comment.save()
            return redirect('product', pk=pk)
        
    def get(self,request, pk):
        product = get_object_or_404(Watches, pk=pk)
        form =RatingCommentForm
        context = {'form':form, 'product':product}
        return render(request, 'HomePage/comments.html', context)
    

class EditRatingComment(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        comment = get_object_or_404(RatingComment, pk=self.kwargs['pk'])
        return self.request.user == comment.user

    def post(self, request, pk):
        comment = get_object_or_404(RatingComment, pk=pk)
        form = RatingCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('product', pk=comment.product.id)
        return render(request, 'HomePage/edit_comment.html', {'form': form})

    def get(self, request, pk):
        comment = get_object_or_404(RatingComment, pk=pk)
        form = RatingCommentForm(instance=comment)
        return render(request, 'HomePage/edit_comment.html', {'form': form})
    

class DeleteRatingComment(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        comment = get_object_or_404(RatingComment, pk=self.kwargs['pk'])
        return self.request.user == comment.user

    def post(self, request, pk):
        comment = get_object_or_404(RatingComment, pk=pk)
        product_id = comment.product.id
        comment.delete()
        return redirect('product', pk=product_id)

    def get(self, request, pk):
        comment = get_object_or_404(RatingComment, pk=pk)
        return render(request, 'HomePage/delete_comment.html', {'comment': comment})

    
# from .forms import RatingCommentForm
# @login_required
# def Reviews_Old(request,pk):
#     watch = get_object_or_404(Watches,id=pk)
#     user =request.user
#     if request.method == "POST":
#         form =RatingCommentForm(request.POST)
#         if form.is_valid():
#             rating_form = form.save(commit=False)
#             rating_form.user = user
#             rating_form.product = watch
#             rating_form.save()
#             return redirect('product', pk=watch.id)
#     else:   
#         form = RatingCommentForm()
#     context = {"form":form}    
#     return render(request, 'HomePage/comments.html', context)

from django.views import View
class Reviews(LoginRequiredMixin, View):
    def get(self,request,product_id):
        watch = get_object_or_404(Watches,id=watch.id)
        form = RatingCommentForm()
        context = {"form":form}  
        return render(request, 'HomePage/comments.html', context)

    def post(self,request,product_id):
        watch = get_object_or_404(Watches,id=watch.id)
        user = request.user
        form = RatingCommentForm(request.POST)
        if form.is_valid():
            rating_form = form.save(commit=False)
            rating_form.user = user
            rating_form.product = watch
            rating_form.save()
            return redirect('product', pk=watch.id)


@login_required
def AddWatch(request):
    if request.method == "POST":
        form = WatchForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                print("Validation successful")
                form.save()  # Attempt to save the new Watch
                return redirect('home')
            except IntegrityError as e:
                print("Error saving watch:", e)
            except Exception as e:
                print("Unexpected error:", e)
        else:
            print("Form errors:", form.errors)
    else:
        form = WatchForm()        
    context = {"form": form}
    return render(request, 'HomePage/add_product.html', context)

from django.shortcuts import get_object_or_404
@login_required
def EditWatch(request,pk):
    selected_watch =get_object_or_404(Watches,pk=pk)
    if request.method == "POST":
        form = WatchForm(request.POST,request.FILES, instance =selected_watch)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = WatchForm(instance=selected_watch)
    context = {"form":form}
    return render(request, "HomePage/edit_product.html", context)

@login_required
def DeleteWatch(request, pk):   
    # Attempt to retrieve the watch object
    selected_wat = get_object_or_404(Watches, pk=pk)   
    if selected_wat.image: 
        try:
            selected_wat.image.delete(save=False)  # Delete the image file from storage
            print("Associated image deleted successfully.")
        except Exception as e:
            print(f"Failed to delete associated image: {e}")
    
    # Delete the watch object itself
    selected_wat.delete()
    print(f"Watch with id {pk} deleted successfully.")
    
    return redirect('home')

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate, logout
# from forms import LoginForm

def LoginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=user_name, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:        
            form.add_error(None, "Invalid username or password.")
    else:        
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "HomePage/login.html",context)

@login_required
def LogoutPage(request):
    logout(request)
    return redirect('home')

from .models import Watches
from django.http import JsonResponse
def SearchProduct(request):
    search_item =request.GET.get('q')
    # print ("\n"*3, search_item)
    watches = Watches.objects.filter(name__icontains = search_item)
    
    result = []
    for watch in watches:
        item = {
            "id": watch.id,
            "name": watch.name,
            "brand": watch.brand,
            "image": watch.image.url,
            "description": watch.description,
            "price": watch.price,
        }
        result.append(item)
    print(watches)
    return JsonResponse({"results":result})