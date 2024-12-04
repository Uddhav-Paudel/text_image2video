# src/main.py
from .media_processor import MediaProcessor

def main():
    # Define the base directory
    base_dir = 'Cell_Biology'

    # Define specific subdirectories
    excel_file = f'{base_dir}.xlsx'
    images_dir = f'{base_dir}/images'
    audio_dir = f'{base_dir}/AudioClips'
    imageclips_dir = f'{base_dir}/ImageClips'
    videoclip_dir = f'{base_dir}/ImageClips'
    output_dir = f'{base_dir}/output'

    # Create an instance of MediaProcessor
    processor = MediaProcessor(excel_file, images_dir, audio_dir, imageclips_dir, videoclip_dir, output_dir)

    # Generate final output videos
    processor.generate_final_output()

    print("Process complete!")

if __name__ == "__main__":
    main()
