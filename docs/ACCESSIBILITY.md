# Accessibility

The frontend uses semantic HTML, labels for form controls, visible focus
states, and text alternatives for status and error states. React renders
values as escaped text rather than injecting HTML.

The current UI is a prototype and has not been certified against a complete
WCAG audit. Before production release, test keyboard-only navigation, screen
reader announcements, color contrast, reduced motion, responsive layouts, and
form error association across supported browsers.
