# drf
## View总结：
### APIView(View):
重写dispatch对request重定义Request，然后initial方法中有各种组件（登录验证，权限、限流、版本管理、渲染、解析等操作）
### GenericAPIView(APIView)：
定义获取数据、序列化类，分页等操作  不用再手动编码对数据进行处理，只需自己定义queryset（以及过滤参数）、serializer_class、pagination_class等一些属性
#### [Create]APIView(mixins.[Create]ModelMixin,GenericAPIView):
定义了执行相应的request方法post，其中调用了CreateModelMixin中数据的具体操作create，接收post请求创建数据（自动验证数据并返回创建的数据）---这样也就不用手动编码各种request方法

### ViewSetMixin(object)
重写了as_view方法，这样路由就不用一个个的写出来  使用 下列写法即可：  
可以自动分发请求到相应的XXX ModelMixin,完成请求任务  
router = DefaultRouter()        
router.register(r'users', UserViewSet, 'user')  
urlpatterns = router.urls  
### ViewSet(ViewSetMixin, views.APIView)：
自己实现各种操作：处理数据，请求方法等  但是不用自己处理路由问题了 一般不用
### GenericViewSet(ViewSetMixin, generics.GenericAPIView);
GenericAPIView的所有功能加上不用自己处理路由问题
### ModelViewSet
继承自下面这些类：  (mixins.CreateModelMixin,
mixins.RetrieveModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
mixins.ListModelMixin,
GenericViewSet):	    
不用自己处理路由、数据、请求  只需自己定义queryset（以及过滤参数）、serializer_class、pagination_class等    
可以完成所有的请求任务
