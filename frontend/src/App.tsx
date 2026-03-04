import { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Send, Upload, FileText, Bot, User, Loader2 } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface Message {
    role: "user" | "bot";
    content: string;
}

function App() {
    const [file, setFile] = useState<File | null>(null);
    const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [uploading, setUploading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setUploading(true);
        const formData = new FormData();
        formData.append("file", file);

        try {
            await axios.post("/api/v1/upload", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            setUploadedFiles(prev => [...prev, file.name]);
            setFile(null); // Clear selected file after upload
            alert("PDF uploaded successfully!");
        } catch (error) {
            console.error(error);
            alert("Error uploading PDF");
        } finally {
            setUploading(false);
        }
    };

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage: Message = { role: "user", content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const res = await axios.post("/api/v1/chat", { question: input });
            const botMessage: Message = { role: "bot", content: res.data.response };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error(error);
            const errorMessage: Message = { role: "bot", content: "Error: Could not get response." };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gray-900 text-gray-100 font-sans">
            {/* Header */}
            <header className="flex items-center justify-between p-4 border-b border-gray-800 bg-gray-950">
                <div className="flex items-center gap-3 px-2 font-semibold text-lg text-indigo-400">
                    <Bot size={28} />
                    <span>Saad AI</span>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex flex-1 overflow-hidden">
                {/* Sidebar / Upload Area (Mobile hidden or collapsible ideally, but simplified here) */}
                <aside className="w-80 bg-gray-950 p-6 border-r border-gray-800 hidden md:flex flex-col gap-6">
                    <div className="space-y-4">
                        <h2 className="text-lg font-semibold text-gray-300">Document Context</h2>
                        <div className="border-2 border-dashed border-gray-700 rounded-xl p-6 flex flex-col items-center gap-4 hover:border-blue-500 transition-colors bg-gray-900/50">
                            <input
                                type="file"
                                accept=".pdf"
                                onChange={handleFileChange}
                                className="hidden"
                                id="file-upload"
                            />
                            <label htmlFor="file-upload" className="cursor-pointer flex flex-col items-center gap-2">
                                <Upload className="w-8 h-8 text-gray-400" />
                                <span className="text-sm text-gray-400 text-center">
                                    {file ? file.name : "Click to select PDF to Upload"}
                                </span>
                            </label>
                        </div>

                        <button
                            onClick={handleUpload}
                            disabled={!file || uploading}
                            className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg font-medium transition-all flex items-center justify-center gap-2"
                        >
                            {uploading ? <Loader2 className="animate-spin w-4 h-4" /> : <Upload className="w-4 h-4" />}
                            {uploading ? "Uploading..." : "Upload PDF"}
                        </button>

                        {uploadedFiles.length > 0 && (
                            <div className="mt-6 flex flex-col gap-2">
                                <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Active Documents</h3>
                                <ul className="space-y-2">
                                    {uploadedFiles.map((fname, idx) => (
                                        <li key={idx} className="flex items-center gap-2 text-sm bg-gray-800 p-2 rounded-md text-gray-200">
                                            <FileText className="w-4 h-4 text-blue-400" />
                                            <span className="truncate">{fname}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>

                    <div className="mt-auto text-xs text-gray-500 text-center">
                        <p>Powered by OpenAI & Pinecone</p>
                    </div>
                </aside>

                {/* Chat Area */}
                <div className="flex-1 flex flex-col relative w-full">
                    <div className="flex-1 overflow-y-auto p-4 md:p-8 space-y-6 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent">
                        {messages.length === 0 && (
                            <div className="text-center text-gray-500 mt-20">
                                <Bot className="w-16 h-16 mx-auto mb-4 opacity-20" />
                                <p className="text-xl font-medium">How can I help you with your document?</p>
                                <p className="text-sm mt-2">Upload a PDF to get started.</p>
                            </div>
                        )}

                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex gap-4 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                {msg.role === 'bot' && (
                                    <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center flex-shrink-0">
                                        <Bot className="w-5 h-5 text-blue-400" />
                                    </div>
                                )}

                                <div className={`max-w-[80%] rounded-2xl px-5 py-3 ${msg.role === 'user'
                                    ? 'bg-blue-600 text-white rounded-br-none'
                                    : 'bg-gray-800 text-gray-100 rounded-bl-none border border-gray-700'
                                    }`}>
                                    {msg.role === 'bot' ? (
                                        <div className="prose prose-invert prose-sm max-w-none">
                                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                                        </div>
                                    ) : (
                                        <p>{msg.content}</p>
                                    )}
                                </div>

                                {msg.role === 'user' && (
                                    <div className="w-8 h-8 rounded-full bg-purple-600/20 flex items-center justify-center flex-shrink-0">
                                        <User className="w-5 h-5 text-purple-400" />
                                    </div>
                                )}
                            </div>
                        ))}

                        {loading && (
                            <div className="flex gap-4">
                                <div className="w-8 h-8 rounded-full bg-blue-600/20 flex items-center justify-center flex-shrink-0">
                                    <Bot className="w-5 h-5 text-blue-400" />
                                </div>
                                <div className="bg-gray-800 rounded-2xl rounded-bl-none px-5 py-3 border border-gray-700 flex items-center gap-2">
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></span>
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input Area */}
                    <div className="p-4 bg-gray-950 border-t border-gray-800">
                        <div className="max-w-4xl mx-auto relative flex items-center gap-2 bg-gray-900 rounded-xl border border-gray-700 px-4 py-2 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                                placeholder="Ask a question about your PDF..."
                                className="flex-1 bg-transparent border-none outline-none text-white placeholder-gray-500 h-10"
                                disabled={loading}
                            />
                            <button
                                onClick={handleSend}
                                disabled={!input.trim() || loading}
                                className="p-2 text-blue-400 hover:text-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                            >
                                <Send className="w-5 h-5" />
                            </button>
                        </div>
                        <p className="text-center text-xs text-gray-600 mt-2">AI can make mistakes. Please verify important information.</p>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
