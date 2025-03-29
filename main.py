import os
import subprocess
import sys
import argparse
import datetime
from PIL import Image


def check_git_config():
    name_result = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True)
    email_result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)

    if name_result.returncode != 0 or not name_result.stdout.strip():
        print("Error: Git user.name is not set. Please configure it using 'git config --global user.name \"Your Name\"'")
        sys.exit(1)

    if email_result.returncode != 0 or not email_result.stdout.strip():
        print("Error: Git user.email is not set. Please configure it using 'git config --global user.email \"your.email@example.com\"'")
        sys.exit(1)


def commit_with_date(date_str):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    subprocess.run(["git", "commit", "--allow-empty", "-m", f"Empty commit on {date_str}"], env=env, check=True)


def fill_commit_history(img, repo_path, year):
    os.chdir(repo_path)

    check_git_config()

    date = get_first_sunday(year)

    width, height = img.size
    for x in range(width):
        for y in range(height):
            intensity = img.getpixel((x, y))
            intensity_level = round((255 - intensity) * 4 / 255)
            print(f"(x,y)=({x},{y}); date={date}; intensity_level={intensity_level}")
            for _ in range(intensity_level):
                commit_with_date(date.isoformat())
            date += datetime.timedelta(days=1)


def get_first_sunday(year): # because github contribution chart starts from Sunday
    date = datetime.datetime(year, 1, 1, 1, 1, 1)
    while date.weekday() != 6:
        date += datetime.timedelta(days=1)

    return date


def convert_image_to_grayscale_jpg(image_path):
    with Image.open(image_path) as img:
        if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
            background = Image.new("RGBA", img.size, (255, 255, 255, 255))
            img = Image.alpha_composite(background, img.convert("RGBA"))
        rgb_im = img.convert("L")
    return rgb_im


def generate_ascii_grid(img):
    mapping = " ░▒▓█"
    # mapping = "01234"
    width, height = img.size

    grid_lines = []
    for y in range(height):
        row = ""
        for x in range(width):
            intensity = img.getpixel((x, y))
            intensity_level = round((255 - intensity) * 4 / 255)
            row += mapping[intensity_level]
        grid_lines.append(row)

    return "\n".join(grid_lines)


def validate_image(img):
    width, height = img.size
    if height != 7 or not (1 <= width <= 49):
        print("Error: Image must have a height of 7px and a width between 1 and 49 pixels.")
        sys.exit(1)


def valid_year(value):
    year = int(value)
    current_year = datetime.datetime.now().year
    if year < 2010 or year > current_year:
        raise argparse.ArgumentTypeError(f"Year must be between 2010 and {current_year}")
    return year


def create_argument_parser():
    parser = argparse.ArgumentParser(description="Create commit history that matches the shape of an input image")
    parser.add_argument("--image_path", help="Path to the input image")
    parser.add_argument("--repo_path", help="Path to the target repository")
    parser.add_argument(
        "--dry_run", 
        type=lambda x: x.lower() == "true", 
        default=True,
        help="Flag to perform a dry run. Use True or False. Default is True"
    )
    parser.add_argument(
        "--year", 
        type=valid_year, 
        required=True,
        help="Year between 2010 and current year"
    )
    return parser


if __name__ == '__main__':
    parser = create_argument_parser()
    args = parser.parse_args()

    image_path = args.image_path
    repo_path = args.repo_path
    dry_run = args.dry_run
    year = args.year

    jpg_image = convert_image_to_grayscale_jpg(image_path)

    validate_image(jpg_image)

    if dry_run:
        ascii_grid = generate_ascii_grid(jpg_image)
        print("Shape of your commit history:")
        print(ascii_grid)
    else:
        fill_commit_history(jpg_image, repo_path, year)
        print("Commit history filled successfully")
