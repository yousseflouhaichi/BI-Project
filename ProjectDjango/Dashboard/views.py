from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

import pickle
import joblib
import pandas as pd
import numpy as np
import datetime







#@unauthenticated_user
@login_required(login_url='login')
def registerForm(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')

            if request.user.groups.filter(name='admin').exists():
                group = Group.objects.get(name='admin')

            user.groups.add(group)
            messages.success(request, 'Account was created for ' + username +' !')
            return redirect('register')

    context = {'form': form}
    return render(request, 'register1.html', context)



@unauthenticated_user
def loginForm(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, 'Username or password is incorrect !')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    return render(request, 'dashboard.html')



#@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def predict(request):

    context={}

    if request.method == 'POST':
        print('test0')
        predict = request.POST.get('predict')
        print("************")
        print(predict)
        print("************")
        #paramsmsg=('')
        #if 'railroad' in request.POST.get('name'):
        if predict == 'railroad':
            print('test1')
            catday = request.POST.get('catday')
            tranchh = request.POST.get('tranchh')
            trafic = request.POST.get('trafic')

            # load the model from disk


            data = pd.read_csv('C:\ProjectDjango\csvFiles\Railroad.csv')
            # Removing Columns not Required
            data = data.drop(columns=['ID_Stop'], axis=1)
            data = data.drop(columns=['ID_Tranche_Horr'], axis=1)
            data = data.drop(columns=['Unnamed: 0'], axis=1)
            data = data.drop(columns=['ID_Cat_Day'], axis=1)
            data = data.drop(columns=['percentage'], axis=1)
            jour = pd.get_dummies(data.Nom_Cat_Day).iloc[:, :]
            data = data.drop(columns=['Nom_Cat_Day'], axis=1)
            data = pd.concat([jour, data], axis=1)
            X = data.drop(['fort'], axis=1)
            y = data['fort']
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
            from sklearn.neighbors import KNeighborsClassifier
            knn = KNeighborsClassifier(1)
            knn_model = knn.fit(X_train, y_train)

            a1 = np.array([1, 0, 0, 0, 0])
            if catday=='DIJFP':
                a1 = np.array([1, 0, 0, 0, 0])
            elif catday=='JOHV':
                a1 = np.array([0, 1, 0, 0, 0])
            elif catday=='JOVS':
                a1 = np.array([0, 0, 1, 0, 0])
            elif catday=='SAHV':
                a1 = np.array([0, 0, 0, 1, 0])
            elif catday=='SAVS':
                a1 = np.array([0, 0, 0, 0, 1])

            a2=np.array([int(tranchh[0:2])])
            a3=np.array([int(trafic)])

            a = np.concatenate((a1, a2, a3), axis=0)
            a = a.reshape(1, -1)
            result = knn_model.predict(a).item(0)
            print(result)


            if result == 0:
                print('test')
                message='Low'
                additionalInf='Less than 4.3%'
            else:
                message='High'
                additionalInf='Above 4.3%'

            parammsg='On ' + catday +' day, at '+ tranchh +' with trafic equals to '+ trafic +', percentage of validation (railroad) is predicted '+message+'.'


            context = {'messageRailroad': message,
                    'additionalInfRailroad': additionalInf,'parammsg':parammsg}


        elif predict == 'surface':
            print('test2')

            catday = request.POST.get('catday')
            tranchh = request.POST.get('tranchh')

            # *************************prediction surface***************************

            data = pd.read_csv("C:\ProjectDjango\csvFiles\Surface.csv")
            # Removing Columns not Required
            data = data.drop(columns=['ID_Line'], axis=1)
            data = data.drop(columns=['ID_Tranche_Horr'], axis=1)
            data = data.drop(columns=['Unnamed: 0'], axis=1)
            data = data.drop(columns=['Percentage_Val'], axis=1)
            jour = pd.get_dummies(data.Nom_Cat_Day).iloc[:, :]
            data = data.drop(columns=['Nom_Cat_Day'], axis=1)
            data = pd.concat([jour, data], axis=1)
            X = data.drop(['fort'], axis=1)
            y = data['fort']
            from sklearn.model_selection import train_test_split
            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
            from sklearn.neighbors import KNeighborsClassifier
            knn = KNeighborsClassifier(1)
            knn_model = knn.fit(X_train, y_train)

            s1 = np.array([1, 0, 0, 0, 0])
            if catday == 'DIJFP':
                s1 = np.array([1, 0, 0, 0, 0])
            elif catday == 'JOHV':
                s1 = np.array([0, 1, 0, 0, 0])
            elif catday == 'JOVS':
                s1 = np.array([0, 0, 1, 0, 0])
            elif catday == 'SAHV':
                s1 = np.array([0, 0, 0, 1, 0])
            elif catday == 'SAVS':
                s1 = np.array([0, 0, 0, 0, 1])

            s2 = np.array([int(tranchh[0:2])])

            s = np.concatenate((s1, s2), axis=0)
            s = s.reshape(1, -1)
            result = knn_model.predict(s).item(0)
            print(result)

            if result == 0:
                print('test')
                message = 'low'
                additionalInf = 'less than 6.49%'
            else:
                message = 'high'
                additionalInf = 'above 6.49%'

            parammsg='On ' + catday +' day, at '+ tranchh +', percentage of validation (surface) is predicted '+message+'.'

            context = {'messageSurface': message,
                   'additionalInfSurface': additionalInf,'parammsg':parammsg}

    return render(request, 'predict.html', context)


def railroad(request):
    if request.user.is_staff:
        return render(request, "ferreAnalyste.html")
    else:
        return render(request, "ferreClient.html")


def surface(request):
    if(request.user.is_staff):
        return render(request,"surfaceAnalyste.html")
    else:
        return render(request,"surfaceClient.html")





