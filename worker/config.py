broker_url = 'redis://127.0.0.1:6379/0'
broker_pool_limit = 1000 #Broker连接池,默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle','json']

task_serialize = 'pickle'
result_expire = 3600 #任务结果过期时间


result_backend = 'redis://127.0.0.1:6379/1'
result_serializer = 'pickle'
result_cache_max = 10000 #任务最大缓存数量

worker_redirect_stdouts_level = 'INFO'
