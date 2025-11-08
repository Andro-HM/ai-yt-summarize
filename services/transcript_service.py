from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_id: str) -> dict:
    """Get transcript from YouTube"""
    try:
        # Create API instance
        api = YouTubeTranscriptApi()

        # List available transcripts
        transcript_list = api.list(video_id)

        # Find English transcript (or first available)
        transcript = transcript_list.find_transcript(['en'])

        # Fetch the transcript data
        transcript_data = transcript.fetch()

        # Combine all text
        full_text = " ".join([item.text for item in transcript_data])

        # Extract title from first sentences (simple approach)
        title = full_text[:100] + "..." if len(full_text) > 100 else full_text

        return {
            "transcript": full_text,
            "source": "youtube",
            "title": title
        }
    except Exception as e:
        raise Exception(f"Failed to get transcript: {str(e)}")
