import React from "react";
import clsx from "clsx";
import { useLocation, Link } from "wouter";
import useSWR from "swr";

export default function Drawer() {
  // const [location, _] = useLocation()
  // const domains = useSWR("/api/domains", async () =>
  // 	fetch("/api/domains").then((res) => res.json()),
  // )
  // const session = useSWR("/api/sessions/mine", async () =>
  // 	fetch("/api/sessions/mine").then((res) => res.json()),
  // )
  return (
    <>
      <>
        <label className="drawer-overlay" htmlFor="caf-drawer" aria-label="close sidebar" />
        <div className="flex flex-col w-64 min-h-full bg-base-100 max-lg:pt-20 lg:pt-2">
          <ul className="menu grow">
            <li>
              <details open>
                <summary>Interact</summary>
                <ul>
                  <li>
                    <a href="/Chat">Chat</a>
                  </li>
                  {/* <li><a href="/ChatW">ChatWebSck</a></li> */}
                  <li>
                    <a href="/Code">Code</a>
                  </li>
                </ul>
              </details>
            </li>
            <li>
              <details open>
                <summary>Custom</summary>
                <ul>
                  <li>
                    <a href="/RAGChat">Retrieval Augmented Generation (RAG) </a>
                  </li>
                  <li>
                    <a href="/Train">Train A Model</a>
                  </li>
                  <li>
                    <a href="/Workflows">Workflows</a>
                  </li>
                </ul>
              </details>
            </li>
          </ul>
          <div className="px-5 grow-0">
            <ul className="menu">
              <li>
                {/* {session?.data?.user?.email ? (
            <a href="/logout">
              <span className="w-4 h-4 icon-[mdi--logout]" />
              Logout
            </a>
          ) : (
            <a href={`/login?path=${location}`}>
              <span className="w-6 h-6 icon-[mdi--login]" />
              Login
            </a>
          )} */}
              </li>
            </ul>
          </div>
        </div>
      </>
    </>
  );
}