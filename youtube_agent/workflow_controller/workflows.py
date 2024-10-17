from youtube_agent import schemas
from youtube_agent.services.config import settings
from typing import Any, List
from urllib.parse import urlparse
from youtube_agent.business import youtube_manager
from fastapi import HTTPException
from youtube_agent.tasks.celery_app import workflow_all_channels

class BusinessWorkflow():
    async def all_channels(self, workflow: schemas.WorkflowCreate) -> Any:
        """
        """
        channels = []
        for channel in workflow.channels:
            try:
                if self.is_url(channel):
                    video_id = youtube_manager.extract_youtube_id(channel)
                    print("\n\n\n", video_id, "\n\n\n")
                    video = schemas.Video(id=video_id, link=channel)
                    channels.append(schemas.ChannelBase(videos=[video]))
                else:
                    channel_search = youtube_manager.search(schemas.Channels(names=[channel]))
                    
                    if 'detail' in channel_search:
                        raise HTTPException(status_code=400, detail=f"Error searching for channel: {channel}. Detail: {channel_search['detail']}")

                    channel_id = channel_search['ids'][0]
                    time_interval = workflow.time_interval

                    videos = youtube_manager.get_channel_videos(
                        channel_id=channel_id,
                        start_date=time_interval.start_date,
                        end_date=time_interval.end_date
                    )

                    if 'detail' in videos:
                        raise HTTPException(status_code=400, detail=f"Error retrieving videos for channel: {channel}. Detail: {videos['detail']}")
                    
                    video_list = [schemas.Video(id=video['id']) for video in videos]
                    channels.append(schemas.ChannelBase(id=channel_id, title=channel, videos=video_list))

            except HTTPException as http_exc:
                raise http_exc
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        workflow_channels = workflow_all_channels(channels)
        tasks = workflow_channels.apply_async()
        result = tasks.get()
        return result
        # return channels





    def is_url(self, string: str) -> bool:
        """
        Verifies if a string it's a valid URL.
        """
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False


workflow = BusinessWorkflow()