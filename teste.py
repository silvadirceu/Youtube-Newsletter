from youtube_agent.tasks.celery_app import workflow_all_channels
from youtube_agent import schemas

# channels = {
#     "channel_name": "",
#     "channel_id": "",
#     "videos": [{"id": "V-r-KnmWZT0", "link": "https://www.youtube.com/shorts/V-r-KnmWZT0"}#,
#             #    {"id": "1Mr-Apxihgs", "link": "https://www.youtube.com/shorts/1Mr-Apxihgs"}
#                ]
# }

# channels = [
#   {
#     "id": "UCxXL5491Db9U8Rhfs-2LVFg",
#     "title": "AsimovAcademy",
#     "videos": [
#       {
#         "id": "MtiHwYOZpVw",
#         "link": None
#       }
#     ]
#   }
# ]

# channels = [
#   {
#     "id": "UCxXL5491Db9U8Rhfs-2LVFg",
#     "title": "AsimovAcademy",
#     "videos": [
#       {
#         "id": "MtiHwYOZpVw",
#         "link": None
#       },
#       {
#         "id": "JdbUZ-65zHk",
#         "link": None
#       }
#     ]
#   }
# ]

channels = [
  {
    "id": "UCxXL5491Db9U8Rhfs-2LVFg",
    "title": "AsimovAcademy",
    "videos": [
      {
        "id": "MtiHwYOZpVw",
        "link": None
      },
      {
        "id": "JdbUZ-65zHk",
        "link": None
      }
    ]
  },
  {
    "channel_name": "",
    "channel_id": "",
    "videos": [{"id": "V-r-KnmWZT0", "link": "https://www.youtube.com/shorts/V-r-KnmWZT0"}]
  }
]

# channels = [
#   {
#     "channel_name": "",
#     "channel_id": "",
#     "videos": [{"id": "MtiHwYOZpVw", "link": "https://www.youtube.com/shorts/MtiHwYOZpVw"}]
#   },
#   {
#     "channel_name": "",
#     "channel_id": "",
#     "videos": [{"id": "V-r-KnmWZT0", "link": "https://www.youtube.com/shorts/V-r-KnmWZT0"}]
#   }
# ]

# channels = [
#   {
#     "id": "UCxXL5491Db9U8Rhfs-2LVFg",
#     "title": "AsimovAcademy",
#     "videos": [
#       {
#         "id": "nSKlgF7ilfM",
#         "link": ""
#       },
#       {
#         "id": "SyALGUlELmc",
#         "link": None
#       }
#     ]
#   }
# ]



# workflow_channel_pipeline = workflow_channel(channel)
# print(type(workflow_channel_pipeline))
# workflow_channel_pipeline.apply_async()
# print(workflow_channel_pipeline.get())


worflow_all_channels_pipeline = workflow_all_channels([schemas.ChannelBase(**channel) for channel in channels])
result = worflow_all_channels_pipeline.apply_async()
result = result.get()
print(type(result))
print(result)
# print(type(worflow_all_channels_pipeline))