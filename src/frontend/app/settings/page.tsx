import Image from "next/image";
import Link from "next/link";


async function getAgents(){
	const res = await fetch("http://localhost:8000/agent/",
		{"cache": "no-cache"}
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
						<>
							<Link href={"/"}>
								<div key={agent.id} className="flex flex-col justify-center mb-5">
									<div
										className="relative flex flex-col md:flex-row md:space-x-5 space-y-3 md:space-y-0 rounded-xl shadow-lg p-3 max-w-xs md:max-w-3xl mx-auto border border-white bg-white">
										<div className="w-full md:w-1/3 bg-white grid place-items-center">
											<img
												src={`http://localhost:8000/${agent.avatar}`}
												alt="test" className="rounded-xl"/>
										</div>
										<div className="w-full md:w-2/3 bg-white flex flex-col space-y-2 p-3">
											<div className="flex justify-between item-center">
												<div
													className="bg-gray-200 px-3 py-1 rounded-full text-xs font-medium text-gray-800 hidden md:block">
													{agent?.llm?.name}
												</div>
											</div>
											<h3 className="font-black text-gray-800  text-xl">{agent.name}</h3>
											<p className="md:text-lg text-gray-500 text-base">{agent.description}</p>
										</div>
									</div>
								</div>
							</Link>
						</>

					)
				})}

			</div>
		</>
	);
}
