from django.contrib import admin

from account_book.models import AccountBook as AccountBookModel
from account_book.models import AccountBookRecord as AccountBookRecord

# Register your models here.
admin.site.register(AccountBookModel)
admin.site.register(AccountBookRecord)
