# Website Komunitas DevOps Jogja

Website komunitas modern untuk DevOps Jogja yang dibangun dengan Flask dan Tailwind CSS.


## 🚀 Fitur

- **Modern Homepage** - Kesan teknologi infrastruktur dengan design responsif
- **Blog System** - Artikel dan blog teknologi dari file Markdown
- **Event Management** - Informasi event dari file Markdown & integrasi Google Calendar
- **Organizer Profiles** - Profil pengurus dari file YAML
- **Community Calendar** - Sinkronisasi jadwal otomatis dengan Google Calendar
- **About Page** - Informasi komunitas dari file YAML
- **Responsive Design** - Menggunakan Tailwind CSS

## 📋 Pra-syarat

- Python 3.11+
- uv 0.7+
- Node.js 14+
- npm atau yarn

## 🛠️ Instalasi

### 1. Kloning Repositori

```bash
git clone https://github.com/devops-jogja/devops-jogja-website.git
cd devops-jogja-website
```

### 2. Siapkan 'environment' python

```bash
# Sync 'environment' dengan uv
uv sync --locked
```

### 3. Siapkan Tailwind CSS

```bash
# Install Node.js dependencies
npm install

# Build Tailwind CSS
npm run build-css
```

### 4. Jalankan Aplikasi

```bash
# Dengan uv
uv run app.py
```

Website akan berjalan di `http://localhost:3000`

## 📁 Struktur Project

```
devops-jogja-website/
├── app.py                 # Main Flask application
├── pyproject.toml         # Python dependencies
├── package.json           # Node.js dependencies
├── tailwind.config.js     # Tailwind configuration
├── static/
│   ├── css/
│   │   ├── input.css     # Tailwind input
│   │   ├── output.css    # Compiled CSS
│   │   └── homepage.css  # Homepage specific styles
│   ├── js/
│   │   ├── main.js       # Global JavaScript
│   │   └── homepage.js   # Homepage specific JS
│   ├── images/           # Image assets
│   │   ├── gallery/      # Gallery slider images
│   │   └── sponsor/      # Sponsor logos
│   └── organizer/        # Organizer photos
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── blog/
│   │   ├── index.html    # Blog listing
│   │   └── post.html     # Blog post detail
│   ├── event/
│   │   ├── index.html    # Event listing
│   │   └── event.html    # Event detail
│   ├── organizer.html    # Organizer page
│   ├── schedule.html     # Community Calendar schedule page
│   ├── about.html        # About page
│   ├── gallery.html      # Gallery page
│   └── 404.html          # Error page
├── content/
│   ├── blog/             # Blog posts (Markdown)
│   ├── event/            # Events (Markdown)
│   ├── organizer.yaml    # Organizer data
│   └── about.yaml        # About page data
└── utils/
    ├── __init__.py
    ├── markdown_parser.py # Markdown parser
    └── yaml_loader.py    # YAML loader
```

## 📝 Manajemen konten

### Blog Posts

Buat file Markdown di folder `content/blog/` dengan format:

```markdown
---
title: "Judul Blog Post"
date: "2024-01-15"
author: "Nama Author"
excerpt: "Ringkasan artikel"
tags: ["DevOps", "Docker", "Kubernetes"]
featured_image: "blog-image.jpg"
---

Konten blog post Anda di sini...
```

### Events

Buat file Markdown di folder `content/event/` dengan format:

```markdown
---
title: "Nama Event"
date: "2024-02-20"
time: "19:00 WIB"
location: "Venue Name, Yogyakarta"
type: "Workshop" # Workshop, Meetup, Conference
registration_url: "https://eventbrite.com/..."
featured_image: "event-image.jpg"
---

Deskripsi event Anda di sini...

### Community Calendar

Halaman schedule (`/schedule`) menggunakan integrasi Google Calendar API (via backend proxy) untuk menampilkan jadwal terbaru secara real-time. Link subscribe tersedia di bagian bawah halaman untuk memudahkan user menambahkan kalender ke akun Google mereka.
```

### Organizer Data

Edit file `content/organizer.yaml`:

```yaml
organizers:
  - name: "Nama Organizer"
    role: "Founder & Lead"
    bio: "Deskripsi singkat"
    photo: "organizer-1.jpg"
    social:
      github: "username"
      linkedin: "username"
      twitter: "username"
```

### About Page

Edit file `content/about.yaml`:

```yaml
about:
  title: "Tentang DevOps Jogja"
  description: "Komunitas DevOps di Yogyakarta"
  mission: "Misi komunitas"
  vision: "Visi komunitas"
  contact:
    email: "hello@devopsjogja.org"
    telegram: "@devopsjogja"
```

### Gallery Images

Upload gambar ke folder `static/images/gallery/` untuk ditampilkan di gallery slider homepage:

- **Format yang didukung**: JPG, PNG, GIF, WebP, **HEIC/HEIF**
- **Ukuran optimal**: 1200x675 pixels (16:9 aspect ratio)
- **File size**: Maksimal 2MB per gambar
- **Naming**: Gunakan nama deskriptif seperti `meetup-docker-workshop-2024.jpg`

**🆕 HEIC Support:**
- File HEIC/HEIF otomatis dikonversi ke format JPEG
- Kualitas konversi 90% untuk menjaga detail gambar
- File hasil konversi disimpan di `static/images/gallery/converted/`
- Konversi hanya dilakukan sekali, file berikutnya menggunakan cache

**Fitur Gallery Slider:**
- **Auto-running**: Berganti slide otomatis setiap 4 detik
- **Navigation**: Tombol prev/next (muncul saat hover di desktop)
- **Indicators**: Dots navigation untuk loncat ke slide tertentu
- **Touch Support**: Swipe gesture untuk mobile devices
- **Keyboard**: Arrow keys untuk navigasi
- **Responsive**: Optimized untuk semua ukuran layar
- **Clean Display**: Tampilan bersih tanpa nama file

Gallery akan pause saat di-hover dan otomatis melanjutkan setelah mouse keluar.

## 🎨 Customization

### Tailwind CSS

Edit `static/css/input.css` untuk menambah custom styles:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
.tech-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

Kemudian build ulang CSS:

```bash
npm run build-css
```

### JavaScript

Tambahkan interaktivitas di `static/js/main.js`.

## 🚀 Deployment

### Menggunakan Docker

```bash
# Build image
docker build -t devops-jogja-website .

# Run container
docker run -p 3000:3000 devops-jogja-website
```

### Menggunakan Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create devops-jogja-website

# Deploy
git push heroku main
```

### Menggunakan Railway

1. Hubungkan GitHub repository ke Railway
2. Deploy otomatis setiap push ke main branch

## 🤝 Berkontribusi

1. Fork repository
2. Buat feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

### Content Contribution

- **Blog Posts**: Submit PR dengan file Markdown baru di `content/blog/`
- **Events**: Submit PR dengan file Markdown baru di `content/event/`
- **Bug Reports**: Gunakan GitHub Issues

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **DevOps Jogja Community** - [Website](https://devopsjogja.org)
- **GitHub** - [@devops-jogja](https://github.com/devops-jogja)

## 🙏 Acknowledgments

- Flask framework
- Tailwind CSS
- Python Markdown
- PyYAML
- Semua kontributor komunitas DevOps Jogja

---

**DevOps Jogja** - Building Infrastructure, Building Community 🚀
