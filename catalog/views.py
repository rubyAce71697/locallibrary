from django.shortcuts import render,reverse,get_object_or_404,get_list_or_404
from .models import Book,Author,BookInstance,Genere,Bookmarks
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse_lazy
from .forms import UserLoginForm,RenewBookForm,UserForm
from django.db.transaction import commit        
from django.db.models import Q    
from django.forms.models import model_to_dict    
from django.contrib.auth.models import User

import datetime

# Create your views here.


@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    bookmarks = Bookmarks.objects.filter(user__exact=request.user)

    return render(
        request,
        'catalog/index.html',
        context = {
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            "bookmarks": bookmarks
        }
    )



@login_required
def user_profile(request,username):
    user_obj = User.objects.get(username__iexact=username)

    template_name = "catalog/user_profile.html"
    if request.method=='POST':
        print "request method is port"
        user_form = UserForm(data = request.POST)
        print request.POST.__dict__
        print request.POST['first_name']
        print request.POST['last_name']
        print user_form
        print "user_form.is_valid() : ", user_form.is_valid()
        user_obj.first_name = request.POST['first_name']
        user_obj.last_name = request.POST['last_name']
        user_obj.save()
        
            
    print "print request method is get"
        

    context = {'form':UserForm(initial={},data=model_to_dict(user_obj))}
        
    return render(request,template_name,context)



def get_bookmarks(request):
    """
        returns the bookmarks for the particular user
    """
    print "fetching bookmarks for user ----------------", request.user
    bookmarks = Bookmarks.objects.filter(user__exact=request.user).filter(act_ind__exact='Y')
    bookmarks_res = {}
    print bookmarks
    res =  [{"title": bookmark.book.title,"url": bookmark.book.get_absolute_url()} for bookmark in bookmarks]
    #print JsonResponse(bookmarks,safe=False)
    print res
    return JsonResponse(res, safe=False)

class BooksListView(LoginRequiredMixin,generic.ListView):
    login_url = 'user_login'
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    
    def get_queryset(self):
        return Book.objects.all()
    
    """
    def get_context_data(self,**kwargs):
        context = super(BookListView,self).get_context_data(**kwargs)
        cotext['some_data'] = "THis is just some data"

       
        return context
    """

class BooksDetailView(LoginRequiredMixin,generic.DetailView):
    login_url = 'user_login'
    model = Book
    template_name = 'catalog/book_detail.html'


class AuthorListView(LoginRequiredMixin,generic.ListView):
    login_url = 'user_login'
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'

class AuthorDetailView(LoginRequiredMixin,generic.DetailView):
    login_url = 'user_login'
    model = Author
    template_name = 'catalog/author_detail.html'

class LoanedBooksByUserListView(generic.ListView):
    model = BookInstance
    template_name = 'catalog/book_instance_list_borrowed_user.html'
    paginate_by = 10
    

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact='o').order_by('due_back')

def user_login(request):
    template_name = 'catalog/login.html'
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponseRedirect(reverse('index'))
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              print  "invalid login details " + username + " " + password
              context = {}
              context['form'] = UserLoginForm()
              return render(request,template_name,context)
    
    elif request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    else:
        # the login is a  GET request, so just show the user the login form.
        
        context = {}
        context['form'] = UserLoginForm()
        return render(request,template_name,context)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
        registered = False
    context = dict()
    context['user_form'] = user_form
    context['registered'] = registered
    template_url = 'quiz/register.html'
    return render(request,template_url,context)


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk, user=None):
    print "in book_inst"
    book_inst = get_object_or_404(BookInstance,pk = pk)
    print book_inst

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            print "saving book_inst after renewing the date"
            book_inst.save()
            print "book_inst saved "

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial = {'renewal_date': proposed_renewal_date})
        
        return render(request,'catalog/book_renew_librarian.html',{'form': form, 'bookinst':book_inst})

@permission_required('catalog.can_mark_returned')
def AllLoanedBooksListView(request):
    num_instances_onloan = BookInstance.objects.filter(status__exact='o').count()
    instances_onloan = BookInstance.objects.filter(status__exact='o')

    return render(
        request,
        'catalog/all_borrowed_books.html',
        context = {
            'num_instances_onloan': num_instances_onloan,
            'instances_onloan': instances_onloan
        }
    )
def ifIssued(request):
    print "cehcking if the book is issue by user " + request.user.first_name, request.POST['book']
    book_issued = BookInstance.objects.all().filter(borrower__exact=request.user).filter(status__exact='o').filter(book__title__exact=request.POST['book'])
    res = {}
    res['status'] =  bool(book_issued.count())
    res['due_back'] = book_issued.values('due_back')[0]['due_back'] if bool(book_issued.count()) else None
    return JsonResponse(res)

def ifbookmarked(request):
    print "checking if the book is bbookarked bu iser" + request.user.first_name , request.POST['book']
    bookmark = Bookmarks.objects.filter( Q(user__exact=request.user) & Q(book__title__iexact=request.POST['book']) & Q(act_ind__exact='Y'))
    status = bool(bookmark.count())
    
    return JsonResponse({'status':status})


def bookmarkme(request):
    print request.POST['book']
    bookmark = Bookmarks.objects.filter( Q(user__exact=request.user) & Q(book__title__iexact=request.POST['book']))
    status = ""
    print bookmark.__dict__,bookmark.count()
    if bookmark.count():
        print "----- bookmark already exist for user --------", request.user
        bookmark = Bookmarks.objects.get( Q(user__exact=request.user) & Q(book__title__iexact=request.POST['book']))
        print "--- bookmark.user --------", bookmark.user.__dict__
        print "--- request.user ---------", request.user.__dict__
        print "updating the bookmark"
        print bookmark.act_ind
        if bookmark.act_ind == 'Y':
            bookmark.act_ind='N'
            status="removed"
        else:
            bookmark.act_ind='Y'
            status="bookmarked"

        print bookmark.__dict__
        bookmark.update_dt=datetime.datetime.now()
        bookmark.save()

    else:
        print "------------creating the bookmark-------------------"
        book_obj = Book.objects.get(title__iexact=request.POST['book'])
        bookmark = Bookmarks.objects.create(user=request.user,book=book_obj,create_dt= datetime.datetime.now(),update_dt=datetime.datetime.now(),act_ind='Y')
        print bookmark.__dict__
        bookmark.save()

        status = "bookmarked"

    return JsonResponse({'status':status})


def get_defaulters(request):
    defaulter_instances = BookInstance.objects.filter(Q(borrower__isnull=False ) & Q( due_back__lt=datetime.datetime.now()))
    print "--- number of defaulters --- ", defaulter_instances.count()

    return render( request, "catalog/all_defaulters.html",
    context={
        "defaulters": defaulter_instances
    })

class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"
    initial = {'date_of_death':'12/10/2016'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('author')


def search(request):
    context = {}
    q = request.GET['q']
    context['sucecss'] = 'success'
    #search books
    books = Book.objects.filter(Q( title__istartswith=q))
    result = {}
    result['book'] = []
    result['authors'] = []
    result['bookmarks'] = []
    for i in books:
        item = {}
        item['title'] = i.title
        item['url'] = i.get_absolute_url()
        result['book'].append(item)

    author = Author.objects.filter(Q(first_name__istartswith=q))

    for i in author:
        item = {}
        item['title'] = i.first_name + " " + i.last_name
        item['url'] = i.get_absolute_url()
        result['authors'].append(item)
        

        
    return JsonResponse(result)