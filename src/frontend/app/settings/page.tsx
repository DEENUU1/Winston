'use client'

import {
	Button,
	Input,
	Modal,
	ModalBody,
	ModalContent,
	ModalFooter,
	ModalHeader,
	Switch,
	Textarea,
	useDisclosure
} from "@nextui-org/react"
import {useEffect, useState} from "react";

async function getAgents() {
	const res = await fetch("http://localhost:8000/agent/",
		{"cache": "no-cache"}
	)
	return res.json()
}

async function getSettings() {
	const res = await fetch("http://localhost:8000/settings/1", {
		"cache": "no-cache",
		headers: {
			'Content-Type': 'application/json'
		}
	})

	return res.json();
}

async function updateSettings(data: any) {
	const res = await fetch("http://localhost:8000/settings/1", {
		method: "PUT",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	})

	return res.json();
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

async function deleteSnippet(id: number) {
	const res = await fetch("http://localhost:8000/snippet/" + id, {
		method: "DELETE",
		headers: {
			'Content-Type': 'application/json'
		},
		cache: "no-cache"
	})
	return res.json()
}

async function updateSnippet(id: number, data: any) {
	const res = await fetch("http://localhost:8000/snippet/" + id, {
		method: "PUT",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	})
	return res.json()
}

export default function Settings() {
	const [settings, setSettings] = useState<any>(null);
	const [agents, setAgents] = useState<any[]>([]);
	const [snippets, setSnippets] = useState<any[]>([]);
	const {isOpen, onOpen, onOpenChange} = useDisclosure();
	const [currentSnippet, setCurrentSnippet] = useState<any>({name: '', prompt: ''});

	const fetchData = async () => {
		const agentsData = await getAgents();
		const settingsData = await getSettings();
		const snippetsData = await getSnippets();
		setAgents(agentsData);
		setSettings(settingsData);
		setSnippets(snippetsData);
	};

	useEffect(() => {
		fetchData();
	}, []);

	const agentIsUsed = (agentId: number) => {
		return settings?.agent_id === agentId;
	}

	const handleSnippetUpdate = async (e: any) => {
		e.preventDefault();
		try {
			await updateSnippet(currentSnippet.id, {name: currentSnippet.name, prompt: currentSnippet.prompt});
			fetchData();
		} catch (error) {
			console.error('Error updating snippet:', error);
		}
	};

	const handleSnippetDelete = async (e: any, snippetId: number) => {
		e.preventDefault();
		try {
			await deleteSnippet(snippetId);
			fetchData();
		} catch (error) {
			console.error('Error deleting snippet:', error);
		}
	}

	const handleAgentToggle = async (agentId: number) => {
		try {
			const newSettings = {...settings, agent_id: agentId};
			await updateSettings(newSettings);

			fetchData();
		} catch (error) {
			console.error('Error updating settings:', error);
		}
	}

	return (
		<>
			<div className="p-4 sm:ml-64">
				<h1>Settings</h1>
				<h2>Agents</h2>

				{agents.map((agent: any) => {
					return (
						<div key={agent.id} className="mb-4">
							<div className="flex items-center bg-gray-600 rounded-lg shadow-lg p-6">
								<div className="w-16 h-16 mr-4">
									<img src={`http://localhost:8000/${agent.avatar}`} alt="Image"
											 className="w-full h-full object-cover rounded-full"/>
								</div>

								<div className="flex-1">
									<p className="text-lg text-white font-semibold">{agent?.name}</p>
									<p className="text-white">{agent?.description}</p>
								</div>

								<div className="flex items-center">
									<Switch isSelected={agentIsUsed(agent.id)} onChange={() => handleAgentToggle(agent.id)}/>
								</div>
							</div>
						</div>
					);
				})}

				<Modal isOpen={isOpen} onOpenChange={onOpenChange}>
					<ModalContent>
						{(onClose) => (
							<>
								<ModalHeader className="flex flex-col gap-1">Update Snippet</ModalHeader>
								<ModalBody>
									<Input
										label={'Name'}
										required={true}
										value={currentSnippet.name}
										onChange={(e) => setCurrentSnippet({...currentSnippet, name: e.target.value})}
									/>
									<Textarea
										label={'Prompt'}
										required={true}
										value={currentSnippet.prompt}
										onChange={(e) => setCurrentSnippet({...currentSnippet, prompt: e.target.value})}
									/>
								</ModalBody>
								<ModalFooter>
									<Button onPress={onClose} color="danger" variant="light">
										Close
									</Button>
									<Button onPress={onClose} type={'submit'} color="warning" onClick={handleSnippetUpdate}>
										Update
									</Button>
								</ModalFooter>
							</>
						)}
					</ModalContent>
				</Modal>

				{snippets?.map((snippet: any) => {
					return (
						<div key={snippet.id} className="mb-4">
							<div className="flex items-center bg-gray-600 rounded-lg shadow-lg p-6">
								<div className="flex-1">
									<p className="text-lg text-white font-semibold">{snippet?.name}</p>
									<p className="text-white">{snippet?.description}</p>
								</div>

								<div className="flex items-center">
									<Button onClick={() => {
										setCurrentSnippet({
											id: snippet?.id,
											name: snippet?.name,
											prompt: snippet?.prompt
										});
										onOpen();
									}} color={'warning'}>
										Update
									</Button>
									<form onSubmit={(e) => {
										e.preventDefault();
										handleSnippetDelete(e, snippet.id)
									}}>
										<Button type={"submit"} color={"danger"}>Delete</Button>
									</form>
								</div>
							</div>
						</div>
					);
				})}


			</div>
		</>
	);
}