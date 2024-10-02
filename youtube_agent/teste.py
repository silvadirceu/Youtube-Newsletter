from celery_app import workflow

links = ["https://www.youtube.com/shorts/1Mr-Apxihgs"]
result = workflow(links)
print(result)