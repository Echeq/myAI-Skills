# Scroll-Style Pharmacy Landing Page — Plan

## Subtask Breakdown

### Subtask 1: HTML Skeleton & Head
- `<!DOCTYPE html>`, `<html lang="en">`, `<head>` with meta viewport, title
- Google Fonts link (e.g. Inter, Playfair Display)
- Font Awesome CDN link (v6)
- Link to inline `<style>` and inline `<script>` (both in same file)
- Semantic HTML5 layout

### Subtask 2: CSS — Reset, Variables, Typography
- CSS reset (box-sizing, margin/padding zero)
- `:root` variables for color palette:
  - `--primary: #2d6a4f` (deep green)
  - `--primary-light: #52b788` (mid green)
  - `--accent: #95d5b2` (soft green)
  - `--bg-light: #f0f7f4` (pale green-white)
  - `--white: #ffffff`
  - `--text-dark: #1b4332` (dark green)
  - `--text-muted: #555`
  - `--shadow: rgba(0,0,0,0.1)`
- Base typography (body, headings, links)
- `html { scroll-behavior: smooth; }`

### Subtask 3: CSS — Full-Page Scroll Sections
- Each `<section>` is `min-height: 100vh`, `display: flex`, `align-items: center`, `justify-content: center`
- `.section-inner { max-width: 1100px; margin: 0 auto; padding: 2rem; }`
- Section-specific background alternating: `.hero` (primary gradient), `.about` (white), `.services` (bg-light), `.products` (white), `.testimonials` (bg-light), `.contact` (white)

### Subtask 4: CSS — Fixed Navigation Bar
- `<nav>` fixed top, full-width, `z-index: 1000`, semi-transparent white background with blur
- Horizontal nav links, underlined or highlighted with `--primary` on active section
- `.nav-link.active { color: var(--primary); border-bottom: 2px solid var(--primary); }`
- Hamburger menu for mobile (`@media max-width: 768px`)

### Subtask 5: CSS — Scroll Animations (fade-in)
- `.fade-in { opacity: 0; transform: translateY(30px); transition: opacity 0.8s ease, transform 0.8s ease; }`
- `.fade-in.visible { opacity: 1; transform: translateY(0); }`
- Staggered delays via `nth-child` for child cards

### Subtask 6: CSS — Component Styles
- **Hero**: big heading (3rem+), tagline, CTA button (pill shape, primary bg)
- **About**: 3 value cards in a CSS grid (`grid-template-columns: repeat(3, 1fr)`)
- **Services**: 4 service cards in a grid with icons (Font Awesome)
- **Products**: 4 product cards with illustrations/placeholders
- **Testimonials**: 3 testimonial cards with quote styling, avatar placeholders
- **Contact**: 2-column grid (info left, form right). Form inputs: name, email, phone, message, submit button
- Responsive breakpoints: 768px (stack grids), 480px (smaller text)

### Subtask 7: HTML — Hero Section
- Full viewport, background gradient (primary → primary-light), white text
- Pharmacy name (e.g. "GreenLeaf Pharmacy"), tagline, CTA button ("Visit Us Today" → scrolls to #contact)

### Subtask 8: HTML — About Section
- Heading "Why Choose Us"
- 3 cards: Trust (fa-handshake), Quality (fa-certificate), Care (fa-heart)
- Each with short descriptive paragraph

### Subtask 9: HTML — Services Section
- Heading "Our Services"
- 4 cards: Prescriptions (fa-prescription), Home Delivery (fa-truck), Vaccinations (fa-syringe), Health Check-ups (fa-stethoscope)

### Subtask 10: HTML — Products Section
- Heading "Shop Our Products"
- 4 cards: Medications (fa-pills), Vitamins (fa-leaf), Personal Care (fa-soap), Baby Products (fa-baby)
- Each with placeholder price/description

### Subtask 11: HTML — Testimonials Section
- Heading "What Our Customers Say"
- 3 testimonial cards with avatar placeholder (fa-user-circle), quote, name, star rating (fa-star)

### Subtask 12: HTML — Contact Section
- Heading "Get In Touch"
- Left column: address (fa-location-dot), phone (fa-phone), hours (fa-clock)
- Right column: form with name, email, phone, message `<textarea>`, submit button

### Subtask 13: HTML — Footer
- Simple footer with copyright, back-to-top link

### Subtask 14: JS — Scroll Spy
- `IntersectionObserver` on all sections (threshold 0.4–0.5)
- On intersection, add `.visible` class for animation and update active nav link

### Subtask 15: JS — Smooth Nav Click
- `document.querySelectorAll('.nav-link').forEach(...)` → prevent default, `scrollIntoView({ behavior: 'smooth' })`

### Subtask 16: JS — Mobile Hamburger Toggle
- Toggle `.nav-links` visibility on hamburger click

### Subtask 17: JS — Contact Form Placeholder Handler
- `submit` event listener: `e.preventDefault()`, show a success toast/alert
- No backend — client-side only

## Dependencies

**None.** All subtasks target the same single HTML file and can be implemented in any order. The file is assembled incrementally.

## HTML Structure Outline

```
index.html
├── <head>
│   ├── Google Fonts link
│   └── Font Awesome CDN
├── <nav> (fixed)
│   ├── .logo
│   ├── .nav-links
│   └── .hamburger (mobile)
├── <main>
│   ├── <section#hero>     — Hero
│   ├── <section#about>    — About (values)
│   ├── <section#services> — Services
│   ├── <section#products> — Products
│   ├── <section#testimonials> — Testimonials
│   └── <section#contact>  — Contact
├── <footer>
└── <script>
    ├── IntersectionObserver (scroll spy + animations)
    ├── Nav click handlers
    ├── Mobile toggle
    └── Form handler
```

## CSS Architecture

| What | Approach |
|---|---|
| Reset | Universal `box-sizing`, `margin: 0`, `padding: 0` |
| Variables | `:root` with green/white/blue palette |
| Layout | Flexbox centering per section, CSS Grid for card grids |
| Scroll snap | `scroll-snap-type: y mandatory` on `<main>` (progressive enhancement) |
| Animation | `.fade-in` + `.visible` via `IntersectionObserver` |
| Nav | Fixed position, `backdrop-filter: blur(8px)`, active link via class |
| Responsive | `@media (max-width: 768px)` single-column grids + hamburger |

## JS Needed

1. **IntersectionObserver** — Observe all sections with `threshold: 0.4`
   - Add `.visible` to `.fade-in` children
   - Toggle `.active` on corresponding `.nav-link`
2. **Nav click** — `scrollIntoView({ behavior: 'smooth', block: 'start' })`
3. **Mobile menu** — Toggle `.nav-links` open/closed
4. **Form** — Prevent default, show success message
