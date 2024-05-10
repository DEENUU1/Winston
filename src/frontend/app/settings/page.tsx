import Image from "next/image";


async function getAgents(){
	const res = await fetch("http://localhost:8000/agent/",
		{"cache": "no-store"}
	)
	return res.json()
}



export default async function Settings() {
	const agents = await getAgents()

	return (
		<>
			<div className="p-4 sm:ml-64">
				<h1>Settings</h1>

				<h2>Agents</h2>
				{agents.map((agent: any) => {
					return (
						<div key={agent.id}>
							<Image src={`http://localhost:8000/${agent.avatar}`} alt={agent.name} width={400} height={400}/>
							<h2>{agent.name}</h2>
							<p>{agent.description}</p>
						</div>
					)
				})}

			</div>
		</>
	);
}
