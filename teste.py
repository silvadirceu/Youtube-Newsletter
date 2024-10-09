from youtube_agent.celery_app import workflow_channel, workflow_all_channels

channels = [{
    "channel_name": "teste",
    "channel_id": "123teste",
    "links": ["a", "b", "c"]
},
{
    "channel_name": "teste2",
    "channel_id": "123teste2",
    "links": ["a", "b", "c"]
},
{
    "channel_name": "teste3",
    "channel_id": "123teste3",
    "links": ["a", "b", "c"]
}
]

channel = {
    "channel_name": "teste",
    "channel_id": "123teste",
    "videos": [{"id": "V-r-KnmWZT0", "link": "https://www.youtube.com/shorts/V-r-KnmWZT0"},
               {"id": "1Mr-Apxihgs", "link": "https://www.youtube.com/shorts/1Mr-Apxihgs"}]
}

workflow_channel_pipeline = workflow_channel(channel)
print(type(workflow_channel_pipeline))
workflow_channel_pipeline.apply_async()
# print(workflow_channel_pipeline.get())


# worflow_all_channels_pipeline = workflow_all_channels(channels)
# worflow_all_channels_pipeline.apply_async()
# print(worflow_all_channels_pipeline)
# print(type(worflow_all_channels_pipeline))