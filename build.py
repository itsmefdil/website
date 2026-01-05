#!/usr/bin/env python3
"""
Static Site Generator for DevOps Jogja Website
Converts Flask app to static HTML files for GitHub Pages hosting
"""

import os
import shutil
import json
from pathlib import Path
from flask import Flask, render_template
from utils.markdown_parser import MarkdownParser
from utils.yaml_loader import YAMLLoader
from datetime import datetime
import glob
from urllib.parse import quote
from PIL import Image

# Try to import pillow_heif for HEIC support
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    print("Warning: pillow_heif not installed. HEIC files will be skipped.")
    HEIC_SUPPORTED = False


class StaticSiteBuilder:
    def __init__(self, output_dir="dist"):
        self.output_dir = Path(output_dir)
        self.app = Flask(__name__)
        
        # Configure Flask for URL generation
        self.app.config['SERVER_NAME'] = 'devopsjogja.com'  # Update with your domain
        self.app.config['APPLICATION_ROOT'] = '/'
        self.app.config['PREFERRED_URL_SCHEME'] = 'https'
        
        self.markdown_parser = MarkdownParser()
        self.yaml_loader = YAMLLoader()
        
        # Setup template filters
        self.setup_template_filters()
        
    def setup_template_filters(self):
        """Setup Flask template filters and context processors"""
        
        # Custom URL function for static site generation
        def static_url_for(endpoint, **values):
            """Custom url_for function for static site generation"""
            if endpoint == 'static':
                filename = values.get('filename', '')
                return f'/static/{filename}'
            elif endpoint == 'index':
                return '/'
            elif endpoint == 'blog_index':
                return '/blog/'
            elif endpoint == 'event_index':
                return '/event/'
            elif endpoint == 'about':
                return '/about/'
            elif endpoint == 'organizer':
                return '/organizer/'
            elif endpoint == 'blog_post':
                slug = values.get('slug', '')
                return f'/blog/{slug}/'
            elif endpoint == 'event_detail':
                slug = values.get('slug', '')
                return f'/event/{slug}/'
            else:
                # Fallback for unknown endpoints
                return f'/{endpoint}/'
        
        # Add url_for to Jinja2 globals
        self.app.jinja_env.globals['url_for'] = static_url_for
        
        # Add base URL for sharing
        base_url = f"{self.app.config['PREFERRED_URL_SCHEME']}://{self.app.config['SERVER_NAME']}"
        self.app.jinja_env.globals['base_url'] = base_url
        
        @self.app.template_filter("date")
        def date_filter(value, format="%Y"):
            if value == "now":
                return datetime.now().strftime(format)
            elif isinstance(value, str):
                try:
                    date_obj = datetime.strptime(value, "%Y-%m-%d")
                    return date_obj.strftime(format)
                except ValueError:
                    return value
            return value

        @self.app.template_filter("date_format")
        def date_format(date_string, format="%B %d, %Y"):
            if isinstance(date_string, str):
                try:
                    date_obj = datetime.strptime(date_string, "%Y-%m-%d")
                    return date_obj.strftime(format)
                except ValueError:
                    return date_string
            return date_string

        @self.app.template_filter("excerpt")
        def excerpt_filter(text, length=150):
            if len(text) <= length:
                return text
            return text[:length].rsplit(" ", 1)[0] + "..."

        @self.app.template_filter("get_image")
        def get_image_filter(image_name, image_type="blog"):
            return self.get_image_path(image_name, image_type)

    def get_image_path(self, image_name, image_type="blog"):
        """Get the correct path for an image"""
        if not image_name:
            return None

        base_path = f"static/images/{image_type}"
        
        if "." in image_name:
            full_path = os.path.join(base_path, image_name)
            if os.path.exists(full_path):
                return image_name

        base_name = os.path.splitext(image_name)[0]
        supported_formats = [".webp", ".jpg", ".jpeg", ".png", ".gif"]

        for ext in supported_formats:
            test_filename = f"{base_name}{ext}"
            full_path = os.path.join(base_path, test_filename)
            if os.path.exists(full_path):
                return test_filename

        return image_name

    def convert_heic_to_jpg(self, heic_path, output_dir="static/images/gallery/converted"):
        """Convert HEIC file to JPG format"""
        if not HEIC_SUPPORTED:
            return None

        try:
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(heic_path))[0]
            jpg_path = os.path.join(output_dir, f"{base_name}.jpg")

            if os.path.exists(jpg_path):
                return jpg_path.replace("static/", "")

            with Image.open(heic_path) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(jpg_path, "JPEG", quality=90, optimize=True)
                print(f"Converted {heic_path} to {jpg_path}")

            return jpg_path.replace("static/", "")

        except Exception as e:
            print(f"Error converting {heic_path}: {e}")
            return None

    def get_gallery_images(self):
        """Get all images from gallery folder with HEIC support"""
        gallery_path = "static/images/gallery"
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.webp", "*.HEIC", "*.heic"]
        images = []

        os.makedirs(gallery_path, exist_ok=True)

        for ext in image_extensions:
            pattern = os.path.join(gallery_path, ext)
            found_images = glob.glob(pattern, recursive=False)

            for img in found_images:
                if "/converted/" in img or "\\converted\\" in img:
                    continue

                filename = os.path.basename(img)
                file_ext = os.path.splitext(filename)[1].lower()

                if file_ext in [".heic"]:
                    if not HEIC_SUPPORTED:
                        print(f"Skipping {filename} - HEIC support not available")
                        continue

                    converted_path = self.convert_heic_to_jpg(img)
                    if converted_path:
                        images.append({
                            "path": converted_path,
                            "filename": os.path.basename(converted_path),
                            "alt": filename.split(".")[0].replace("-", " ").replace("_", " ").title(),
                            "original_format": "HEIC",
                        })
                else:
                    relative_path = img.replace("static/", "")
                    images.append({
                        "path": relative_path,
                        "filename": filename,
                        "alt": filename.split(".")[0].replace("-", " ").replace("_", " ").title(),
                        "original_format": file_ext.upper().replace(".", ""),
                    })

        images.sort(key=lambda x: x["filename"])
        print(f"Gallery loaded: {len(images)} images total")
        return images

    def clean_output_dir(self):
        """Clean the output directory"""
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Cleaned output directory: {self.output_dir}")

    def copy_static_files(self):
        """Copy all static files to output directory"""
        static_src = Path("static")
        static_dest = self.output_dir / "static"
        
        if static_src.exists():
            shutil.copytree(static_src, static_dest, dirs_exist_ok=True)
            print(f"Copied static files to {static_dest}")

    def save_page(self, html_content, path):
        """Save HTML content to file"""
        file_path = self.output_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Generated: {file_path}")

    def build_homepage(self):
        """Build homepage"""
        with self.app.app_context():
            with self.app.test_request_context():
                latest_blogs = self.markdown_parser.get_latest_posts("content/blog", limit=3)
                upcoming_events = self.markdown_parser.get_upcoming_events("content/event", limit=3)
                latest_events = self.markdown_parser.get_latest_posts("content/event", limit=3)
                
                sponsor_data = self.yaml_loader.load_yaml("content/sponsor.yaml")
                sponsors = sponsor_data.get("sponsors", []) if sponsor_data else []
                active_sponsors = [sponsor for sponsor in sponsors if sponsor.get("active", True)]
                
                gallery_images = self.get_gallery_images()
                
                # Add current_url for sharing
                current_url = f"{self.app.jinja_env.globals['base_url']}/"
                
                html = render_template(
                    "index.html",
                    latest_blogs=latest_blogs,
                    upcoming_events=upcoming_events,
                    latest_events=latest_events,
                    sponsors=active_sponsors,
                    gallery_images=gallery_images,
                    current_url=current_url,
                    current_page="index",
                )
                
                self.save_page(html, "index.html")

    def build_blog_pages(self):
        """Build all blog pages"""
        with self.app.app_context():
            with self.app.test_request_context():
                # Blog index page
                blog_posts = self.markdown_parser.get_all_posts("content/blog")
                current_url = f"{self.app.jinja_env.globals['base_url']}/blog/"
                html = render_template("blog/index.html", posts=blog_posts, current_url=current_url, current_page="blog_index")
                self.save_page(html, "blog/index.html")
                
                # Individual blog posts
                for post in blog_posts:
                    current_url = f"{self.app.jinja_env.globals['base_url']}/blog/{post['slug']}/"
                    html = render_template("blog/post.html", post=post, current_url=current_url, current_page="blog_post")
                    self.save_page(html, f"blog/{post['slug']}/index.html")

    def build_event_pages(self):
        """Build all event pages"""
        with self.app.app_context():
            with self.app.test_request_context():
                # Event index page
                events = self.markdown_parser.get_all_posts("content/event")
                current_url = f"{self.app.jinja_env.globals['base_url']}/event/"
                html = render_template("event/index.html", events=events, current_url=current_url, current_page="event_index")
                self.save_page(html, "event/index.html")
                
                # Individual event pages
                for event in events:
                    current_url = f"{self.app.jinja_env.globals['base_url']}/event/{event['slug']}/"
                    html = render_template("event/event.html", event=event, current_url=current_url, current_page="event_detail")
                    self.save_page(html, f"event/{event['slug']}/index.html")

    def build_other_pages(self):
        """Build other static pages"""
        with self.app.app_context():
            with self.app.test_request_context():
                # About page
                about_data = self.yaml_loader.load_yaml("content/about.yaml")
                current_url = f"{self.app.jinja_env.globals['base_url']}/about/"
                html = render_template("about.html", data=about_data, current_url=current_url, current_page="about")
                self.save_page(html, "about/index.html")
                
                # Organizer page
                organizer_data = self.yaml_loader.load_yaml("content/organizer.yaml")
                current_url = f"{self.app.jinja_env.globals['base_url']}/organizer/"
                html = render_template("organizer.html", data=organizer_data, current_url=current_url, current_page="organizer")
                self.save_page(html, "organizer/index.html")

    def build_error_pages(self):
        """Build error pages"""
        with self.app.app_context():
            with self.app.test_request_context():
                # 404 page
                html = render_template("404.html")
                self.save_page(html, "404.html")
                
                # 500 page
                html = render_template("500.html")
                self.save_page(html, "500.html")

    def create_cname_file(self, domain=None):
        """Create CNAME file if custom domain is specified"""
        if domain:
            cname_path = self.output_dir / "CNAME"
            with open(cname_path, 'w') as f:
                f.write(domain)
            print(f"Created CNAME file for domain: {domain}")

    def create_nojekyll_file(self):
        """Create .nojekyll file to bypass Jekyll processing on GitHub Pages"""
        nojekyll_path = self.output_dir / ".nojekyll"
        nojekyll_path.touch()
        print("Created .nojekyll file")

    def build_sitemap(self):
        """Generate sitemap.xml for SEO"""
        base_url = "https://devopsjogja.com"  # Update with your domain
        
        urls = [
            {"url": "/", "priority": "1.0"},
            {"url": "/blog/", "priority": "0.8"},
            {"url": "/event/", "priority": "0.8"},
            {"url": "/about/", "priority": "0.6"},
            {"url": "/organizer/", "priority": "0.6"},
            {"url": "/gallery/", "priority": "0.6"},
        ]
        
        # Add blog posts
        blog_posts = self.markdown_parser.get_all_posts("content/blog")
        for post in blog_posts:
            urls.append({
                "url": f"/blog/{post['slug']}/",
                "priority": "0.7",
                "lastmod": post.get('date', '')
            })
        
        # Add events
        events = self.markdown_parser.get_all_posts("content/event")
        for event in events:
            urls.append({
                "url": f"/event/{event['slug']}/",
                "priority": "0.7",
                "lastmod": event.get('date', '')
            })
        
        sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url_info in urls:
            sitemap_content += f'  <url>\n'
            sitemap_content += f'    <loc>{base_url}{url_info["url"]}</loc>\n'
            if 'lastmod' in url_info and url_info['lastmod']:
                sitemap_content += f'    <lastmod>{url_info["lastmod"]}</lastmod>\n'
            sitemap_content += f'    <priority>{url_info["priority"]}</priority>\n'
            sitemap_content += f'  </url>\n'
        
        sitemap_content += '</urlset>'
        
        sitemap_path = self.output_dir / "sitemap.xml"
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        print("Generated sitemap.xml")

    def build_all(self, custom_domain=None):
        """Build the complete static site"""
        print("🏗️  Starting static site build...")
        print("=" * 50)
        
        # Clean and prepare
        self.clean_output_dir()
        
        # Copy static files
        self.copy_static_files()
        
        # Build pages
        print("\n📝 Building pages...")
        self.build_homepage()
        self.build_blog_pages()
        self.build_event_pages()
        self.build_other_pages()
        self.build_error_pages()
        self.build_gallery_page()

    def build_gallery_page(self):
        """Build gallery page"""
        with self.app.app_context():
            with self.app.test_request_context():
                gallery_images = self.get_gallery_images()
                current_url = f"{self.app.jinja_env.globals['base_url']}/gallery/"
                html = render_template("gallery.html", gallery_images=gallery_images, current_url=current_url, current_page="gallery")
                self.save_page(html, "gallery/index.html")
        print("\n🔧 Generating additional files...")
        self.create_nojekyll_file()
        self.build_sitemap()
        
        if custom_domain:
            self.create_cname_file(custom_domain)
        
        print("\n" + "=" * 50)
        print("✅ Static site build completed!")
        print(f"📁 Output directory: {self.output_dir.absolute()}")
        print(f"📊 Total files generated: {len(list(self.output_dir.rglob('*')))} files")


if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    custom_domain = None
    if len(sys.argv) > 1:
        custom_domain = sys.argv[1]
    
    # Build the site
    builder = StaticSiteBuilder()
    builder.build_all(custom_domain)
