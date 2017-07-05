from django.contrib import admin
from django.shortcuts import render
from django.contrib.admin import helpers
from django.conf.urls import url
from .forms import AuthorUpLoadForm,LanguageUpLoadForm,GenereUpLoadForm

import csv

# Register your models here.
from .models import Author,Book,BookInstance,Language,Genere,Bookmarks

#admin.site.register(Author)
#admin.site.register(Genere)
#admin.site.register(BookInstance)
#admin.site.register(Book)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super(LanguageAdmin,self).get_urls()
        add_urls =[
            url(r'^upload/$', self.admin_site.admin_view(self.upload), name='catalog_language_upload')
        ]
        return add_urls + urls

    def upload(self, request):
        context = {
                    'title': 'Upload languages',
                    'app_label': self.model._meta.app_label,
                    'opts': self.model._meta,
                    'has_change_permission': self.has_change_permission(request)
                }
        
            # Handle form request
        if request.method == 'POST':
            form = LanguageUpLoadForm(request.POST, request.FILES)
            if form.is_valid():
                # Do CSV processing and create Author records
                print "----------- CSV uploaded -------------"
                print request.FILES
                uploaded_file = request.FILES['file']
                data = csv.reader(uploaded_file)
                print data
                for row in data:
                    if len(row) >0:
                        print row[0]
                        obj,create = Language.objects.get_or_create(name=row[0])
                        print "The db object is added" + row[0], obj,create


        else:
            form =LanguageUpLoadForm()
        context['form'] = form

        context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                                self.get_prepopulated_fields(request))

        return render(request, 'catalog/language_upload.html', context)




class BookInline(admin.TabularInline):

    model = Book
    fk_name = 'author'
    extra = 0

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name','first_name','date_of_birth','date_of_death')
    fields = [('first_name', 'last_name'),('date_of_birth', 'date_of_death')]
    inlines = [BookInline,]

    def get_urls(self):
        urls = super(AuthorAdmin,self).get_urls()
        add_urls =[
            url( r'^upload/$',self.admin_site.admin_view(self.upload), name='catalog_author_upload')

        ]
        return add_urls + urls

    def add_data_db(self,data):
        for row in data:
            print ",".join(row)
            Author.objects.create(first_name=row[1],last_name=row[0])

    def upload(self, request):
        context = {
                    'title': 'Upload Authors',
                    'app_label': self.model._meta.app_label,
                    'opts': self.model._meta,
                    'has_change_permission': self.has_change_permission(request)
                }
        
            # Handle form request
        if request.method == 'POST':
            form = AuthorUpLoadForm(request.POST, request.FILES)
            if form.is_valid():
                # Do CSV processing and create Author records
                print "----------- CSV uploaded -------------"
                print request.FILES
                uploaded_file = request.FILES['file']
                data = csv.reader(uploaded_file)
                print data
                for row in data:
                    if len(row) >=4:
                        print row
                        Author.objects.get_or_create(first_name=row[1],last_name=row[0])

                #self.add_data_db(data)
                print "The db object is added"


        else:
            form = AuthorUpLoadForm()
        context['form'] = form

        context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                                self.get_prepopulated_fields(request))

        return render(request, 'catalog/author_upload.html', context)



         


admin.site.register(Author,AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    fk_name = 'book'
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):  
    list_display = ('title','author','display_genere')
    
    fieldsets = (
        (None, {
            'fields':(('title','author'),'summary',('isbn','genere', 'language'))
        }),
    )
    inlines = (BookInstanceInline,)

    def get_urls(self):
        urls = super(BookAdmin,self).get_urls()
        add_urls = [
            url(r'^upload/$',self.admin_site.admin_view(self.upload), name='catalog_book_upload')
        ]
        return add_urls + urls

    def upload(self):
        pass
    

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status','due_back')
    list_display = ('book','due_back', 'status','id','borrower')

    fieldsets = (
        (None, {
            'fields':('book','imprint', 'id')
        }),
        ('Availability',{
            'fields':('status','due_back','borrower',)
        })
    )
    pass


@admin.register(Genere)
class GenereAdmin(admin.ModelAdmin):
    
    def get_urls(self):
        urls = super(GenereAdmin,self).get_urls()
        add_url = [
            url(r'^upload/$',self.admin_site.admin_view(self.upload),name='catalog_genere_upload')
        ]
        return add_url + urls

    def upload(self, request):
        context = {
                    'title': 'Upload languages',
                    'app_label': self.model._meta.app_label,
                    'opts': self.model._meta,
                    'has_change_permission': self.has_change_permission(request)
                }
        
            # Handle form request
        if request.method == 'POST':
            form = GenereUpLoadForm(request.POST, request.FILES)
            if form.is_valid():
                # Do CSV processing and create Author records
                print "----------- CSV uploaded -------------"
                print request.FILES
                uploaded_file = request.FILES['file']
                data = csv.reader(uploaded_file)
                print data
                for row in data:
                    if len(row) >0:
                        print row
                        Genere.objects.get_or_create(name=row[0])
                print "The db object is added"


        else:
            form =LanguageUpLoadForm()
        context['form'] = form

        context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                                self.get_prepopulated_fields(request))

        return render(request, 'catalog/genere_upload.html', context)



@admin.register(Bookmarks)
class BookmarksAdmin(admin.ModelAdmin):
    list_filter = ('create_dt','update_dt','act_ind')
    