'use client'

import {FaCopy} from "react-icons/fa";
import {FaRegCopy} from "react-icons/fa6";
import React, {useState, } from "react";
// @ts-ignore
import {CopyToClipboard} from 'react-copy-to-clipboard';

import {toast} from "react-toastify";

export default function CopyButton({text}: {text: string}) {
    const [copied, setCopied] = useState(false);
    const [isHovered, setIsHovered] = useState(false);

    const handleCopy = () => {
        setCopied(true);
    }

    if(copied){
      toast.success('Copied to clipboard');
    }

    return (
        <CopyToClipboard text={text} onCopy={() => handleCopy()}>
            <span
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                style={{cursor: isHovered ? 'pointer' : 'default'}}
            >
              {isHovered ? <FaCopy size="1.2rem"/> : <FaRegCopy size="1.2rem"/>}
            </span>
        </CopyToClipboard>
    )
}
