from flask import Flask, request, jsonify
from utils import get_video_id, get_video_transcript

app = Flask(__name__)

# API endpoint to get the transcript of a YouTube video
@app.route('/api/transcript', methods=['GET'])
def get_transcript():
    youtube_url = request.args.get('url')
    if not youtube_url:
        return jsonify({"error": "Missing YouTube URL parameter"}), 400

    try:
        video_id = get_video_id(youtube_url)
        transcript_text, result_message = get_video_transcript(video_id)
        
        if transcript_text:
            return jsonify({
                "transcript": transcript_text,
                "message": result_message
            }), 200
        else:
            return jsonify({"error": result_message}), 404

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)