from django.contrib.auth.forms import UserCreationForm
from gent.models import Gent



class GentRegisterForm(UserCreationForm):
    class Meta:
        model = Gent
        fields = ('email', 'password1', 'password2')