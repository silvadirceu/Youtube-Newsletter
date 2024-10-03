from celery_app import workflow_channel

channel = {
    "channel_name": "teste",
    "channel_id": "123teste",
    "links": ["a", "b", "c"]
}

worflow_channel_pipeline = workflow_channel(channel)
