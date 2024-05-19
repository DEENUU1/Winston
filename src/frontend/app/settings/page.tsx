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
import {toast} from "react-toastify";


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

async function createSnippet(data: any) {
	const res = await fetch("http://localhost:8000/snippet/", {
		method: "POST",
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	})
	return res.json()
}

async function createAgent(data: any) {
	const res = await fetch("http://localhost:8000/agent/", {
		method: "POST",
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
	const updateSnippetModal = useDisclosure();
	const createSnippetModal = useDisclosure();
	const createAgentModal = useDisclosure();
	const settingsModal = useDisclosure();
	const [currentSnippet, setCurrentSnippet] = useState<any>({name: '', prompt: ''});
	const [newSnippet, setNewSnippet] = useState({name: '', prompt: ''})
	const [newAgent, setNewAgent] = useState({name: '', description: '', prompt: '', llm_id: 1, temperature: 0.0})


	const fetchData = async () => {
		const agentsData = await getAgents();
		const settingsData = await getSettings();
		const snippetsData = await getSnippets();
		setAgents(agentsData);
		setSettings(settingsData);
		setSnippets(snippetsData);
	};

	const handleSnippetCreate = async (e: any) => {
		e.preventDefault();
		try{
			await createSnippet(newSnippet);
			fetchData();
			toast.success("Snippet created")
		} catch (error){
			toast.error("Error creating snippet")
		}
	}

	const handleAgentCreate = async (e: any) => {
		e.preventDefault();
		try{
			await createAgent(newAgent);
			fetchData();
		} catch (error){
			console.error("Error creating agent:", error);
		}
	}

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
			setNewSnippet({name: '', prompt: ''})
			fetchData();
		} catch (error) {
			console.error('Error updating settings:', error);
		}
	}

	return (
		<>
			<div className="p-4">
				<h1>Settings</h1>
				<h2>Agents</h2>

				<Button className={"mt-5 mb-5"} color={"success"} onPress={settingsModal.onOpen}>Settings</Button>
				<Modal isOpen={settingsModal.isOpen} onOpenChange={settingsModal.onOpenChange}>
					<ModalContent>
						{(onClose) => (
							<>
								<form>
									<ModalHeader className="flex flex-col gap-1">Update settings</ModalHeader>
									<ModalBody>
										<Input label={"OpenAI API Key"} value={settings?.openai_api_key}/>
										<Input label={"Groq API Key"} value={settings?.groq_api_key}/>
									</ModalBody>
									<ModalFooter>
										<Button color="danger" variant="light" onPress={onClose}>
											Close
										</Button>
										<Button type={"submit"} color="warning" onPress={onClose}>
											Update
										</Button>
									</ModalFooter>
								</form>
							</>
						)}
					</ModalContent>
				</Modal>


				<Button className={"mt-5 mb-5"} color={"success"} onPress={createAgentModal.onOpen}>Create agent</Button>
				<Modal isOpen={createAgentModal.isOpen} onOpenChange={createAgentModal.onOpenChange}>
					<ModalContent>
						{(onClose) => (
							<>
								<form onSubmit={handleAgentCreate}>
									<ModalHeader className="flex flex-col gap-1">Create agent</ModalHeader>
									<ModalBody>
										<Input
											label={'Name'}
											required={true}
											value={newAgent.name}
                      onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
										/>
										<Textarea
											label={'Description'}
											required={true}
											value={newAgent.description}
                      onChange={(e) => setNewAgent({ ...newAgent, description: e.target.value })}
										/>
										<Textarea
											label={'Prompt'}
											required={true}
											value={newAgent.prompt}
                      onChange={(e) => setNewAgent({ ...newAgent, prompt: e.target.value })}
										/>
									</ModalBody>
									<ModalFooter>
										<Button color="danger" variant="light" onPress={onClose}>
											Close
										</Button>
										<Button type={"submit"} color="primary" onPress={onClose}>
											Create
										</Button>
									</ModalFooter>
								</form>
							</>
						)}
					</ModalContent>
				</Modal>

				<Button className={"mt-5 mb-5"} color={"success"} onPress={createSnippetModal.onOpen}>Creates snippet</Button>
				<Modal isOpen={createSnippetModal.isOpen} onOpenChange={createSnippetModal.onOpenChange}>
					<ModalContent>
						{(onClose) => (
							<>
								<form onSubmit={handleSnippetCreate}>
									<ModalHeader className="flex flex-col gap-1">Create snippet</ModalHeader>
									<ModalBody>
										<Input
											label={'Name'}
											required={true}
											value={newSnippet.name}
                      onChange={(e) => setNewSnippet({ ...newSnippet, name: e.target.value })}
										/>
										<Textarea
											label={'Prompt'}
											required={true}
											value={newSnippet.prompt}
                      onChange={(e) => setNewSnippet({ ...newSnippet, prompt: e.target.value })}
										/>
									</ModalBody>
									<ModalFooter>
										<Button color="danger" variant="light" onPress={onClose}>
											Close
										</Button>
										<Button type={"submit"} color="primary" onPress={onClose}>
											Create
										</Button>
									</ModalFooter>
								</form>
							</>
						)}
					</ModalContent>
				</Modal>

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

				<Modal isOpen={updateSnippetModal.isOpen} onOpenChange={updateSnippetModal.onOpenChange}>
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
										updateSnippetModal.onOpen();
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