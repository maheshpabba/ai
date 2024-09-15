import React from "react";
import Navbar from "./Navbar";
import Drawer from "./Drawer";

// import Footer from "@/components/Footer"

export default function Layout({ children }) {
  return (
    <>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <div className="drawer drawer-mobile lg:drawer-open flex flex-1 relative">
          <input id="caf-drawer" type="checkbox" className="drawer-toggle" />
          <div className="drawer-side" style={{ height: "100%" }}>
            <label htmlFor="caf-drawer" className="drawer-overlay"></label>
            <Drawer />
          </div>
          <div className="drawer-content flex flex-col flex-1 overflow-y-auto">
            <div className="flex flex-col px-4 w-full max-w-7xl grow">
              <div className="items-start grow">{children}</div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}