from flask import Flask, render_template, abort
from utils.markdown_parser import MarkdownParser
from utils.yaml_loader import YAMLLoader
import os
import glob
from datetime import datetime
from PIL import Image

# Try to import pillow_heif for HEIC support
try:
    import pillow_heif

    # Register HEIF opener with Pillow
    pillow_heif.register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    print("Warning: pillow_heif not installed. HEIC files will be skipped.")
    HEIC_SUPPORTED = False

app = Flask(__name__)

# Initialize parsers
markdown_parser = MarkdownParser()
yaml_loader = YAMLLoader()


def convert_heic_to_jpg(heic_path, output_dir="static/images/gallery/converted"):
    """Convert HEIC file to JPG format"""
    if not HEIC_SUPPORTED:
        return None

    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get filename without extension
        base_name = os.path.splitext(os.path.basename(heic_path))[0]
        jpg_path = os.path.join(output_dir, f"{base_name}.jpg")

        # Check if converted file already exists
        if os.path.exists(jpg_path):
            return jpg_path.replace("static/", "")

        # Convert HEIC to JPG
        with Image.open(heic_path) as img:
            # Convert to RGB if necessary
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Save as JPG with high quality
            img.save(jpg_path, "JPEG", quality=90, optimize=True)
            print(f"Converted {heic_path} to {jpg_path}")

        return jpg_path.replace("static/", "")

    except Exception as e:
        print(f"Error converting {heic_path}: {e}")
        return None


def get_image_path(image_name, image_type="blog"):
    """
    Get the correct path for an image, checking multiple formats including WebP
    Args:
        image_name: filename from frontmatter (e.g., "image.jpg" or "image.webp")
        image_type: "blog" or "event"
    Returns:
        The actual filename that exists, or the original if not found
    """
    if not image_name:
        return None

    base_path = f"static/images/{image_type}"

    # Create directory if it doesn't exist
    os.makedirs(base_path, exist_ok=True)

    # If the image_name already has an extension, check if it exists
    if "." in image_name:
        full_path = os.path.join(base_path, image_name)
        if os.path.exists(full_path):
            return image_name

    # Get base name without extension
    base_name = os.path.splitext(image_name)[0]

    # Supported image formats (prioritize WebP for better compression)
    supported_formats = [".webp", ".jpg", ".jpeg", ".png", ".gif"]

    # Check each format
    for ext in supported_formats:
        test_filename = f"{base_name}{ext}"
        full_path = os.path.join(base_path, test_filename)
        if os.path.exists(full_path):
            return test_filename

    # If no file found, return original name (will show as 404 but won't break the site)
    return image_name


def get_gallery_images():
    """Get all images from gallery folder with HEIC support"""
    gallery_path = "static/images/gallery"
    image_extensions = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.gif",
        "*.webp",
        "*.HEIC",
        "*.heic",
    ]
    images = []

    # Create gallery directory if it doesn't exist
    os.makedirs(gallery_path, exist_ok=True)

    for ext in image_extensions:
        pattern = os.path.join(gallery_path, ext)
        found_images = glob.glob(pattern, recursive=False)

        for img in found_images:
            # Skip files in subdirectories like 'converted'
            if "/converted/" in img or "\\converted\\" in img:
                continue

            filename = os.path.basename(img)
            file_ext = os.path.splitext(filename)[1].lower()

            # Handle HEIC files
            if file_ext in [".heic"]:
                if not HEIC_SUPPORTED:
                    print(f"Skipping {filename} - HEIC support not available")
                    continue

                # Convert HEIC to JPG
                converted_path = convert_heic_to_jpg(img)
                if converted_path:
                    # Use converted JPG file
                    images.append(
                        {
                            "path": converted_path,
                            "filename": os.path.basename(converted_path),
                            "alt": filename.split(".")[0]
                            .replace("-", " ")
                            .replace("_", " ")
                            .title(),
                            "original_format": "HEIC",
                        }
                    )
                    print(f"Added HEIC file: {filename} -> {converted_path}")
                else:
                    # Fallback: skip this file if conversion failed
                    print(f"Skipping {filename} - conversion failed")
                    continue
            else:
                # Handle regular image files
                relative_path = img.replace("static/", "")
                images.append(
                    {
                        "path": relative_path,
                        "filename": filename,
                        "alt": filename.split(".")[0]
                        .replace("-", " ")
                        .replace("_", " ")
                        .title(),
                        "original_format": file_ext.upper().replace(".", ""),
                    }
                )

    # Sort by filename
    images.sort(key=lambda x: x["filename"])

    print(f"Gallery loaded: {len(images)} images total")
    if images:
        for img in images:
            print(f"  - {img['filename']} ({img['original_format']})")

    return images


