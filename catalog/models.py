from __future__ import unicode_literals
from django.urls import reverse
from django.db import models
import uuid
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

class Genere(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a book genere")
    def __str__(self):
        return self.name



class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author",on_delete=models.SET_NULL,null=True)
    summary = models.TextField(max_length=1000,help_text="Enter the brief description of book")
    isbn = models.CharField('ISBN',max_length=13,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genere = models.ManyToManyField('Genere',help_text='Select a genere for book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        __module__= '__name__'

    def display_genere(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ", ".join([genere.name for genere in self.genere.all()[:3]])
    display_genere.short_description = 'Genere'

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, help_text="Unique id for this particular book accross whole library")
    book = models.ForeignKey('Book',on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(blank=True, null=True)
    borrower = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True, null=True)
    
    LOAN_STATUS = (
        ('d', 'Maintenance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),

    )

    status = models.CharField(max_length=1,choices=LOAN_STATUS, default = 'd' ,blank=True, help_text='book availability')

    class Meta:
        permissions = (('can_mark_returned',"Set book as returned"),)
        ordering = ["due_back"]
        

    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)
    
    def __unicode__(self):
        return '%s (%s)' % (self.id,self.book.title)
    
    @property
    def is_overdue(self):
        if date.today() > self.due_back:
            return True
        else:
            return False

class Bookmarks(models.Model):
    """
    Model representing the bookmarks of user
    """
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True, null=True)
    book = models.ForeignKey('Book',on_delete=models.SET_NULL, null=True)
    create_dt = models.DateField("Bookmarked", blank=True, null=True)
    update_dt = models.DateField(blank=True, null=True)
    act_ind = models.CharField(max_length=1,help_text="bookmark valid",blank=True, null=True)

    def __str__(self):
        return '%s (%s) ' % (self.user, self.book.title)


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)


class Language(models.Model):
    """
    Model representing a Language (e.g. English, French, Japanese, etc.)
    """
    name = models.CharField(max_length=200, help_text="Enter a the book's natural language (e.g. English, French, Japanese etc.)")
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name