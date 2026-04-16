// Shared visual theme for all chart templates.
// Palette matches the site (web/css/style.css) — dark surface, cyan primary.
// Importable as an ES module from render.mjs and inlined into HTML templates.

export const theme = {
  palette: {
    // Primary cyan scale (from site --primary: #44d8f1)
    cyan: {
      50:  '#b8eff8',
      200: '#7ee6f5',
      500: '#44d8f1',
      700: '#00bcd4',
      900: '#00363e',
    },
    // Secondary lavender scale (from site --secondary: #bdc2ff)
    lavender: {
      200: '#dde0ff',
      500: '#bdc2ff',
      700: '#a8afff',
      900: '#343d96',
    },
    // Accents (pulled from site highlight palette)
    coral:  '#ff8a9e',  // site's warm accent
    amber:  '#e8c87a',
    violet: '#c4a0f5',
    mint:   '#a6e88e',
    // Neutral surfaces (dark mode, match site)
    neutral: {
      bg:            '#0e131e',
      surface:       '#0e131e',
      surfaceLow:    '#171b27',
      surface1:      '#1b1f2b',
      surface2:      '#252a36',
      surface3:      '#303541',
      border:        '#3c494c',
      borderStrong:  '#869396',
      text:          '#dee2f2',
      textMuted:     '#bbc9cc',
      textFaint:     '#869396',
    },
  },
  typography: {
    fontFamily:
      '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    displayFamily:
      '"Space Grotesk", "Inter", -apple-system, BlinkMacSystemFont, sans-serif',
    monoFamily:
      '"JetBrains Mono", ui-monospace, "SF Mono", Menlo, Consolas, monospace',
    sizes: {
      title:         '34px',
      subtitle:      '18px',
      body:          '15px',
      caption:       '13px',
      bigNumber:     '104px',
      mediumNumber:  '56px',
    },
    weights: { regular: 400, medium: 500, semibold: 600, bold: 700 },
  },
  spacing: {
    xs: '4px', sm: '8px', md: '16px', lg: '24px', xl: '40px', xxl: '64px',
  },
  radius: {
    card: '8px',
    bar:  '4px',
    pill: '999px',
  },
  // Multi-series sequence (cyan → lavender, with warm highlight)
  seriesOrder: ['#44d8f1', '#bdc2ff', '#7ee6f5', '#a8afff', '#ff8a9e', '#e8c87a'],
  highlight: '#ff8a9e',
};

export function toCSSVars(t = theme) {
  const p = t.palette;
  const css = `
:root {
  --cyan-50: ${p.cyan[50]};
  --cyan-200: ${p.cyan[200]};
  --cyan-500: ${p.cyan[500]};
  --cyan-700: ${p.cyan[700]};
  --lav-500: ${p.lavender[500]};
  --lav-700: ${p.lavender[700]};
  --coral: ${p.coral};
  --amber: ${p.amber};

  --bg: ${p.neutral.bg};
  --surface: ${p.neutral.surface};
  --surface-low: ${p.neutral.surfaceLow};
  --surface-1: ${p.neutral.surface1};
  --surface-2: ${p.neutral.surface2};
  --border: ${p.neutral.border};
  --border-strong: ${p.neutral.borderStrong};
  --text: ${p.neutral.text};
  --text-muted: ${p.neutral.textMuted};
  --text-faint: ${p.neutral.textFaint};

  --font-sans: ${t.typography.fontFamily};
  --font-display: ${t.typography.displayFamily};
  --font-mono: ${t.typography.monoFamily};
  --size-title: ${t.typography.sizes.title};
  --size-subtitle: ${t.typography.sizes.subtitle};
  --size-body: ${t.typography.sizes.body};
  --size-caption: ${t.typography.sizes.caption};
  --size-big: ${t.typography.sizes.bigNumber};
  --size-medium: ${t.typography.sizes.mediumNumber};

  --s-xs: ${t.spacing.xs}; --s-sm: ${t.spacing.sm}; --s-md: ${t.spacing.md};
  --s-lg: ${t.spacing.lg}; --s-xl: ${t.spacing.xl}; --s-xxl: ${t.spacing.xxl};

  --radius-card: ${t.radius.card};
  --radius-bar: ${t.radius.bar};
}

html, body {
  margin: 0; padding: 0;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
  font-size: var(--size-body);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
`;
  return `<style>${css}</style>`;
}

export default theme;
