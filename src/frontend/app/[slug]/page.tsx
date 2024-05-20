'use client';

import CopyButton from "@/components/CopyButton";
import {useEffect, useState} from "react";
import {Button, Input, Select, SelectItem} from "@nextui-org/react";
import Markdown from "react-markdown";
import gfm from 'remark-gfm';
import {toast} from "react-toastify";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, useDisclosure} from "@nextui-org/react";

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

async function getFiles(session_id: string){
	const res = await fetch("http://localhost:8000/file/chat/" + session_id + "/", {
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
  const [file, setFile] = useState(null);
  const {isOpen, onOpen, onOpenChange} = useDisclosure();
	const [files, setFiles] = useState([])

	const fetchFiles = async () => {
		try {
			const files = await getFiles(sessionId);
			setFiles(files);
		} catch (error) {
			console.log(error)
		} finally {
			console.log("Fetch files")
		}
	};

	useEffect(() => {
		if (isOpen) {
			fetchFiles();
		}
	}, [isOpen]);

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
				<div className="p-4">
					<Button className={"mb-5"} onPress={onOpen}>Files</Button>
					<Modal isOpen={isOpen} onOpenChange={onOpenChange}>
						<ModalContent>
							{(onClose) => (
								<>
									<ModalHeader className="flex flex-col gap-1">Files</ModalHeader>
									<ModalBody>
										{files?.map((file, index) => (
											<div key={index} className="flex flex-col gap-1">
												<h2 className={"font-bold"}>{file?.original_file_name}</h2>
												<span className={"text-gray-400"}>{file?.path}</span>
											</div>
										))}

									</ModalBody>
									<ModalFooter>
										<Button color="danger" variant="light" onPress={onClose}>
											Close
										</Button>
									</ModalFooter>
								</>
							)}
						</ModalContent>
					</Modal>


					<ConversationRender messages={conversation}/>
				</div>
			</div>

			<div className={"bottom-0 sticky p-4 bg-black"}>
				<form className={""} onSubmit={sendMessage}>
					<div className="flex w-full flex-wrap md:flex-nowrap gap-4">
						<Input value={message} type={"text"} onChange={(e) => setMessage(e.target.value)}/>
						<Button isLoading={isLoading} type={"submit"}>Send</Button>
					</div>

					<div className="flex w-full flex-wrap md:flex-nowrap gap-4 mt-5">
						<Input onChange={handleFileChange} type="file" label={"File"} />
						<Select
						onChange={(e) => handleSnippetSelection(e.target.value)}
						items={transformedSnippets}
						label="Snippet"
						placeholder="Select a snippet"
					>
						{(snippet) => (
								<SelectItem key={snippet.value} value={snippet.value}>
									{snippet.label}
								</SelectItem>
						)}
					</Select>
					</div>
				</form>
			</div>
		</>
);
}