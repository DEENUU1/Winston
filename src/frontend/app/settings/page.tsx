'use client'

import Link from "next/link";
import {Switch} from "@nextui-org/react"
import {useEffect, useState} from "react";

async function getAgents(){
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

export default function Settings() {
	const [settings, setSettings] = useState<any>(null);
	const [agents, setAgents] = useState<any[]>([]);

	const fetchData = async () => {
		const agentsData = await getAgents();
		const settingsData = await getSettings();
		setAgents(agentsData);
		setSettings(settingsData);
	};

	useEffect(() => {
		fetchData();
	}, []);

	const agentIsUsed = (agentId: number) => {
		return settings?.agent_id === agentId;
	}

	const handleAgentToggle = async (agentId: number) => {
		try {
			const newSettings = { ...settings, agent_id: agentId };
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
							<div className="relative flex flex-col md:flex-row md:space-x-5 space-y-3 md:space-y-0 rounded-xl shadow-lg p-3 max-w-xs md:max-w-3xl mx-auto border border-white bg-white">
								<div className="w-full md:w-1/3 bg-white grid place-items-center">
									<img src={`http://localhost:8000/${agent.avatar}`} alt="test" className="rounded-xl" />
								</div>
								<div className="w-full md:w-2/3 bg-white flex flex-col space-y-2 p-3">
									<div className="flex justify-between item-center">
										<div className="bg-gray-200 px-3 py-1 rounded-full text-xs font-medium text-gray-800 hidden md:block">
											{agent?.llm?.name}
										</div>
									</div>
									<Link href={`/settings/agent/${agent.id}`}>
										<h3 className="font-black text-gray-800 text-xl">{agent?.name}</h3>
									</Link>
									<p className="md:text-lg text-gray-500 text-base">{agent?.description}</p>
									<Switch
										isSelected={agentIsUsed(agent.id)}
										onChange={() => handleAgentToggle(agent.id)}
									/>
								</div>
							</div>
						</div>
					);
				})}
			</div>
		</>
	);
}