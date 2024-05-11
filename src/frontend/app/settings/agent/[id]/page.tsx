'use client';

import Image from "next/image";
import {Button, Input, Select, SelectItem, Slider} from "@nextui-org/react";
import {useEffect, useState} from "react";


import {Textarea} from "@nextui-org/input";
import {Switch} from "@nextui-org/switch";

async function getAgent(id: string) {
	const res = await fetch(`http://localhost:8000/agent/${id}`,
		{"cache": "no-cache"}
	)
	return res.json()
}

async function getTools() {
	const res = await fetch(`http://localhost:8000/tool/`, {"cache": "no-store"})
	return res.json()
}

async function getLLMs() {
	const res = await fetch(`http://localhost:8000/llm/`, {"cache": "no-store"})
	return res.json()
}


async function updateAgent(id: string, data: any) {
	const res = await fetch(`http://localhost:8000/agent/` + id, {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	})
	return res.json()
}

async function updateTool(agentId: string, data: any) {
	const res = await fetch("http://localhost:8000/agent/" + agentId + "/tool/", {
		method: 'PUT',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(data)
	})
	return res.json()
}

interface PageParams {
	id: string;
}


export default function AgentDetails({params}: { params: PageParams }) {
	const [agent, setAgent] = useState()
	const [tools, setTools] = useState()
	const [llms, setLLMs] = useState()

	const handleDataFetch = async () => {
		const agentData = await getAgent(params.id);
		const toolsData = await getTools();
		const llmsData = await getLLMs();

		setAgent(agentData);
		setTools(toolsData);
		setLLMs(llmsData);

	}

	useEffect(() => {


		handleDataFetch()
	}, [params.id])

	const [agentUpdatedData, setAgentUpdatedData] = useState({
		"name": agent?.name,
		"description": agent?.description,
		"prompt": agent?.prompt,
		"temperature": agent?.temperature,
		"llm_id": agent?.llm?.id,
	})

	const handleAgentUpdate = async (e: any) => {
		e.preventDefault();

		await updateAgent(params.id, agentUpdatedData);

		const agentData = await getAgent(params.id);

		setAgent(agentData);
	}

	const transformedLLMsData = llms?.map(item => ({
		label: item.name,
		value: item.id,
		description: `ID: ${item.id}, Provider ID: ${item.provider_id}`
	}))

	const handleToolToggle = async (agentId: string, toolId: number) => {

		try {
			const isToolAssigned = agent?.tools?.some((aTool) => aTool.id === toolId);

			if (isToolAssigned) {
				const requestData = {
					operation_type: "remove",
					tool_id: toolId
				};
				await updateTool(agentId, requestData);
				handleDataFetch();
			}
			else if (!isToolAssigned) {
				const requestData = {
					operation_type: "add",
					tool_id: toolId
				};
				await updateTool(agentId, requestData);
				handleDataFetch();
			}
		} catch (error) {
			console.error('Error updating tool:', error);
		}
	}

	return (
		<>
			<div className="p-4 sm:ml-64 flex justify-center">
				<div className="w-full max-w-4xl">
					<form className="flex flex-col items-center" onSubmit={handleAgentUpdate}>
						<Image
							src={`http://localhost:8000/${agent?.avatar}`}
							className="rounded-full"
							alt={agent?.name}
							width={250}
							height={250}
						/>
						<Input
							className={"mt-10 w-full max-w-md"}
							onChange={(e) => agentUpdatedData.name}
							type={"text"}
							variant={"flat"}
							label={"Agent name"}
							value={agent?.name}
						/>

						{agent?.description !== undefined && (
							<Textarea
								label={"Description"}
								value={agent?.description}
								onChange={(e) => {
									setAgentUpdatedData((prevState) => ({...prevState, description: e.target.value}));
								}}
								className={"w-full max-w-md mt-5"}
							/>
						)}

						{agent?.temperature !== undefined && (
							<Slider
								onChange={(value) => agentUpdatedData.temperature = value}
								label="Temperature"
								step={0.1}
								maxValue={2}
								minValue={0}
								className={"w-full max-w-md mt-5"}
								defaultValue={agent?.temperature}
							/>
						)}

						{agent?.llm?.id !== undefined && (
							<Select
								onChange={(value) => agentUpdatedData.llm_id = value}
								label="LLM"
								items={transformedLLMsData}
								defaultSelectedKeys={[agent?.llm?.id.toString()]}
								className={"w-full max-w-md mt-5"}
							>
								{transformedLLMsData?.map((llm) => (
									<SelectItem key={llm?.value} value={llm?.value}>
										{llm?.label}
									</SelectItem>
								))}
							</Select>
						)}

						{agent?.prompt !== undefined && (
							<Textarea
								value={agent?.prompt}
								label={"Prompt"}
								onChange={(e) => agentUpdatedData.prompt = e.target.value}
								className={"w-full max-w-md mt-5"}
							/>
						)}

						<Button
							type={"submit"}
							className={"w-full max-w-md mt-5"}
						>
							Update
						</Button>
					</form>

					<form className="flex flex-col items-center mt-10">
						<ul>
							{tools?.map((tool) => (
								<li key={tool.id}>
									<div>
										<h2 className="font-bold text-md">{tool.name}</h2>
										<p className="font-thin">{tool.description}</p>
										<Switch
											isSelected={agent?.tools?.some((aTool) => aTool.id === tool.id)}
											onChange={(e) => handleToolToggle(agent?.id, tool.id)}
										/>
									</div>
								</li>
							))}
						</ul>
					</form>

				</div>
			</div>
		</>


	);

}
