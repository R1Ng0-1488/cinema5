from django.db import models

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

from user.models import AdvUser

# Create your models here.


class Order(models.Model):
    # phone = models.CharField(max_length=11)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/%Y/%M/%M', blank=True)
    url = models.CharField(max_length=200, blank=True, default=f'http://127.0.0.1:8000/')
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_row_set(self):
        return {ticket.place.row.row for ticket in self.ticket_set.all()}

    def get_total_cost(self):
        return sum(ticket.session.price for ticket in self.ticket_set.all())

    def save(self, *args, **kwargs):
        self.url = f'http://127.0.0.1:8000/orenburg/payment/done/{self.id}'
        qrcode_img = qrcode.make(self.url)
        canvas = Image.new('RGB', (400, 400), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.id}'