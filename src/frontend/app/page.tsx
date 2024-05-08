'use client'
import {useEffect, useState} from "react";


async function getConversationList(){
  const res = await fetch("http://localhost:8000/conversation/",
    {
      cache: 'no-cache'
    })
  return res.json()
}


async function getConversation(sessionId: string){
  const res = await fetch("http://localhost:8000/conversation/" + sessionId,
    {
      cache: 'no-store'
    })
  return res.json()
}

async function createConversation(){
  const res = await fetch("http://localhost:8000/conversation/", {
    method: 'POST'
  })
  return res.json()
}



const Conversation = ({ messages }: {messages: any[] | undefined}) => {
  console.log(messages?.length);
  if (!messages || messages.length == 0 || !Array.isArray(messages)) {
    return <div className="text-center text-gray-500">No messages yet</div>;
  } else {
    return (
      <div className="flex flex-col space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`${
              message?.type === 'human' ? 'self-end' : 'self-start'
            } max-w-md mx-2`}
          >
            <div className={`text-black p-4 rounded-lg shadow ${message?.type === 'human' ? 'bg-blue-100 text-right' : 'bg-gray-100 text-left'}`}>
              {message?.content}
            </div>
          </div>
        ))}
      </div>
    );
  }
};



export default function Home() {
  const [sessionId, setSessionId] = useState()
  const [conversations, setConversations] = useState([])
  const [conversation, setConversation] = useState([])

  useEffect(() => {
    async function fetchData() {
      const data = await getConversationList();
      setConversations(data);
      setSessionId(data?.session_id[0])

      const conversation = await getConversation(sessionId);
      setConversation(conversation)
    }
    fetchData();

  }, [sessionId]);

  const handleCreateConversation = async () => {
    const newConversation = await createConversation();
    setSessionId(newConversation.session_id)
    setConversation(sessionId)
  }

  return (
    <>

      <button data-drawer-target="default-sidebar" data-drawer-toggle="default-sidebar" aria-controls="default-sidebar"
              type="button"
              className="inline-flex items-center p-2 mt-2 ms-3 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600">
        <span className="sr-only">Open sidebar</span>
        <svg className="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20"
             xmlns="http://www.w3.org/2000/svg">
          <path clip-rule="evenodd" fill-rule="evenodd"
                d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"></path>
        </svg>
      </button>

      <aside id="default-sidebar"
             className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0"
             aria-label="Sidebar">

        <div className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
          <ul className="space-y-2 font-medium mb-5">
              <li>
                <a href="#"
                   className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
                  <button onClick={handleCreateConversation} className="ms-3">New conversation</button>
                </a>
              </li>
          </ul>

          <ul className="space-y-2 font-medium">
            {conversations?.session_id?.map(session_id => (
              <li key={session_id}>
                <a href="#"
                   className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
                  <span className="ms-3">{session_id}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      </aside>

      <div className="p-4 sm:ml-64">
        <Conversation messages={conversation}/>
      </div>

    </>
  );
}
