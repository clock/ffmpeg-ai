# FFmpeg-AI

FFmpeg-AI is a command-line tool that leverages AI to generate FFmpeg command arguments based on natural language input. This makes it easier to trim, compress, apply color correction, and perform other video editing tasks without manually writing complex FFmpeg commands.

## Features
- Use natural language to generate FFmpeg commands
- Supports trimming, compression, and color correction
- Can be set as an environment variable for quick access

## Installation
```bash
git clone https://github.com/yourusername/ffmpeg-ai.git
cd ffmpeg-ai
pip install -r requirements.txt
```

## Usage
Once installed, you can use FFmpeg-AI anywhere by running:
```bash
ffmpegai input.mp4
```
Then, enter a prompt such as:
```
> Trim this clip from 30 seconds to 45 seconds and compress it
```
FFmpeg-AI will process the request and generate the appropriate FFmpeg command to execute.

## Example
```bash
ffmpegai video.mp4
> Increase brightness and reduce file size
```
The tool will generate and run an equivalent FFmpeg command like:
```bash
ffmpeg -i video.mp4 -vf "eq=brightness=0.1" -b:v 1M output.mp4
```
