import { useEffect } from "react"
import { atom, useAtom } from "jotai"

export const darkAtom = atom(false)

export function useDark() {
	return useAtom(darkAtom)
}

export default function ThemeProvider({ children }) {
	const [dark, setDark] = useAtom(darkAtom)

	useEffect(() => {
		const systemTheme = window.matchMedia("(prefers-color-scheme: dark)")
		setDark(systemTheme.matches)
		const handler = (e) => setDark(e.matches)
		systemTheme.addEventListener("change", handler)
		return () => systemTheme.removeEventListener("change", handler)
	}, [])

	useEffect(() => {
		document
			.querySelector("html")
			.setAttribute("data-theme", dark ? "dark" : "light")
	}, [dark])
	return children
}