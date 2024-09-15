import { useDark } from "../../components/Theme";

export default function Home() {
  const [dark, _] = useDark()
  return (
    <div className="mx-auto prose">
      <div className="flex items-center">
        {dark ? (
          <img src="/DC-AI-Dark.svg" alt="AI" className="inline-block mr-4 max-h-20" />
        ) : (
          <img src="/DC-AI.svg" alt="AI" className="inline-block mr-4 max-h-20" />
        )}
        <span className="text-3xl font-semibold">AI Frameworks</span>
        <span className="ml-4 text-gray-500">(with locally hosted LLM's)</span>
      </div>
      <p>
        The UI platform is home to Interact with private and local LLM(Large Language AI models). The goal of these AI tools is to help the DataCenter
        teams to interact with the AI models and get to know in using AI for Network Automation.
      </p>
      <div className="flex items-center">
        <p>
          <b>Select your option from the menu to the left to continue.</b>
        </p>
      </div>
    </div>        
  )
}