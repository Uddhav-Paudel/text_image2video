# src/media_processor.py
import os
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, VideoFileClip
from .utils import create_directories, get_image_path


class MediaProcessor:
    def __init__(self, excel_file, images_dir, audio_dir, imageclips_dir, videoclip_dir, output_dir):
        # Initialize with paths for folders and Excel file
        self.excel_file = excel_file
        self.images_dir = images_dir
        self.audio_dir = audio_dir
        self.imageclips_dir = imageclips_dir
        self.videoclips_dir = videoclip_dir
        self.output_dir = output_dir

        # Create necessary directories
        create_directories([self.audio_dir, self.imageclips_dir, self.videoclips_dir, self.output_dir])

    def read_excel(self):
        """Read the Excel file containing the data."""
        import pandas as pd
        return pd.read_excel(self.excel_file)

    def create_audio_clip(self, sentence, chapter_name, sentence_num):
        """Create and save an audio clip for a given sentence."""
        audio_folder = os.path.join(self.audio_dir, chapter_name)
        os.makedirs(audio_folder, exist_ok=True)
        audio_path = os.path.join(audio_folder, f'{sentence_num}.mp3')

        tts = gTTS(text=sentence, lang='en')
        tts.save(audio_path)
        return audio_path

    def create_image_clip(self, sentence_num, chapter_name, audio_clip_path):
        """Create and save an image clip for a given sentence."""
        image_folder = os.path.join(self.images_dir, chapter_name)
        os.makedirs(os.path.join(self.imageclips_dir, chapter_name), exist_ok=True)

        audio_clip = AudioFileClip(audio_clip_path)
        image_path = get_image_path(image_folder, sentence_num)
        image_clip = ImageClip(image_path, duration=audio_clip.duration).with_audio(audio_clip)  # Set duration per image
        image_clip_path = os.path.join(self.imageclips_dir, chapter_name, f'{sentence_num}.mp4')
        image_clip.write_videofile(image_clip_path, fps=24)
        return image_clip_path

    def create_video_clip(self, image_clip_path, audio_clip_path):
        """Combine image and audio into a video clip."""
        image_clip = ImageClip(image_clip_path)
        audio_clip = AudioFileClip(audio_clip_path)
        video_clip = image_clip.with_audio(audio_clip)
        return video_clip

    def process_chapter(self, chapter_data):
        """Process all sentences in a given chapter."""
        chapter_name = chapter_data['Chapter']
        moral_sentences = chapter_data['Moral'].split('.')  # Assuming sentences are separated by periods
        
        video_clips = []
        for sentence_num, sentence in enumerate(moral_sentences, start=1):
            if sentence.strip():
                # Generate audio and image clips for the sentence
                audio_clip_path = self.create_audio_clip(sentence.strip(), chapter_name, sentence_num)
                image_clip_path = self.create_image_clip(sentence_num, chapter_name, audio_clip_path)

                # Create a video clip combining audio and image
                video_clip = VideoFileClip(image_clip_path)
                video_clips.append(video_clip)

        # Combine all video clips for the chapter into a final video
        return concatenate_videoclips(video_clips)

    def save_final_video(self, final_video, chapter_name):
        """Save the final video for the chapter."""
        video_folder = os.path.join(self.videoclips_dir, chapter_name)
        os.makedirs(video_folder, exist_ok=True)
        video_output_path = os.path.join(video_folder, f'{chapter_name}.mp4')
        final_video.write_videofile(video_output_path, fps=24)
        #final_video.write_videofile(video_output_path, codec="libx264", audio_codec="aac", fps=24, threads=1)

    def generate_final_output(self):
        """Generate the final output videos for all chapters."""
        df = self.read_excel()

        for index, row in df.iterrows():
            if row['Process'] == 1:
                final_video = self.process_chapter(row)
                #self.save_final_video(final_video, row['Chapter'])

        # Combine all chapter videos into a final output folder
        self._combine_chapter_videos()

    def _combine_chapter_videos(self):
        """Combine individual chapter videos into the final output folder."""
        from moviepy import VideoFileClip

        for chapter_folder in os.listdir(self.videoclips_dir):
            chapter_video_folder = os.path.join(self.videoclips_dir, chapter_folder)
            if os.path.isdir(chapter_video_folder):
                chapter_video_files = [os.path.join(chapter_video_folder, f) for f in os.listdir(chapter_video_folder) if f.endswith('.mp4')]
                
                final_chapter_video = concatenate_videoclips([VideoFileClip(f) for f in chapter_video_files])
                final_chapter_video_output = os.path.join(self.output_dir, f'{chapter_folder}.mp4')
                final_chapter_video.write_videofile(final_chapter_video_output, fps=24)
