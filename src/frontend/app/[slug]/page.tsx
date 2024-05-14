'use client';

import CopyButton from "@/components/CopyButton";
import {useEffect, useState} from "react";
import {Button, Input, Select, SelectItem} from "@nextui-org/react";
import Markdown from "react-markdown";
import gfm from 'remark-gfm';
import {toast} from "react-toastify";


interface PageParams {
	slug: string;
}


export function MarkdownMessage({message}: { message: string }) {
	return (
		<>
			<div className="whitespace-pre-wrap">
				<Markdown remarkPlugins={[gfm]}>{message}</Markdown>
			</div>
		</>
	)
}

async function getSnippets() {
	const res = await fetch("http://localhost:8000/snippet/", {
		method: "GET",
		headers: {
			'Content-Type': 'application/json'
		},
		cache: "no-cache"
	})
	return res.json()
}

async function createFile(formData: any, session_id: string){
	const res = await fetch("http://localhost:8000/file/chat/" + session_id + "/", {
		method: "POST",
		body: formData
	})
	return res.json()
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
							<MarkdownMessage message={message?.content}/>
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
	const [snippets, setSnippets] = useState([]);
	const [selectedSnippetPrompt, setSelectedSnippetPrompt] = useState('');
  const [file, setFile] = useState(null);

	const handleFileChange = async (event: any) => {
		const file = event.target.files[0];
		setFile(file);

		if (file) {
			const formData = new FormData();
			formData.append('file', file);

			try {
				const response = await createFile(formData, sessionId);

				if (response.ok) {
					toast.success('File uploaded successfully');
				} else {
					toast.error('Failed to upload file');
				}
			} catch (error) {
				toast.error('An error occurred while uploading the file');
				console.error('An error occurred while uploading the file', error);
			}
		}
	};

	const fetchChatHistory = async () => {
		try {
			const response = await fetch("http://localhost:8000/conversation/" + sessionId);
			const data = await response.json();
			setConversation(data);
		} catch (error) {
			toast.error("Can't fetch chat history")
		}
	};

	const fetchSnippets = async () => {
		try {
			const snippets = await getSnippets();
			setSnippets(snippets);
		} catch (error) {
			console.log("Error fetching snippets");
		}
	}

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
				body: JSON.stringify({'message': `${selectedSnippetPrompt} ${message}`})
			});

			if (response.ok) {
				setIsLoading(false);
			} else {
				toast.error("Can't send message")
			}
		} catch (error) {
			toast.error("Can't send message")
			console.log(error)
		} finally {
			await fetchChatHistory();
			setSelectedSnippetPrompt("");
		}
	}

	useEffect(() => {
		fetchChatHistory();
		fetchSnippets();
	}, []);

	const transformedSnippets = [
		{label: 'None', value: '', description: 'None'},
		...snippets?.map(item => ({
			label: item?.name,
			value: item?.prompt,
			description: item?.prompt
		}))
	];

	const handleSnippetSelection = (value: any) => {
		setSelectedSnippetPrompt(value);
	}

	return (
		<>
			<div className="relative min-h-screen pb-16">
				<div className="p-4 sm:ml-64">
					<ConversationRender messages={conversation}/>
				</div>
			</div>
			<div className="p-4 flex justify-center fixed bottom-0 w-full">
				<form>
					<div className="rounded-md p-4 shadow-md w-36">
						<label htmlFor="upload" className="flex flex-col items-center gap-2 cursor-pointer">
							<svg fill="#ffffff" height="25px" width="25px" version="1.1" id="Capa_1"
									 xmlns="http://www.w3.org/2000/svg"
									 viewBox="0 0 374.116 374.116">
								<g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
								<g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g>
								<g id="SVGRepo_iconCarrier">
									<g>
										<path
											d="M344.058,207.506c-16.568,0-30,13.432-30,30v76.609h-254v-76.609c0-16.568-13.432-30-30-30c-16.568,0-30,13.432-30,30 v106.609c0,16.568,13.432,30,30,30h314c16.568,0,30-13.432,30-30V237.506C374.058,220.938,360.626,207.506,344.058,207.506z"></path>
										<path
											d="M123.57,135.915l33.488-33.488v111.775c0,16.568,13.432,30,30,30c16.568,0,30-13.432,30-30V102.426l33.488,33.488 c5.857,5.858,13.535,8.787,21.213,8.787c7.678,0,15.355-2.929,21.213-8.787c11.716-11.716,11.716-30.71,0-42.426L208.271,8.788 c-11.715-11.717-30.711-11.717-42.426,0L81.144,93.489c-11.716,11.716-11.716,30.71,0,42.426 C92.859,147.631,111.855,147.631,123.57,135.915z"></path>
									</g>
								</g>
							</svg>
						</label>
						<input id="upload" type="file" className="hidden" onChange={handleFileChange}/>
					</div>
				</form>

				<form onSubmit={sendMessage} className="flex items-center">
					<Select
						onChange={(e) => handleSnippetSelection(e.target.value)}
						items={transformedSnippets}
						label="Snippet"
						placeholder="Select a snippet"
						className="max-w-xs"
					>
						{(snippet) => (
							<SelectItem key={snippet.value} value={snippet.value}>
								{snippet.label}
							</SelectItem>
						)}
					</Select>
					<div className="sm:pl-64">
						<Input value={message} type={"text"} onChange={(e) => setMessage(e.target.value)}/>
					</div>
					<Button isLoading={isLoading} type={"submit"}>Send</Button>
				</form>
			</div>
		</>
	);
}