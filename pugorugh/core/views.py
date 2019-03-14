from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import permissions
from rest_framework.generics import (CreateAPIView,
                                     RetrieveUpdateAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,)

from pugorugh.core.serializers import (UserSerializer,
                                       ProfileSerializer,
                                       DogSerializer)
from pugorugh.core.models import Profile, Dog, UserDog


class UserRegisterView(CreateAPIView):
    """Register User"""
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class RetrieveUpdateProfileView(RetrieveUpdateAPIView):
    """Update Profile"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        queryset = self.get_queryset()
        user_pref = get_object_or_404(queryset, user=self.request.user)
        return user_pref


class RetrieveUpdateDog(RetrieveUpdateDestroyAPIView):
    """Update / Delete Dog"""
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class ListCreateDog(ListCreateAPIView):
    """Create Dog"""
    queryset = Dog.objects.all()
    serializer_class = DogSerializer


class NextDogView(RetrieveUpdateAPIView):
    """View for viewing dogs in all sections"""
    serializer_class = DogSerializer

    def detect_user(self):
        user_obj = Profile.objects.get(user=self.request.user)
        return user_obj

    def color_selection(self):
        color = self.detect_user().color.split(',')
        if len(color) == 1:
            queryset = Dog.objects.filter(color=color[0])
        elif len(color) == 0:
            raise Http404
        else:
            queryset = Dog.objects.all()

        return queryset

    def gender_selection(self):
        queryset = self.color_selection()
        gender = self.detect_user().gender.split(',')
        if len(gender) == 1:
            queryset = queryset.filter(gender=gender[0])
        elif len(gender) == 0:
            raise Http404
        else:
            queryset = queryset

        return queryset

    def size_selection(self):
        queryset = self.gender_selection()
        sizes = self.detect_user().size.split(',')

        # Turn list of values into list of Q objects
        queries = [Q(size=size) for size in sizes]
        query = Q()
        for item in queries:
            query |= item
        queryset = queryset.filter(query)

        return queryset

    def age_selection(self):
        queryset = self.size_selection()
        ages = self.detect_user().age.split(',')

        qs_list = []
        for age in ages:
            if age == 'b':
                for dog in queryset:
                    if dog.age <= 24:
                        qs_list.append(queryset.filter(age=dog.age))
            elif age == 'y':
                for dog in queryset:
                    if 25 <= dog.age <= 48:
                        qs_list.append(queryset.filter(age=dog.age))
            elif age == 'a':
                for dog in queryset:
                    if 49 <= dog.age <= 72:
                        qs_list.append(queryset.filter(age=dog.age))
            elif age == 's':
                for dog in queryset:
                    if 73 <= dog.age:
                        qs_list.append(queryset.filter(age=dog.age))

        final_queryset = UserDog.objects.none()
        for qs in qs_list:
            final_queryset |= qs

        return final_queryset

    def get_queryset(self):
        queryset = self.age_selection()

        if self.kwargs.get('dog_filter') == 'liked':
            try:
                queryset = queryset.filter(dogtag__status='liked').\
                    filter(dogtag__user_id=self.request.user.id)
                return queryset
            except:
                raise Http404
        elif self.kwargs.get('dog_filter') == 'disliked':
            try:
                queryset = queryset.filter(dogtag__status='disliked').\
                    filter(dogtag__user_id=self.request.user.id)
                return queryset
            except:
                raise Http404
        else:
            try:
                queryset = queryset.exclude(dogtag__user_id=
                                            self.request.user.id)
                return queryset
            except:
                raise Http404

    def get_object(self):
        dogs = self.get_queryset().filter(id__gt=self.kwargs.get('pk'))
        obj = dogs.first()
        if not obj:
            raise Http404
        return obj


class UpdateUserDogView(RetrieveUpdateAPIView):
    """Updating Dogs in all sections"""
    serializer_class = DogSerializer

    def get_queryset(self):
        return UserDog.objects.filter(user=self.request.user)

    def get_object(self):
        status = self.kwargs.get('status')
        if status == 'liked' or status == 'disliked' or status == 'undecided':
            dogs = Dog.objects.filter(id=self.kwargs.get('pk'))
            obj = dogs.first()
            if not obj:
                raise Http404
            return obj
        else:
            raise Http404

    def put(self, request, *args, **kwargs):
        user = self.request.user
        status = self.kwargs.get('status')
        dog = Dog.objects.get(id=self.kwargs.get('pk'))

        if not self.get_queryset():
            UserDog.objects.create(
                user=user,
                dog=dog,
                status=status
            )
        else:
            if status == 'undecided':
                try:
                    qs = self.get_queryset().get(dog=dog)
                    qs.delete()
                except:
                    raise Http404
            elif status == 'liked' or status == 'disliked':
                try:
                    qs = self.get_queryset().get(dog=dog)
                    qs.status = status
                    qs.save()
                except:
                    UserDog.objects.create(
                        user=user,
                        dog=dog,
                        status=status
                    )
            else:
                raise Http404
        return self.update(request, *args, **kwargs)


"""
class EmployeeCompanyList(generic.ListView):
    model = models.Company
    template_name = 'list.html'
    context_object_name = 'companies'

    def get_context_data(self):
        context = super().get_context_data()
        companies = context.get('companies')
        # <QuerySet [<Company: Company object (1)>, <Company: Company object (2)>]>

        # Ex. companies[0].employees.filter(first_name='Vitor')[0].last_name
        employees = companies[0].employees.filter(first_name='Chris')
        print(employees)
        emps = models.Employee.objects.filter(first_name='Chris')
        print(emps)
        # <QuerySet [<Employee: Employee object (2)>]>

        first_employee = employees.first().first_name
        # Chris

        return context
"""
