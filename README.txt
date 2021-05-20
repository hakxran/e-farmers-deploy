A description of the e-farm project
A test to see if the changes are saved in github

updates on 18.04.2021
the following updates were made:

1) view.py
4 new views were added:
MyTokenObtainPairSerializer
MyTokenObtainPairView
getUserProfile
getUsers

2) urls.py
the follwing pathes were added:
users/login
users/profile
users/

3) serializer.py
2 new serializers were added 
UserSerializer
UserSerializerWithToken

!!!!!!!!!!! IMPORTANT  NOTE !!!!!!!!!!!!!!!!!
1)cd into backend
2)type pip freeze 
3)check if there any JWT related packges are installed
4) if there are uninstall them since they will cause some problems 
5) use pip install djangorestframework-simplejwt to install the jwt package 
