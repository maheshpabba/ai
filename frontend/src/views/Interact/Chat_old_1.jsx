import {React,useRef} from "react"


const n=10

export default function Chat_old_1() {

    return (
    <>
            <div class="grid grid-cols-3 gap-4">

  <div class="col-span-3">04</div>
  <div class="">05</div>

</div>










    {/* <div className="h-screen flex gap-4">   
        <div className="flex flex-none pt-4 w-64 min-h-full">
            <form>
                <article className="mb-16 md:mx-0 md:mr-16">
                        <fieldset className="grid gap-4 rounded-lg border p-2">
                            <legend className="text-sm">Settings</legend>
                            <label className="form-control w-full max-w-xs">
                                <div className="label">
                                    <span className="label-text">Select Model</span>
                                </div>
                                <select className="select select-bordered">
                                    <option defaultValue="Llama-2-13b">Llama-2-13b</option>
                                </select>
                            </label>
                            <label className="form-control w-full max-w-xs">
                                <div className="label">
                                    <span className="label-text">Temperature</span>
                                </div>
                                <input type="number" placeholder="0.4" className="input input-bordered input-success w-full max-w-xs" required />
                            </label>
                            <div className="grid grid-cols-2 gap-4">
                                <label className="grid gap-3 form-control w-full max-w-xs">
                                    <div className="label">
                                        <span className="label-text">Top_P</span>
                                    </div>
                                    <input type="number" placeholder="0.4" className="input input-bordered input-success w-full max-w-xs" required />
                                </label>
                                <label className="grid gap-3 form-control w-full max-w-xs">
                                    <div className="label">
                                        <span className="label-text">Top_K</span>
                                    </div>
                                    <input type="number" placeholder="0.4" className="input input-bordered input-success w-full max-w-xs" required />
                                </label>
                            </div>
                        </fieldset>
                        <fieldset className="grid gap-4 rounded-lg border p-2">
                            <legend className="text-sm">Messages</legend>
                            <label className="form-control w-full max-w-xs">
                                <div className="label">
                                    <span className="label-text">Role</span>
                                </div>
                                <select className="select select-bordered">
                                    <option >System</option>
                                    <option defaultValue="User">User</option>
                                    <option>Assistant</option>
                                </select>
                            </label>
                            <div className="grid gap-3">
                                <label htmlFor="content">Content</label>
                                <textarea
                                    id="content"
                                    placeholder="You are a..."
                                    className="textarea textarea-bordered min-h-[9.5rem]"
                                />
                                </div>
                        </fieldset>
                </article>
            </form>
        </div>
        <div className="flex flex-col overflow-y-auto w-full min-h-[50vh] pt-4 bg-gray-100 ">    
            <div className="flex-grow md:flex-grow-0 overflow-y-auto">
                {[...Array(n)].map((e, i) => (
                    <div key={i}> Content </div>
                ))}
            </div>
            <div className="flex-none ">
                <div className="grid grid-flow-row auto-rows-max ">
                    <div>
                        <label className="input input-bordered input-lg flex items-center gap-6">
                            <input type="text" className="grow" placeholder="Type Your Text Here" />
                            <svg className="h-8 w-8 text-gray-500"  width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" fill="none" strokeLinecap="round" strokeLinejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <line x1="10" y1="14" x2="21" y2="3" />  <path d="M21 3L14.5 21a.55 .55 0 0 1 -1 0L10 14L3 10.5a.55 .55 0 0 1 0 -1L21 3" /></svg>
                        </label>
                    </div>
                </div>
            </div>

        </div>
    </div> */}

    </>
    )

}


