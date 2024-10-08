"""Handles the pathing for the audio files and output files."""

import os
from fastapi import HTTPException
from ..settings import GeneralSettings

settings = GeneralSettings()


def audio_path_builder(details):
    """Return the path to the audio file."""
    ext = os.path.basename(details["audio_filename"]).split(".")[-1]
    audio_path = ""
    if details["is_task"]:
        audio_path = os.path.join(
            settings.ROOT,
            settings.AUDIO_TASKS_DIRECTORY,
            details["work_id"],
            details["track_id"] + "." + ext,
        )
    else:
        audio_path = os.path.join(
            settings.ROOT,
            settings.AUDIO_UNIVERSE_DIRECTORY,
            details["work_id"],
            details["track_id"] + "." + ext,
        )

    if os.path.exists(audio_path):
        return audio_path
    else:
        return HTTPException(
            status_code=404,
            detail=f"Audio file could not be found in database for path: {audio_path}.",
        )


def output_path(details):
    """Return the path to the output file."""
    file_output_path = ""
    if details["is_task"]:
        file_output_path = os.path.join(
            settings.ROOT,
            settings.FEATURES_TASKS_DIRECTORY,
            details["work_id"],
            details["track_id"] + "." + settings.FILE_EXT,
        )
        if not os.path.exists(
            os.path.join(
                settings.ROOT, settings.FEATURES_TASKS_DIRECTORY, details["work_id"]
            )
        ):
            os.makedirs(
                os.path.join(
                    settings.ROOT, settings.FEATURES_TASKS_DIRECTORY, details["work_id"]
                )
            )
    else:
        file_output_path = os.path.join(
            settings.ROOT,
            settings.FEATURES_UNIVERSE_DIRECTORY,
            details["work_id"],
            details["track_id"] + "." + settings.FILE_EXT,
        )
        if not os.path.exists(
            os.path.join(
                settings.ROOT, settings.FEATURES_UNIVERSE_DIRECTORY, details["work_id"]
            )
        ):
            os.makedirs(
                os.path.join(
                    settings.ROOT,
                    settings.FEATURES_UNIVERSE_DIRECTORY,
                    details["work_id"],
                )
            )

    return file_output_path
