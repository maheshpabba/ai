import React from "react";
import { useLocation, Link } from "wouter";
import { useDark } from "./Theme";
import useSWR from "swr";

function ThemeSelector() {
  const [dark, setDark] = useDark();
  return (
    <label className="text-primary swap swap-rotate btn btn-ghost btn-circle">
      <input onClick={() => setDark(!dark)} type="checkbox" value={dark} />
      <span className="w-6 h-6 swap-on icon-[mdi--weather-night]" />
      <span className="w-6 h-6 swap-off icon-[mdi--weather-sunny]" />
    </label>
  );
}

function UserMenu({ session }) {
  if (session?.data?.user?.sub) {
    return (
      <div className="flex items-center space-x-4 font-light text-primary">
        <div className="avatar">
          <div className="w-8 rounded-full ring ring-primary ring-offset-base-100">
            <img
              className="object-cover object-top"
              alt="avatar"
              onError={console.error}
              src={`https://wwwin.cisco.com/dir/photo/zoom/${session.data.user.sub}.jpg`}
            />
          </div>
        </div>
      </div>
    );
  }
  return (
    <a href={`/login?path=${location}`} className="font-light btn btn-ghost text-primary">
      Login
    </a>
  );
}

export default function Navbar() {
  const [location, _] = useLocation();
  // const session = useSWR("/api/session/mine", () => fetch("/api/sessions/mine").then((res) => res.json()));

  return (
    <div className="sticky top-0 z-20 w-full h-16 border-b navbar border-b-base-200 bg-base-100">
      <div className="navbar-start">
        <label htmlFor="caf-drawer" aria-label="open sidebar" className="lg:hidden btn btn-square btn-ghost">
          <span className="w-6 h-6 icon-[mdi--menu]" />
        </label>
        <Link href="/" className="hidden items-center lg:flex">
          <span className="mx-2 mr-4 mb-1 w-12 h-12 bg-accent icon-[simple-icons--cisco]" />
          <span className="text-xl font-extralight">DataCenter AI Frameworks</span>
        </Link>
      </div>
      <Link href="/" className="lg:hidden navbar-center">
        <span className="mx-2 w-12 h-12 bg-accent icon-[simple-icons--cisco]" />
      </Link>
      <div className="navbar-end">
        <div className="mx-2">
          <ThemeSelector />
        </div>
        <div className="mx-2">{/* <UserMenu session={session} /> */}</div>
      </div>
    </div>
  );
}