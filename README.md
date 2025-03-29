# Contribution Chart Pixelart

This is a tool that allows you to create artificial commit history to paint pictures on your GitHub contribution chart. The script reads an image file, converts it to grayscale, and generates commits with appropriate timestamps to recreate the image on your GitHub contribution graph.

## How it Works

1. Reads an image file and converts it to grayscale. Must be 7px height and up to 49px width (I used https://www.pixilart.com/draw to create these images);
2. Processes each pixel's intensity value to determine how many commits to create for that day;
3. Creates empty commits with specific dates to form the image pattern;
4. Supports "dry run" mode to preview the output in console before making actual commits.

It creates empty commits using `--allow-empty` flag on a specific dates leveraging environment variables `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` which it will set during execution (it will actually make a copy of current env and just add these to a copy).

## Usage

```
python main.py --image_path PATH_TO_IMAGE --repo_path PATH_TO_TARGET_REPOSITORY --year YEAR --dry_run true|false
```

### Arguments:
- `--image_path`: Path to the input image;
- `--repo_path`: Path to the target Git repository, must be initialised prior this script run;
- `--year`: Year to place the commits (between 2010 and current year);
- `--dry_run`: Preview the pattern without making commits (default: True).

## Requirements

- Python 3
- Pillow library
- Git configured with user.name and user.email
