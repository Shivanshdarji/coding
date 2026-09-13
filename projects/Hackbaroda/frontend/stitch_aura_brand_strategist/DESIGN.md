---
name: Quiet Intelligence
colors:
  surface: '#fbf9f7'
  surface-dim: '#dcdad8'
  surface-bright: '#fbf9f7'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f1'
  surface-container: '#f0edeb'
  surface-container-high: '#eae8e6'
  surface-container-highest: '#e4e2e0'
  on-surface: '#1b1c1b'
  on-surface-variant: '#434843'
  inverse-surface: '#30302f'
  inverse-on-surface: '#f3f0ee'
  outline: '#747873'
  outline-variant: '#c3c8c2'
  surface-tint: '#556157'
  primary: '#18241b'
  on-primary: '#ffffff'
  primary-container: '#2d3930'
  on-primary-container: '#95a397'
  inverse-primary: '#bccabd'
  secondary: '#5f5e5b'
  on-secondary: '#ffffff'
  secondary-container: '#e5e2dd'
  on-secondary-container: '#656461'
  tertiary: '#242118'
  on-tertiary: '#ffffff'
  tertiary-container: '#39362d'
  on-tertiary-container: '#a49e93'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e6d9'
  primary-fixed-dim: '#bccabd'
  on-primary-fixed: '#131e16'
  on-primary-fixed-variant: '#3d4a40'
  secondary-fixed: '#e5e2dd'
  secondary-fixed-dim: '#c9c6c2'
  on-secondary-fixed: '#1c1c19'
  on-secondary-fixed-variant: '#474743'
  tertiary-fixed: '#e9e2d4'
  tertiary-fixed-dim: '#ccc6b9'
  on-tertiary-fixed: '#1e1b13'
  on-tertiary-fixed-variant: '#4a463d'
  background: '#fbf9f7'
  on-background: '#1b1c1b'
  surface-variant: '#e4e2e0'
typography:
  display-lg:
    fontFamily: EB Garamond
    fontSize: 48px
    fontWeight: '500'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: EB Garamond
    fontSize: 32px
    fontWeight: '500'
    lineHeight: 40px
  headline-md:
    fontFamily: EB Garamond
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.1em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-max-width: 1200px
  gutter: 24px
  margin-mobile: 20px
  margin-desktop: 40px
---

## Brand & Style
The design system is rooted in the concept of "Quiet Luxury"—an aesthetic that prioritizes substance, intentionality, and understated elegance over loud trends. It is designed for an AI-powered content strategist app that values clarity of thought and the maturity of its insights. 

The visual language is **Minimalist** and **Spacious**, moving away from the frenetic "tech-heavy" aesthetic of typical AI tools. Instead, it evokes the feeling of a high-end editorial office or a private library. The UI uses solid, high-quality material surfaces, prioritizing legibility and a sense of calm. White space is treated as a premium asset, used to group information logically and provide the user with cognitive breathing room.

## Colors
The palette is a sophisticated, low-contrast arrangement of warm neutrals and organic tones. It avoids the harshness of pure black (#000) and pure white (#FFF) to reduce eye strain and maintain a premium feel.

- **Primary (Deep Forest Green):** Used for primary actions and subtle brand accents. It conveys growth, stability, and sophistication.
- **Secondary (Champagne/Cream):** The primary surface color. It provides a warm, tactile base that feels more luxurious than standard white.
- **Muted Charcoal:** Used for primary text to maintain high legibility without the jarring contrast of black.
- **Dusty Rose/Taupe Accent:** Reserved for secondary highlights or specific data visualizations to provide a soft contrast to the greens and creams.

## Typography
The typography system employs a classic pairing of a high-end Serif and a utilitarian Sans-serif.

- **Headlines (EB Garamond):** Used for titles, section headers, and editorial moments. The classical proportions of this serif provide an authoritative, literary tone.
- **Body & UI (Inter):** Used for all functional text, inputs, and long-form content generation results. Inter's neutrality ensures that the AI's output is easy to parse and professional.
- **Labels:** Small caps with increased letter spacing are used for metadata and category labels to create a sense of architectural structure.

## Layout & Spacing
The design system utilizes a **fixed-grid** philosophy for desktop to maintain a contained, curated feel, transitioning to a fluid layout for mobile devices.

- **Grid:** A 12-column grid with generous 24px gutters.
- **Rhythm:** An 8px linear scale governs all padding and margins. 
- **Spaciousness:** Content blocks are separated by significant vertical margins (often 64px or 80px) to distinguish different strategic themes within the app.
- **Mobile:** On smaller screens, the 12 columns collapse to 4, and margins are reduced to 20px to maximize the readable area for generated content.

## Elevation & Depth
Depth is created through **Tonal Layering** and **Ambient Shadows** rather than stark borders or glossy effects.

- **Surfaces:** The base layer is the Champagne neutral (#F5F2ED). Secondary surfaces (like cards or sidebars) use a slightly lighter Off-White (#FAF9F6) to "lift" them visually.
- **Shadows:** Use extremely diffused, low-opacity shadows with a hint of the primary green or charcoal in the tint. The goal is for the shadow to be felt rather than seen—avoiding hard edges.
- **Outlines:** Use thin (1px) low-contrast borders in a shade just slightly darker than the surface color to define boundaries in complex layouts.

## Shapes
The shape language is **Soft**. A 0.5rem (8px) base radius is applied to buttons, input fields, and cards. This provides a modern, approachable feel without becoming overly "bubbly" or informal. For large container elements like hero sections or large content cards, use a 1rem (16px) radius to emphasize the "material" nature of the UI.

## Components
- **Buttons:** Primary buttons use the Deep Forest Green with cream text. They should feel substantial but not aggressive. Secondary buttons use a tonal outline or a subtle shift in background cream. 
- **Input Fields:** Sophisticated text entries use a solid background slightly darker than the page, with a 1px bottom border that transitions to the primary green on focus. Labels should always sit above the field in the `label-caps` style.
- **Cards:** Content cards use the "Elevation" strategy—a slightly lighter background than the canvas with a very soft ambient shadow. Avoid heavy borders.
- **Chips/Tags:** Used for content categories, these should have a 1px border and use the `body-sm` font. They remain rectangular with a small 4px radius.
- **AI Response Containers:** Distinguished by a very subtle Tonal Layer (perhaps a hint of the Dusty Rose or a deeper Cream) to signal that this content was generated by the strategist tool.