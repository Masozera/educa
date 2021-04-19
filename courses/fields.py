# You need a field that allows you to define an order for objects. An easy way
# to specify an order for objects using existing Django fields is by adding a
# PositiveIntegerField to your models. Using integers, you can easily specify
# the order of objects. You can create a custom order field that inherits from
# PositiveIntegerField and provides additional behavior.
# There are two relevant functionalities that you will build into your order field:

# • Automatically assign an order value when no specific order is provided:
# When saving a new object with no specific order, your field should
# automatically assign the number that comes after the last existing ordered
# object. If there are two objects with order 1 and 2 respectively, when saving
# a third object, you should automatically assign the order 3 to it if no specific
# order has been provided.

#  Order objects with respect to other fields: Course modules will be ordered
# with respect to the course they belong to and module contents with respect
# to the module they belong to.

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):  # This is your custom OrderField. It inherits from the PositiveIntegerField field provided by
    def __init__(self, for_fields=None, *args, **kwargs): # Your OrderField field takes an optional for_fields parameter that allows you to indicate the fields that the order has to be calculated with respect to.
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)
    def pre_save(self, model_instance, add):  # Your field overrides the pre_save() method of the PositiveIntegerField field, which is executed before saving the field into the database
        if getattr(model_instance, self.attname) is None:
        # no current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field)\
                    for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)

        # You check whether a value already exists for this field in the model instance.
        # You use self.attname, which is the attribute name given to the field in the
        # model. If the attribute's value is different to None, you calculate the order you
        # should give it as follows:
        # 1. You build a QuerySet to retrieve all objects for the field's model. You
        # retrieve the model class the field belongs to by accessing self.model.
        # 2. If there are any field names in the for_fields attribute of the field,
        # you filter the QuerySet by the current value of the model fields in
        # for_fields. By doing so, you calculate the order with respect to
        # the given fields.
        # 3. You retrieve the object with the highest order with last_item =
        # qs.latest(self.attname) from the database. If no object is found,
        # you assume this object is the first one and assign the order 0 to it.
        # 4. If an object is found, you add 1 to the highest order found.
        # 5. You assign the calculated order to the field's value in the model
        # instance using setattr() and return it.

        # When you create custom model fields, make them generic. Avoid
        # hardcoding data that depends on a specific model or field. Your
        # field should work in any model.