@app.route("/")
def index():
    """Homepage with modern tech infrastructure design"""
    # Get latest blog posts and events for homepage
    latest_blogs = markdown_parser.get_latest_posts("content/blog", limit=3)
    upcoming_events = markdown_parser.get_upcoming_events("content/event", limit=3)
    latest_events = markdown_parser.get_latest_posts("content/event", limit=3)

    # Load sponsor data
    sponsor_data = yaml_loader.load_yaml("content/sponsor.yaml")
    sponsors = sponsor_data.get("sponsors", []) if sponsor_data else []
    # Filter only active sponsors
    active_sponsors = [sponsor for sponsor in sponsors if sponsor.get("active", True)]

    # Get gallery images
    gallery_images = get_gallery_images()

    return render_template(
        "index.html",
        latest_blogs=latest_blogs,
        upcoming_events=upcoming_events,
        latest_events=latest_events,
        sponsors=active_sponsors,
        gallery_images=gallery_images,
        current_page="index",
    )


@app.route("/blog")
def blog_index():
    """Blog listing page"""
    blog_posts = markdown_parser.get_all_posts("content/blog")
    return render_template(
        "blog/index.html", posts=blog_posts, current_page="blog_index"
    )


@app.route("/blog/<slug>")
def blog_post(slug):
    """Individual blog post"""
    post = markdown_parser.get_post_by_slug("content/blog", slug)
    if not post:
        abort(404)
    return render_template("blog/post.html", post=post, current_page="blog_post")


@app.route("/event")
def event_index():
    """Event listing page"""
    events = markdown_parser.get_all_posts("content/event")
    return render_template(
        "event/index.html", events=events, current_page="event_index"
    )


@app.route("/event/<slug>")
def event_detail(slug):
    """Individual event detail"""
    event = markdown_parser.get_post_by_slug("content/event", slug)
    if not event:
        abort(404)
    return render_template("event/event.html", event=event, current_page="event_detail")


@app.route("/organizer")
def organizer():
    """Organizer profiles page"""
    organizer_data = yaml_loader.load_yaml("content/organizer.yaml")
    return render_template(
        "organizer.html", data=organizer_data, current_page="organizer"
    )


@app.route("/about")
def about():
    """About page"""
    about_data = yaml_loader.load_yaml("content/about.yaml")
    return render_template("about.html", data=about_data, current_page="about")


@app.route("/gallery")
def gallery():
    """Gallery page"""
    gallery_images = get_gallery_images()
    return render_template(
        "gallery.html", gallery_images=gallery_images, current_page="gallery"
    )



@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


# Template filters
@app.template_filter("date")
def date_filter(value, format="%Y"):
    """Custom date filter for Jinja2"""
    if value == "now":
        return datetime.now().strftime(format)
    elif isinstance(value, str):
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d")
            return date_obj.strftime(format)
        except ValueError:
            return value
    return value


@app.template_filter("date_format")
def date_format(date_string, format="%B %d, %Y"):
    """Format date string"""
    if isinstance(date_string, str):
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%d")
            return date_obj.strftime(format)
        except ValueError:
            return date_string
    return date_string


@app.template_filter("excerpt")
def excerpt_filter(text, length=150):
    """Create excerpt from text"""
    if len(text) <= length:
        return text
    return text[:length].rsplit(" ", 1)[0] + "..."


@app.template_filter("get_image")
def get_image_filter(image_name, image_type="blog"):
    """Template filter to get the correct image path with WebP support"""
    return get_image_path(image_name, image_type)


if __name__ == "__main__":
    # Create content directories if they don't exist
    os.makedirs("content/blog", exist_ok=True)
    os.makedirs("content/event", exist_ok=True)
    os.makedirs("static/organizer", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)
    os.makedirs("static/images/gallery", exist_ok=True)

    app.run(debug=True, host="0.0.0.0", port=3008)
