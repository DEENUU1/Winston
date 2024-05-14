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