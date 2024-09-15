import { React, useState, useEffect } from "react";

export default function RagChat() {
  const [clientId, setClienId] = useState(Math.floor(new Date().getTime() / 1000));
  const [input, setInput] = useState("");
  const [stream, setStream] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [role, setRole] = useState("System");
  const [roleContent, setRoleContent] = useState("");
  const [topp, setTopp] = useState(0.1);
  const [topk, setTopK] = useState(40);
  const [temp, setTemp] = useState(0.7);
  const [maxt, setMaxT] = useState(200);
  const [websckt, setWebsckt] = useState();
  const chatWithModel = async () => {
    const data = {
      role: role,
      roleContent: roleContent,
      model: "llama2",
      userMessage: input,
      max_new_tokens: maxt,
      top_p: topp,
      top_k: topk,
      temperature: temp,
    };
    return fetch("http://localhost:5000/llm/ChatCompletion", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((data) => {
        return data.json();
      })
      .catch((error) => {
        console.log(error.message);
      });
  };

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:5000/ws/stream/" + clientId);
    setWebsckt(ws);
    return () => {
      ws.close;
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMessage = { text: input, user: true };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");
    setRoleContent("");
    if (!stream) {
      const aiMessage = { text: "", user: false };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
      const response = await chatWithModel();
      const newaiMessage = { text: response.response, user: false };
      setMessages((prevMessages) => [...prevMessages.slice(0, -1), newaiMessage]);
    } else {
      const aiMessage = { text: message, user: false };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
      const data = {
        role: role,
        roleContent: roleContent,
        model: "llama2",
        userMessage: input,
        max_new_tokens: maxt,
        top_p: topp,
        top_k: topk,
        temperature: temp,
      };
      websckt.send(JSON.stringify(data));
      // recieve message every send message
      websckt.onmessage = (e) => {
        const me = JSON.parse(e.data);
        setMessage([...message, me]);
      };
      setMessage([]);
    }
  };

  return (
    <>
      <div className="h-screen grid grid-cols-3 pt-20 overflow-auto md:overflow-scroll gap-4">
        <div className="col-span-2 flex flex-col w-full">
          <div className="flex-grow overflow-auto md:overflow-scroll bg-gray-100">
            {messages.map((message, index) => (
              <div className={`message ${message.user ? "chat chat-start" : "chat chat-end"}`} key={index}>
                <div className="chat-bubble">
                  {!message.user && message.text == "" ? <span className="loading loading-dots loading-lg"></span> : message.text}
                </div>
              </div>
            ))}
          </div>
          <div className="py-5">
            <form onSubmit={handleSubmit}>
              <input
                className="w-full bg-gray-300 py-5 px-3 rounded-xl"
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="type your message here..."
              />
            </form>
          </div>
        </div>
        <div className="flex-grow flex flex-col w-auto">
          <form>
            <article className="mb-16 md:mx-0 md:mr-16">
              <fieldset className="grid gap-4 rounded-lg border p-2">
                <legend className="text-sm">Start Here</legend>
                <label className="form-control w-full max-w-xs">
                  <div className="label">
                    <span className="label-text">File Input</span>
                  </div>
                  <input type="file" className="file-input file-input-bordered w-full max-w-xs" />
                </label>

                <label className="form-control w-full max-w-xs">
                  <div className="label">
                    <span className="label-text">Role</span>
                  </div>
                  <select
                    className="select select-bordered"
                    value={role}
                    onChange={(e) => {
                      setRole(e.target.value);
                    }}
                  >
                    <option value="System">System</option>
                    <option value="Assistant">Assistant</option>
                  </select>
                </label>
                <div className="grid gap-3">
                  <label htmlFor="content">Content</label>
                  <textarea
                    id="content"
                    value={roleContent}
                    onChange={(e) => {
                      setRoleContent(e.target.value);
                    }}
                    placeholder="You are a helpful expert ACI Network assistant. Your users are asking questions about information contained in the Healthcheck report."
                    className="textarea textarea-bordered min-h-[9.5rem]"
                  />
                </div>
              </fieldset>
            </article>
          </form>
        </div>
      </div>
    </>
  );
}