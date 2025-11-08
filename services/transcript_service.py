from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_id: str, preferred_language: str = 'en') -> dict:
    """Get transcript from YouTube with fallback to any available language"""
    try:
        # Create API instance
        api = YouTubeTranscriptApi()

        # List available transcripts
        transcript_list = api.list(video_id)

        # Try to find transcript in order of preference
        transcript = None
        detected_language = preferred_language

        try:
            # Try preferred language first
            transcript = transcript_list.find_transcript([preferred_language])
        except:
            # If preferred language not available, try common languages
            common_languages = ['en', 'hi', 'es', 'fr', 'de', 'pt', 'ja', 'ko', 'zh-CN', 'zh-TW']
            for lang in common_languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    detected_language = lang
                    break
                except:
                    continue

            # If still no transcript, get the first available one
            if not transcript:
                available = transcript_list._manually_created_transcripts or transcript_list._generated_transcripts
                if available:
                    first_transcript = list(available.values())[0]
                    transcript = first_transcript
                    detected_language = first_transcript.language_code

        if not transcript:
            raise Exception("No transcripts available for this video")

        # Fetch the transcript data
        transcript_data = transcript.fetch()

        # Combine all text
        full_text = " ".join([item.text for item in transcript_data])

        # Extract title from first sentences (simple approach)
        title = full_text[:100] + "..." if len(full_text) > 100 else full_text

        return {
            "transcript": full_text,
            "source": "youtube",
            "title": title,
            "language": detected_language
        }
    except Exception as e:
        raise Exception(f"Failed to get transcript: {str(e)}")
