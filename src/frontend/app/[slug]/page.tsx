'use client';

import CopyButton from "@/components/CopyButton";
import {useEffect, useState} from "react";
import {Input, Button} from "@nextui-org/react";


interface PageParams {
	slug: string;
}


const ConversationRender = ({messages}: { messages: any[] | undefined }) => {
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
						<div
							className={`text-black p-4 rounded-lg shadow ${message?.type === 'human' ? 'bg-blue-100 text-right' : 'bg-gray-100 text-left'}`}>
							{message?.content}
							<CopyButton text={message?.content}/>
						</div>
					</div>
				))}
			</div>
		);
	}
};


export default function Conversation({params}: { params: PageParams }) {
	const sessionId = params.slug;
	const [conversation, setConversation] = useState([])
	const [message, setMessage] = useState('')
	const [isLoading, setIsLoading] = useState(false);

	const fetchChatHistory = async () => {
		try {
			const response = await fetch("http://localhost:8000/conversation/" + sessionId);
			const data = await response.json();
			setConversation(data);
		} catch (error) {
			console.log("Error fetching chat history");
		}
	};

	const sendMessage = async (e: any) => {
		e.preventDefault();
		setMessage('');
		setIsLoading(true);

		try {
			const response = await fetch("http://localhost:8000/conversation/" + sessionId, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'accept': 'application/json'
				},
				body: JSON.stringify({'message': message})
			});

			if (response.ok) {
				setIsLoading(false);
			} else {
				console.log("Can't send message");
			}
		} catch (error) {
			console.log("Error sending message. Please try again later.");
		} finally {
			await fetchChatHistory();
		}
	}

	useEffect(() => {
		fetchChatHistory();
	}, []);

	return (
<>
  <div className="relative min-h-screen pb-16">
    <div className="p-4 sm:ml-64">
      <ConversationRender messages={conversation} />
    </div>
  </div>
  <div className="p-4 flex justify-center fixed bottom-0 w-full">
    <form onSubmit={sendMessage} className="flex items-center">
      <div className="sm:pl-64">
        <Input value={message} type={"text"} onChange={(e) => setMessage(e.target.value)} />
      </div>
      <Button isLoading={isLoading} type={"submit"}>Send</Button>
    </form>
  </div>
</>


	);
}