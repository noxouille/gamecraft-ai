"""PyTube Tool for YouTube video operations."""

import logging
import tempfile
from typing import Any

from langchain_core.tools import tool
from pytube import YouTube

logger = logging.getLogger(__name__)


@tool
def pytube_video_tool(youtube_url: str, action: str) -> dict[str, Any]:
    """
    Uses pytube for YouTube video operations.

    Args:
        youtube_url: YouTube video URL
        action: Action to perform ('metadata', 'transcript', 'download_audio')

    Returns:
        Dict containing video info, captions, or audio file path
    """
    try:
        logger.info(f"Processing YouTube video: {youtube_url} with action: {action}")

        if action == "metadata":
            return _get_video_metadata(youtube_url)
        elif action == "transcript":
            return _get_video_transcript(youtube_url)
        elif action == "download_audio":
            return _download_audio(youtube_url)
        else:
            return {
                "error": f"Unknown action: {action}",
                "supported_actions": ["metadata", "transcript", "download_audio"],
            }

    except Exception as e:
        logger.error(f"PyTube error for {youtube_url}: {str(e)}")
        return {"error": str(e), "url": youtube_url, "action": action}


def _get_video_metadata(youtube_url: str) -> dict[str, Any]:
    """Extract video metadata using pytube."""
    try:
        yt = YouTube(youtube_url)

        metadata = {
            "url": youtube_url,
            "action": "metadata",
            "title": yt.title,
            "author": yt.author,
            "channel_url": yt.channel_url,
            "description": yt.description,
            "length": yt.length,
            "views": yt.views,
            "rating": getattr(yt, "rating", None),
            "publish_date": yt.publish_date.isoformat() if yt.publish_date else None,
            "keywords": yt.keywords,
            "thumbnail_url": yt.thumbnail_url,
            "video_id": yt.video_id,
        }

        # Get available streams info
        streams_info = []
        for stream in yt.streams.filter(progressive=True):
            streams_info.append(
                {
                    "itag": stream.itag,
                    "resolution": stream.resolution,
                    "fps": stream.fps,
                    "video_codec": stream.video_codec,
                    "audio_codec": stream.audio_codec,
                    "filesize": stream.filesize,
                }
            )

        metadata["available_streams"] = streams_info

        # Get audio streams info
        audio_streams = []
        for stream in yt.streams.filter(only_audio=True):
            audio_streams.append(
                {
                    "itag": stream.itag,
                    "abr": stream.abr,
                    "audio_codec": stream.audio_codec,
                    "filesize": stream.filesize,
                }
            )

        metadata["audio_streams"] = audio_streams

        logger.info(f"Metadata extracted for: {yt.title}")
        return metadata

    except Exception as e:
        logger.error(f"Error extracting metadata from {youtube_url}: {str(e)}")
        return {"error": str(e), "url": youtube_url, "action": "metadata"}


def _get_video_transcript(youtube_url: str) -> dict[str, Any]:
    """Get video captions/transcript."""
    try:
        yt = YouTube(youtube_url)

        transcript_data = {
            "url": youtube_url,
            "action": "transcript",
            "title": yt.title,
            "captions_available": False,
            "languages": [],
            "transcript": "",
            "auto_generated": False,
        }

        # Get available caption tracks
        caption_tracks = yt.captions

        if caption_tracks:
            transcript_data["captions_available"] = True
            transcript_data["languages"] = list(caption_tracks.keys())

            # Try to get English captions first
            preferred_languages = ["en", "en-US", "en-GB"]
            selected_caption = None

            for lang in preferred_languages:
                if lang in caption_tracks:
                    selected_caption = caption_tracks[lang]
                    break

            # If no English, get the first available
            if not selected_caption and caption_tracks:
                selected_caption = list(caption_tracks.values())[0]

            if selected_caption:
                try:
                    # Download caption content
                    caption_text = selected_caption.generate_srt_captions()
                    transcript_data["transcript"] = caption_text
                    transcript_data["selected_language"] = selected_caption.code
                    transcript_data["auto_generated"] = (
                        "auto-generated" in selected_caption.name.lower()
                    )

                    # Also provide cleaned text without timestamps
                    cleaned_text = _clean_transcript_text(caption_text)
                    transcript_data["cleaned_transcript"] = cleaned_text

                except Exception as e:
                    logger.warning(f"Error downloading captions: {str(e)}")
                    transcript_data["caption_error"] = str(e)

        logger.info(f"Transcript data extracted for: {yt.title}")
        return transcript_data

    except Exception as e:
        logger.error(f"Error extracting transcript from {youtube_url}: {str(e)}")
        return {"error": str(e), "url": youtube_url, "action": "transcript"}


def _download_audio(youtube_url: str) -> dict[str, Any]:
    """Download audio stream for further processing (e.g., Whisper)."""
    try:
        yt = YouTube(youtube_url)

        # Get the best audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        if not audio_stream:
            return {
                "error": "No audio streams available",
                "url": youtube_url,
                "action": "download_audio",
            }

        # Create temporary directory for download
        temp_dir = tempfile.mkdtemp()

        # Download audio
        output_file = audio_stream.download(output_path=temp_dir, filename=f"{yt.video_id}_audio")

        audio_data = {
            "url": youtube_url,
            "action": "download_audio",
            "title": yt.title,
            "audio_file_path": output_file,
            "filesize": audio_stream.filesize,
            "audio_codec": audio_stream.audio_codec,
            "abr": audio_stream.abr,
            "duration": yt.length,
            "temp_directory": temp_dir,
        }

        logger.info(f"Audio downloaded for: {yt.title} to {output_file}")
        return audio_data

    except Exception as e:
        logger.error(f"Error downloading audio from {youtube_url}: {str(e)}")
        return {"error": str(e), "url": youtube_url, "action": "download_audio"}


def _clean_transcript_text(srt_content: str) -> str:
    """Clean SRT transcript to plain text."""
    try:
        lines = srt_content.split("\n")
        text_lines = []

        for line in lines:
            line = line.strip()
            # Skip sequence numbers
            if line.isdigit():
                continue
            # Skip timestamp lines (contain -->)
            if "-->" in line:
                continue
            # Skip empty lines
            if not line:
                continue
            # Add actual transcript lines
            text_lines.append(line)

        # Join and clean up
        clean_text = " ".join(text_lines)

        # Remove common SRT artifacts
        clean_text = clean_text.replace("&gt;", ">").replace("&lt;", "<")
        clean_text = clean_text.replace("&amp;", "&").replace("&quot;", '"')

        return clean_text

    except Exception as e:
        logger.warning(f"Error cleaning transcript: {str(e)}")
        return srt_content


def cleanup_temp_files(temp_directory: str) -> bool:
    """Helper function to clean up temporary files."""
    try:
        import shutil

        shutil.rmtree(temp_directory)
        logger.info(f"Cleaned up temporary directory: {temp_directory}")
        return True
    except Exception as e:
        logger.warning(f"Error cleaning up {temp_directory}: {str(e)}")
        return False
