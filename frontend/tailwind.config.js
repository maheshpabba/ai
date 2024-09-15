/** @type {import('tailwindcss').Config} */
const { addDynamicIconSelectors } = require("@iconify/tailwind")

export default {
	plugins: [
		require("@tailwindcss/typography"),
		require("daisyui"),
		addDynamicIconSelectors(),
	],
	content: ["**/*.jsx"],
	daisyui: {
		darkTheme: "dark",
		themes: [
			{
				light: {
					primary: "#107daa",
					"primary-content": "#ffffff",
					secondary: "#ffffff",
					"secondary-content": "#107daa",
					accent: "#54b9e6",
					"accent-content": "#f2f2f2",
					neutral: "#f2f2f2",
					"neutral-content": "#000000",
					"base-100": "#ffffff",
					info: "#d7eafc",
					success: "#ddf2d8",
					warning: "#ffe6bd",
					error: "#ffdad8",
				},
				dark: {
					primary: "#107daa",
					"primary-content": "#eceff4",
					secondary: "#eceff4",
					"secondary-content": "#107daa",
					accent: "#54b9e6",
					"accent-content": "#f2f2f2",
					neutral: "#434c5e",
					"neutral-content": "#d8dee9",
					"base-100": "#2e3440",
					info: "#d7eafc",
					success: "#ddf2d8",
					warning: "#ffe6bd",
					error: "#ffdad8",
				},
			},
		],
	},
}
