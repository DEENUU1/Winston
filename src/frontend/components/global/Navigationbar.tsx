import React, {useEffect, useState} from "react";
import {
	Badge,
	Button,
	Link,
	Modal,
	ModalBody,
	ModalContent,
	ModalFooter,
	ModalHeader,
	Navbar,
	NavbarBrand,
	NavbarContent,
	NavbarItem,
	NavbarMenu,
	NavbarMenuItem,
	NavbarMenuToggle,
	useDisclosure
} from "@nextui-org/react";
import {useRouter} from "next/navigation";


function getConversations() {
	// eslint-disable-next-line react-hooks/rules-of-hooks
	const [conversationList, setConversationlist] = useState([]);

	// eslint-disable-next-line react-hooks/rules-of-hooks
	useEffect(() => {
		fetch("http://localhost:8000/conversation/")
			.then(response => response.json())
			.then(data => setConversationlist(data));
	}, []);

	return conversationList;
}


export default function NavigationBar() {
	const [isMenuOpen, setIsMenuOpen] = React.useState(false);
	const router = useRouter()
	const {isOpen, onOpen, onOpenChange} = useDisclosure();

	const conversations = getConversations();

	async function createConversation() {
		const res = await fetch("http://localhost:8000/conversation/new/", {
			method: 'POST'
		})
		return res.json()
	}

	const handleCreateConversation = async () => {
		const newConversation = await createConversation();
		const newSessionId = newConversation.session_id;
		router.push(`/${newSessionId}`)
	}

	return (
		<>
			<Navbar onMenuOpenChange={setIsMenuOpen}>
				<NavbarContent>
					<NavbarMenuToggle
						aria-label={isMenuOpen ? "Close menu" : "Open menu"}
						className="sm:hidden"
					/>
					<NavbarBrand>
						<p onClick={handleCreateConversation} className="font-bold text-inherit">Winston</p>
					</NavbarBrand>
				</NavbarContent>

				<NavbarContent className="hidden sm:flex gap-4" justify="center">
					<NavbarItem>
						<Badge content="5">
							<Link onPress={onOpen} color="foreground" href="#">
								Conversations
							</Link>
						</Badge>
					</NavbarItem>
					<NavbarItem isActive>
						<Link onClick={handleCreateConversation} href="#" aria-current="page">
							Create new conversation
						</Link>
					</NavbarItem>
				</NavbarContent>
				<NavbarContent justify="end">
					<NavbarItem className="hidden lg:flex">
						<Link href="/settings">Settings</Link>
					</NavbarItem>
				</NavbarContent>
				<NavbarMenu>
					<NavbarMenuItem>
						<Badge content="5">
							<Link onPress={onOpen} color="foreground" href="#">
								Conversations
							</Link>
						</Badge>
					</NavbarMenuItem>
					<NavbarMenuItem>
						<Link onClick={handleCreateConversation} href="#" aria-current="page">
							Create new conversation
						</Link>
					</NavbarMenuItem>
					<NavbarMenuItem>
						<Link href="/settings">Settings</Link>
					</NavbarMenuItem>
				</NavbarMenu>
			</Navbar>

			<Modal isOpen={isOpen} onOpenChange={onOpenChange}>
				<ModalContent>
					{(onClose) => (
						<>
							<ModalHeader className="flex flex-col gap-1">Modal Title</ModalHeader>
							<ModalBody>
								<ul className="space-y-2 font-medium">
									{conversations?.session_id?.map(session_id => (
										<li key={session_id}>
											<Link href={`/${session_id}`}
														className="flex items-center p-2 text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 group">
												<span className="ms-3">{session_id}</span>
											</Link>
										</li>
									))}
								</ul>
							</ModalBody>
							<ModalFooter>
								<Button color="danger" variant="light" onPress={onClose}>
									Close
								</Button>
								<Button color="primary" onPress={onClose}>
									Action
								</Button>
							</ModalFooter>
						</>
					)}
				</ModalContent>
			</Modal>
		</>
	);
}
