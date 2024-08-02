# TubeScript API

The TubeScript API provides access to the TubeScript transcript extraction service. It allows you to fetch transcripts from YouTube videos using simple HTTP requests.

## API Endpoint

`GET /api/transcript`

## Base URL

When running locally: `http://127.0.0.1:5000`

## Authentication

The API uses API key authentication. Include your API key as a query parameter in each request.

## Request Parameters

- `url` (required): The YouTube video URL
- `api_key` (required): Your API key for authentication

## Response Format

The API returns JSON responses with the following structure:

### Success Response (200 OK)
```json

{
"transcript": "Full transcript text here...",
"message": "The transcript is saved at: /path/to/file.txt"
}
```

### Error Response (400, 403, 404, or 500)

```json
{
"error": "Error message here"
}

```

