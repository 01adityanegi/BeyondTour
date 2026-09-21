/**
 * Beyond Tour — Tailwind Play CDN Configuration
 * Configures the Himalayan color palette, custom serif typography, shadows, and animations.
 */
if (typeof tailwind !== 'undefined') {
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          'ivory':            '#F7F3EC',
          'pine':             '#16302B',
          'pine-dark':        '#0E201C',
          'charcoal':         '#2B2A28',
          'charcoal-light':   '#4A4844',
          'terracotta':       '#C1622D',
          'terracotta-hover': '#A65123',
          'sage':             '#6B8F71',
          'sage-light':       '#EBF2EC',
          'stone':            '#DCD3C4',
          'surface':          '#FFFFFF',
          // Legacy aliases remapped to palette
          'deodar':           '#16302B',
          'deodar-light':     '#1E433C',
          'rust':             '#C1622D',
          'rust-light':       '#A65123',
          'marigold':         '#C1622D',
          'marigold-light':   '#A65123',
          'aipan':            '#C1622D',
          'slate-ink':        '#2B2A28',
          'mist':             '#F7F3EC',
          'mist-dark':        '#DCD3C4',
          'alpine':           '#6B8F71',
        },
        fontFamily: {
          serif:  ['CleanAmpersand', 'Georgia', 'Fraunces', 'serif'],
          sans:   ['Manrope', 'Inter', 'sans-serif'],
        },
        boxShadow: {
          'card':       '0 2px 16px rgba(22, 48, 43, 0.06)',
          'card-hover': '0 8px 30px rgba(22, 48, 43, 0.12)',
          'hero':       '0 24px 60px rgba(22, 48, 43, 0.25)',
        },
        borderRadius: {
          'card': '16px',
        },
        animation: {
          'fade-up': 'fadeUp 0.6s ease-out forwards',
          'fade-in': 'fadeIn 0.4s ease-out forwards',
          'slide-right': 'slideRight 0.5s ease-out forwards',
        },
        keyframes: {
          fadeUp: {
            '0%': { opacity: '0', transform: 'translateY(30px)' },
            '100%': { opacity: '1', transform: 'translateY(0)' },
          },
          fadeIn: {
            '0%': { opacity: '0' },
            '100%': { opacity: '1' },
          },
          slideRight: {
            '0%': { opacity: '0', transform: 'translateX(-20px)' },
            '100%': { opacity: '1', transform: 'translateX(0)' },
          },
        },
      }
    }
  };
}
