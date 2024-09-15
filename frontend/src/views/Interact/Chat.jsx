import { React, useEffect, useState } from "react";

export default function Chat() {
  const modeldict = {
    "Llama-2-13b":"llama2",
    "Llama-3-7b":"llama3"
  }
  const [clientId, setClienId] = useState(Math.floor(new Date().getTime() / 1000));
  const [input, setInput] = useState("");
  const [stream, setStream] = useState(false);

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const [selmodel,setSelModel] = useState("Llama-2-13b")
  const [role, setRole] = useState("System");
  const [roleContent, setRoleContent] = useState("");
  const [topp, setTopp] = useState(0.1);
  const [topk, setTopK] = useState(40);
  const [temp, setTemp] = useState(0.7);
  const [maxt, setMaxT] = useState(200);
  const [websckt, setWebsckt] = useState();
  const [evtsrc,setEvtSrc] = useState();

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
      stream: stream,
    };
    return fetch("https://dcaf.cisco.com/api/"+modeldict[selmodel]+"/ChatCompletion", {
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
    const ws = new WebSocket("wss://dcaf.cisco.com/ws/"+modeldict[selmodel]+"/ChatCompletion/" + clientId);
    ws.onmessage = (e) => {
      console.log(e.data);
      setMessages((messages) => {
        const newmessages = [...messages];
        newmessages[newmessages.length - 1].text += e.data;
        return newmessages;
      });
    };
    ws.onclose = () => {
      console.log("Websocket Closed");
    };
    setWebsckt(ws);
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
        stream: stream,
      };
      websckt.send(JSON.stringify(data));
    }
  };
  return (
    <>
      <div className="max-h-screen flex  pl-2" style={{ maxHeight: "90vh" }}>
        <div className="col-span-2 flex flex-col w-full bg-gray-100">
          <div className="flex-grow overflow-y-scroll md:overflow-scroll" style={{ maxHeight: "80vh" }}>
            {messages.map((mess, index) => (
              <div className={`message ${mess.user ? "chat chat-start" : "chat chat-end"}`} key={index}>
                <div className=" chat-bubble light:chat-bubble-error" >
                  <pre className="text-balance">{!mess.user && mess.text === "" ? <span className="loading loading-dots loading-lg"></span> : mess.text}</pre>
                </div>
              </div>
            ))}
          </div>
          <div className="py-3  w-full bg-white">
            <form onSubmit={handleSubmit}>
              <input
                className="w-full bg-gray-100 py-5 px-3 rounded-xl text-gray-900 dark:text-gray-300"
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message here..."
              />
            </form>
          </div>
        </div>
        <div className="flex flex-col w-auto pl-2 overflow-y-auto max-h-screen" style={{ maxHeight: "90vh" }}>
          <form>
            <article className=" md:mx-0 md:mr-16">
              <fieldset className="grid gap-4 rounded-lg border p-2">
                <legend className="text-sm">Settings</legend>
                <label className="form-control w-full max-w-xs">
                  <div className="label">
                    <span className="label-text">Select Model</span>
                  </div>
                  <select className="select select-bordered" onChange={(e)=>{setSelModel(e.target.value)}}>
                    <option defaultValue="Llama-2-13b">Llama-2-13b</option>
                    <option defaultValue="Llama-2-13b">Llama-3-7b</option>
                  </select>
                </label>
                <label className="form-control w-full max-w-xs">
                  <div className="label">
                    <span className="label-text">Temperature</span>
                  </div>
                  <input
                    type="number"
                    placeholder="0.4"
                    value={temp}
                    onChange={(e) => {
                      setTemp(e.target.value);
                    }}
                    className="input input-bordered input-success w-full max-w-xs"
                    required
                  />
                </label>
                <label className="form-control w-full max-w-xs">
                  <div className="label">
                    <span className="label-text">Max Tokens</span>
                  </div>
                  <input
                    type="number"
                    placeholder="200"
                    value={maxt}
                    onChange={(e) => {
                      setMaxT(e.target.value);
                    }}
                    className="input input-bordered input-success w-full max-w-xs"
                    required
                  />
                </label>
                <div className="grid grid-cols-2 gap-4">
                  <label className="grid gap-3 form-control w-full max-w-xs">
                    <div className="label">
                      <span className="label-text">Top_P</span>
                    </div>
                    <input
                      type="number"
                      placeholder="0.4"
                      value={topp}
                      onChange={(e) => {
                        setTopp(e.target.value);
                      }}
                      className="input input-bordered input-success w-full max-w-xs"
                      required
                    />
                  </label>
                  <label className="grid gap-3 form-control w-full max-w-xs">
                    <div className="label">
                      <span className="label-text">Top_K</span>
                    </div>
                    <input
                      type="number"
                      placeholder="0.4"
                      value={topk}
                      onChange={(e) => {
                        setTopK(e.target.value);
                      }}
                      className="input input-bordered input-success w-full max-w-xs"
                      required
                    />
                  </label>
                </div>
                <div className="form-control">
                  <label className="label cursor-pointer">
                    <span className="label-text">Stream Output</span>
                    <input
                      type="checkbox"
                      className="toggle"
                      onChange={() => {
                        setStream(!stream);
                      }}
                    />
                  </label>
                </div>
              </fieldset>
              <fieldset className="grid gap-4 rounded-lg border p-2">
                <legend className="text-sm">Messages</legend>
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
                    placeholder="You are a..."
                    className="textarea textarea-bordered min-h-[9.5rem]"
                  />
                </div>
              </fieldset>{" "}
              <fieldset className="grid gap-4 rounded-lg border p-2">
                <legend className="text-sm">Response Statistics</legend>
                <div className="label">
                  <span className="label-text">Total Input Tokens: </span> 1000
                </div>
                <div className="label">
                  <span className="label-text">Total Output Tokens: </span> 1000
                </div>
                <div className="label">
                  <span className="label-text">Time to First Token: </span> 1000
                </div>
                <div className="label">
                  <span className="label-text">Tokens Per Second: </span> 1000
                </div>
              </fieldset>
            </article>
          </form>
        </div>
      </div>
    </>
  );
}