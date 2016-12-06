from django.views.generic import View
from portal.forms import LoginForm, RegistrationForm, AddSensorForm
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from portal.models import SensorDetail
from django.contrib.auth.decorators import login_required
import random
import json
import logging
import uuid

logger = logging.getLogger(__name__);


class UserLoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    # Display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'login': 'active'})

    # Submit form
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    url = reverse("portal:dashboard")
                    return redirect(url)

        return render(request, self.template_name, {'form': form})


class RegistrationView(View):
    form_class = RegistrationForm
    template_name = 'login.html'

    # Display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form, 'register': 'active'})

   # Submit form
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned (normalized) data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            # Login credentials in the default User table
            user.username = username;
            user.first_name = first_name
            user.set_password(password)
            user.last_name = last_name
            user.email = email
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    url = reverse("portal:dashboard")
                    return redirect(url)

        return render(request, self.template_name, {'form': form})


@login_required()
def dashboard(request):
    all_sensor_data = SensorDetail.objects.filter(sensorOwner=request.user)
    paginator = Paginator(all_sensor_data, 3)
    sensor_page = request.GET.get('page')
    try:
        sensor_data = paginator.page(sensor_page)
    except PageNotAnInteger:
        sensor_data = paginator.page(1)
    except EmptyPage:
        sensor_data = paginator.page(paginator.num_pages)

    info_msg = ''
    if not all_sensor_data:
        info_msg = 'No data to show, please add sensor'
    latlongdata = []
    for sensor in all_sensor_data:
        singledata = []
        singledata.append(str(sensor.location))
        singledata.append(sensor.latitude)
        singledata.append(sensor.longitude)
        latlongdata.append(singledata)
    return render(request, 'dashboard.html', {'sensor_data': sensor_data, 'latlongdata': json.dumps(latlongdata),
                                              'info_msg': info_msg})


class AddSensor(View):
    form_class = AddSensorForm
    template_name = 'add_sensor.html'

    # Display a blank form
    def get(self, request):
        form = self.form_class(None)
        user = request.user
        available_sensors = SensorDetail.objects.filter(sensorOwner=user)
        paginator = Paginator(available_sensors, 5)
        sensor_page = request.GET.get('page')
        try:
            sensor_data = paginator.page(sensor_page)
        except PageNotAnInteger:
            sensor_data = paginator.page(1)
        except EmptyPage:
            sensor_data = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'form': form, 'available_sensors': sensor_data})

    # Submit form
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            sensor = SensorDetail()

            # cleaned (normalized) data
            sensor.sensor_id = self.get_sensor_id()
            sensor.station_name = form.cleaned_data['station_name']
            sensor.station_desc = form.cleaned_data['station_desc']
            sensor.sensor_type = form.cleaned_data['sensor_type']
            sensor.latitude = form.cleaned_data['latitude']
            sensor.longitude = '-' + form.cleaned_data['longitude']
            sensor.location = form.cleaned_data['location']
            sensor.sensorOwner = request.user
            tag = form.cleaned_data['sensor_type']

            form = self.form_class(None)
        available_sensors = SensorDetail.objects.filter(sensorOwner=request.user)

        # ami = getImageID(tag)
        # sensor.ip_address = createServer(ami, tag)
        sensor.save()
        return render(request, self.template_name, {'form': form, 'available_sensors': available_sensors,
                                                    'success_message': 'Sensor added successfully'})

    def get_sensor_id(self):
        sensor_present = True
        while sensor_present:
            try:
                sensor_id = uuid.uuid4().hex
                SensorDetail.objects.get(sensor_id=sensor_id)
            except SensorDetail.DoesNotExist:
                sensor_present = False
        return sensor_id


@login_required()
def delete_sensor(request, pk):
    sensor = SensorDetail.objects.get(id=pk)
    sensor.delete()

    # user_sensor_data = SensorDetail.objects.filter(sensorOwner=request.user)
    # available_sensor_data = SensorDetail.objects.all()
    # success_message = 'Sensor deleted'

    return redirect('portal:dashboard')


def logoutView(request):
    logout(request)
    return redirect('portal:login')
