from django.urls import path

from . import views
urlpatterns = [
    path('home', views.Home, name="Home"),

    path('profile/register/', views.Register, name="register"),
    path('profile/loging/', views.login, name="login"),
    path('profile/logout/', views.logout_page, name="logout"),

    path('profile/create/<int:pk>', views.Create_Profile, name="create-profile"),
    path('profile/edit/<int:pk>/', views.Profile_Edit, name="edit-profile"),

    path('profile/OverView/<int:pk>/',views.Profile_View, name="profile"),

    path('home/post/detail/<int:pk>/', views.Post_Detail, name="post-detail"),
    path('home/post/add/<int:pk>/', views.Add_Post, name="add-post"),
    path('home/post/edit/<int:pk>/', views.Post_Edit, name="post-edit"),
    path('home/post/delete/<int:pk>/', views.Post_Delete, name="post-delete"),

    path('home/post/comment/edit/<int:pk>/', views.Comment_Edit, name="comment-edit"),
    path('home/post/comment/delete/<int:pk>/', views.Comment_Delete, name="comment-delete"),


    #Messages
    path('inbox/', views.List_Threads.as_view(), name='inbox'),

    path('inbox/create-thread', views.Create_Thread.as_view(), name='create-thread'),

    path('inbox/<int:pk>/', views.Thread_View.as_view(), name='thread'),

    path('inbox/<int:pk>/create-message/', views.Create_Message.as_view(), name='create-message'),

    #Follow 
    path('profile/<int:pk>/followers/add/', views.Add_Follow.as_view(), name="add-follow"),
    path('profile/<int:pk>/followers/remove/', views.Remove_follow.as_view(), name="remove-follow"),

    #Like and Dislike
    path('profile/<int:pk>/likes/add/', views.Add_like.as_view(), name="like"),
    path('profile/<int:pk>/likes/remove/', views.Dislike.as_view(), name="dislike"),

    #Comment like and Dislike
    path('profile/comment/<int:pk>/likes/add/', views.Comment_like.as_view(), name="comment-like"),
    path('profile/comment/<int:pk>/likes/remove/', views.Comment_Dislike.as_view(), name="comment-dislike"),

    #Notifications
    path('profile/<int:notification_pk>/notification/post/<post_pk>/', views.Post_Notification.as_view(), name="post-notification"),
    path('profile/<int:notification_pk>/notification/porfile/<profile_pk>/', views.Follow_Noification.as_view(), name="follow-notification"),

    path('profile/<int:notification_pk>/notification/delete/', views.Remove_Notification.as_view(), name="notification-delete"),

]