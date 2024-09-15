import React, { lazy, Suspense } from "react"
import { Route } from "wouter"
import { Provider} from "jotai"
import ThemeProvider from "./components/Theme"
import Layout from "./components/Layout"
import Chat from "./views/Interact/Chat"
// import ChatW from "./views/Interact/ChatW"
const Home = lazy(() => import("./views/Home"))
const RequireSession = lazy(() => import( "./views/Auth"))
const Code = lazy(() => import("./views/Interact/Code"))
const RagChat = lazy(() => import("./views/Custom/RAGChat"))
const Train = lazy(() => import ("./views/Custom/Train"))
const Workflows = lazy(() => import ("./views/Custom/Workflows"))
function App() {
  return (
    <RequireSession>
      <Provider>
        <ThemeProvider>
          <Layout>
            
              <Route path="/" component={Home} />
              {/* Interact */}
              <Route path="/Chat" component={Chat} />
              {/* <Route path="/ChatW" component={ChatW} /> */}
              <Route path="/Code" component={Code} />

              {/* Custom */}
              <Route path="/RAGChat" component={RagChat} />
              <Route path="/Train" component={Train} />
              <Route path="/Workflows" component={Train} />
           
          </Layout>
        </ThemeProvider>
      </Provider>
    </RequireSession>
  )
}

export default App
