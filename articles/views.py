from django.contrib.auth.models import User
from django.db.models import Count
from django.http import request
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from .models import Article, Profile,User,Comment
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
    
    
)
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import (ArticleCreateForm,
        UserRegistrationform,
        UpdateProfileForm,
        UpdateProfilePic,
        CommentForm,
)
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin ,UserPassesTestMixin
from django.contrib.auth import login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required 
from taggit.models import Tag

class CustomLoginView(LoginView):
    template_name = 'articles/login_view.html'
    fields = '__all__'
    redirect_authenticated_user = True   #this will prevent logged in users to go to login page.
 
    def get_success_url(self):
        return reverse('articles:article-list')

 

class UserRegistration(FormView):
    template_name = 'articles/register.html'
    form_class = UserRegistrationform
    
    def get_success_url(self):
        return reverse('articles:article-list')
    #this method will override the get method of the Formview and will restrict users logged in from going to register page simply just by redirect.

    # redirect_authenticated_user = True
    # in here redirect_authenticated_user is not a property or attr so we create one for this.
    def get(self,*args,**kwargs):  
        if self.request.user.is_authenticated:
            return redirect('articles:article-list')
        return super(UserRegistration, self).get(self,*args,**kwargs)#this line means in other situation go for what you supposed to do.
    # POST method for recieving form
    def form_valid(self,form):
        user = form.save()

        if user is not None:
            login(self.request, user)   #this login method will login the user right after pressing submit button.
        return super(UserRegistration,self).form_valid(form)



class ArticleListView(ListView):
    template_name  = 'articles/article_list.html'
    paginate_by = 8

    def get_queryset(self):
        search_input  = self.request.GET.get('search-area')
        if search_input:
            return Article.objects.filter(title__contains=search_input )
        else:
            return Article.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # search_input = self.request.GET.get('search-area') or ''
        # if search_input:
        #     context['object_list'] = context['object_list'].filter(
        #         title__icontains=search_input)
        # context['search_input'] = search_input
        context['user_pic'] = Profile.objects.filter(_user__id = self.request.user.id).first()
        return context


class UserArticleView(ListView):
    template_name  = 'articles/specific_user_articles_list.html'
    queryset       = Article.objects.all()
    paginate_by    = 5
    
    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Article.objects.filter(user=user)
    
    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['object_list'] = context['object_list'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        context['user_pic'] = Profile.objects.filter(_user__id = self.request.user.id).first()
        return context

# list post view by tag
def list_article_view(request, tag_slug= None):
    object_list = Article.objects.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug =tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    paginator = Paginator(object_list,5)
    page      = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)

    return render(request, 'articles/tag_list.html', {'object_list': object_list, 'page':page,'articles':articles ,'tag':tag})




class ArticleCreateView(LoginRequiredMixin,CreateView):
    template_name ='articles/article_create.html'
    form_class = ArticleCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleCreateView,self).form_valid(form) 

    def get_success_url(self):
        return reverse('articles:article-cutomize')

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
    form_class = ArticleCreateForm
    template_name ='articles/article_update.html'
    queryset = Article.objects.all()

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.user:
            return True
        return False

def article_detail(request,  pk):

    article = get_object_or_404(Article, pk = pk)
    comments = article.comments.filter(active=True)

    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            messages.success(request,message='Your comment has been added successfuly.')
            form = CommentForm()  
    else:
        form = CommentForm()  

    article_tags_ids = article.tags.values_list('id',flat=True)
    similar_posts    = Article.objects.filter(tags__in=article_tags_ids).exclude(id=article.id)
    similar_posts    = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-released_date')
    return render(request,'articles/article_detail.html' , {'article':article,
    'comments':comments,
    'form': form,
    'similar_posts': similar_posts,
    })

# class ArticleDetailView(DetailView, FormView):

#     template_name = 'articles/article_detail.html'
#     form_class = CommentForm
#     queryset = Article.objects.all()

 
  
#     def get_object(self,*args, **kwargs):
#         object = super(ArticleDetailView,self).get_object()       
#         return object

#     obj      = get_object()
#     comments = obj.comments.filter(active=True)
#     def form_valid(self,form):
#             new_comment = form.save(commit=False)
#             new_comment.self.obj = self.obj
#             new_comment.save()
#             return super(UserRegistration,self).form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         context['comments'] = self.comments
#         return context
#     context = get_context_data()
#     print(context)


class ArticleDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    template_name = 'articles/article_delete.html'
    queryset = Article.objects.all()

    def get_success_url(self):
        return reverse('articles:article-cutomize')

    
    def test_func(self):
        article = self.get_object()
        if self.request.user == article.user:
            return True
        return False


    

class CustomListView(LoginRequiredMixin,ListView):
    model = Article
    template_name = 'articles/edit_article_list.html'
    paginate_by   = 6
    
    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)
 

  
#function view for contact page.
def contact_form_view(request,*args, **kwargs):
    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_content = request.POST['message-content']

        send_mail(
            message_name,
            message_content,
            message_email,
            ['prgm.pouya19@gmail.com']
        )
        return render(request, 'about.html',{'message_name':message_name})
    else:
        return render(request, 'about.html', {})


#function view for updating profile
def user_update_profile_view(request, *args, **kwargs):
  
    print(request.user)
    if request.method == 'POST': 
        u_form = UpdateProfileForm(request.POST,instance=request.user)
        p_form = UpdateProfilePic(request.POST,request.FILES,instance= request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'your acount has been updated!')
            return redirect( 'articles:update-view', pk=request.user.pk) 
        else:
            messages.success(request, f'There was an error in your form...')
            u_form = UpdateProfileForm(instance=request.user)
            p_form = UpdateProfilePic(instance= request.user.profile)
            # p_form = UpdateProfilePic(instance= Profile.objects.get(_user__id = request.user.id))
            return redirect( 'articles:update-view', id=request.user.id) 
        #always for submitting data over form use redirect,because if you use render it will popup a window says 'are you sure you want to reload cause the '


    u_form = UpdateProfileForm(instance=request.user)
    p_form = UpdateProfilePic(instance= request.user.profile)
    pic = User.objects.get(username=request.user.username)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'object' : pic.profile.profile_pic,
    }

    return render(request, 'articles/update_profile.html', context)


