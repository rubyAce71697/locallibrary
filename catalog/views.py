from django.shortcuts import render,reverse,get_object_or_404,get_list_or_404
from .models import Book,Author,BookInstance,Genere,Bookmarks
from django.views import generic
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse_lazy
from .forms import UserLoginForm,RenewBookForm                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
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



def get_bookmarks(request):
    """
        returns the bookmarks for the particular user
    """
    print "fetching bookmarks"
    bookmarks = Bookmarks.objects.filter(user__exact=request.user)
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
def renew_book_librarian(request,pk):
    book_inst = get_object_or_404(BookInstance,pk = pk)


    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

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
    print "cehcking if the book is issue by user " + request.user .first_name
    return JsonResponse("success",safe=False)
def ifbookmarked(reqeust):
    print "checking if the book is bbookarked bu iser" + reqeust.user.first_name
    return JsonResponse("success",safe=False)
    
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