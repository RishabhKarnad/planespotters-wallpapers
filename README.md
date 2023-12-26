# Planespotters.net wallpaper scraper

Simple script to fetch latest and top images of the day from https://planespotters.net. Saves images in the following folders:

- Images from [Latest Additions](https://www.planespotters.net/photos/latest) are saved to `./latest` (16 images by default)
- Images from [User Favourites of the Day](https://www.planespotters.net/photos/favorited/added/day) are saved to `./top_daily` (100 images by default)

Set your OS to apply backgrounds / wallpapers from these folders.

## Running the script

Install dependencies

```sh
pip install -r requirements.txt
```

Run the script

```sh
python main.py
```

## Running the script as a systemd service

Use the `example.service` file as a template for a systemd service.
